/* Cache the whole app on install so the routine works with no signal.
   Only the YouTube demos need the network. */
/* Bump this on every deploy. Changing these bytes is what makes the browser reinstall
   the worker; the new cache name is what makes install() re-pull the assets. */
const CACHE = "postrun-v2";
const ASSETS = ["./", "./index.html", "./bg.mp4", "./poster.jpg",
                "./manifest.webmanifest", "./icon-192.png", "./icon-512.png", "./icon-maskable-512.png"];

self.addEventListener("install", e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(ASSETS)).then(() => self.skipWaiting()));
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
