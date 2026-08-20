/* Cache the whole app on install so the routine works with no signal.
   Only the YouTube demos need the network. */
/* A namespace, not a release number -- it no longer has to be bumped to ship. Install
   revalidates every asset past the HTTP cache, and the page checks itself for a newer
   build on its own, so both paths refresh without a rename. Change it only to force
   every client to rebuild its cache from scratch. */
const CACHE = "postrun-v2";
const ASSETS = ["./", "./index.html", "./bg.mp4", "./poster.jpg",
                "./manifest.webmanifest", "./icon-192.png", "./icon-512.png", "./icon-maskable-512.png"];

/* no-cache, not the default: install has to reach past the browser's HTTP cache,
   or a fresh worker can happily reinstall the build it was meant to replace. Each
   asset is put separately so one failure cannot abort the whole install. */
self.addEventListener("install", e => {
  e.waitUntil(caches.open(CACHE).then(c => Promise.all(ASSETS.map(u =>
    fetch(new Request(u, { cache:"no-cache" }))
      .then(r => r.status === 200 ? c.put(u, r) : null)
      .catch(() => null)
  ))).then(() => self.skipWaiting()));
});
self.addEventListener("activate", e => {
  e.waitUntil(caches.keys()
    .then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k))))
    .then(() => self.clients.claim()));
});
/* Stale-while-revalidate. Cache-first alone never re-read anything it had already
   stored, so a deploy only reached people who reinstalled the app. Now the cached copy
   still answers instantly -- the routine has to work with no signal -- and the refetch
   running behind it means the next launch starts on the new build, whether or not the
   version above was remembered. */
self.addEventListener("fetch", e => {
  if (e.request.method !== "GET") return;
  const url = new URL(e.request.url);
  if (url.origin !== location.origin) return;          // let YouTube go to the network
  e.respondWith(caches.open(CACHE).then(cache => cache.match(e.request).then(hit => {
    const fresh = fetch(e.request).then(res => {
      /* 200 only: the video's range requests come back 206 and cannot be put(), and an
         error page must never be allowed to overwrite a good asset */
      if (res.status === 200) cache.put(e.request, res.clone()).catch(() => {});
      return res;
    }).catch(() => hit || cache.match("./index.html"));
    /* offline, or just slow: the revalidation must outlive the response we already gave */
    e.waitUntil(fresh);
    return hit || fresh;
  })));
});

/* Serving the stale page is only half of an update -- the page also has to be told, or
   the new build sits in the cache until the next cold start. The page asks for this
   check itself rather than the fetch handler announcing during a navigation: at that
   point the only client listening is the document being torn down, so the news would
   go to a page that is already on its way out. Asking after load reaches a client that
   is actually there, and works just as well for an installed app left open for days. */
function announce(){
  return self.clients.matchAll({ type:"window" })
    .then(cs => cs.forEach(c => c.postMessage({ type:"update-ready" })));
}

function checkPage(url){
  return caches.open(CACHE).then(cache => Promise.all([
    cache.match(url),
    fetch(new Request(url, { cache:"no-cache" }))      // conditional: a 304 costs nothing
  ]).then(([hit, res]) => {
    if (!res || res.status !== 200) return;
    const after = res.clone().text();
    return Promise.all([hit ? hit.text() : null, after, cache.put(url, res)])
      .then(([before, body]) => {
        if (before !== null && before !== body) return announce();
      });
  })).catch(() => {});
}

self.addEventListener("message", e => {
  if (e.data && e.data.type === "check-update")
    e.waitUntil(checkPage(e.data.url || "./index.html"));
});
