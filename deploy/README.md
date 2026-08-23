# Deploying

The app ships as a container: nginx plus the static files, no build step.

## On the server

```sh
cp .env.example .env        # set APP_DOMAIN, and IMAGE_TAG if not on :latest
docker compose pull && docker compose up -d
curl -sI http://127.0.0.1:8080/healthz     # 200 ok, straight from the container
```

Once the proxy is up, check what the browser will actually receive:

```sh
curl -sI https://postrun.zuacaldeira.com/ | grep -iE 'cache-control|content-security|strict-transport'
```

`Cache-Control: no-cache` and the CSP must both survive the proxy. If either is
missing, the proxy is stripping headers and the app will not update itself.

The image is published to `ghcr.io/zuacaldeira/post-run` by
`.github/workflows/docker.yml` on every push. `:latest` only ever moves from the
default branch; feature branches publish under their own tag, so a work-in-progress
build cannot become what the server pulls next. GHCR packages start **private** --
either `docker login ghcr.io` on the server with a read:packages token, or mark the
package public in its GitHub settings.

## The subdomain

Create one DNS record, pointing at the server's public IP:

```
postrun.zuacaldeira.com.   A     <server ip>      # AAAA too if it has IPv6
```

Then `cp .env.example .env` and set `APP_DOMAIN` to match. Nothing else in the
repo hardcodes the hostname.

**If zuacaldeira.com is on Cloudflare**, leave this record DNS-only (grey cloud)
at least until the first certificate is issued -- an orange-clouded record
terminates TLS at Cloudflare's edge, so Caddy's HTTP-01 challenge is answering
for a hostname it does not actually control. Once issued you can proxy it and
switch Cloudflare to Full (strict), or skip Caddy entirely and use a Cloudflare
origin certificate.

### If nothing is terminating TLS on the box yet

```sh
docker compose -f compose.yaml -f compose.tls.yaml up -d
```

That adds Caddy, which gets a Let's Encrypt certificate on first start and
renews it on its own. Keep the `caddy_data` volume: certificates live there, and
recreating without it means re-issuing every time, which runs into rate limits.

### If you already run a reverse proxy

Skip `compose.tls.yaml`. Put your proxy on the `web` network and send it to
`post-run:80`. For Traefik that is labels on the post-run service:

```yaml
    labels:
      traefik.enable: "true"
      traefik.http.routers.postrun.rule: Host(`postrun.zuacaldeira.com`)
      traefik.http.routers.postrun.entrypoints: websecure
      traefik.http.routers.postrun.tls.certresolver: letsencrypt
      traefik.http.services.postrun.loadbalancer.server.port: "80"
```

Whatever the proxy, it must pass the origin's response headers through
untouched. The CSP and the cache headers come from the app's own nginx; a proxy
that rewrites or duplicates them is how the two copies drift apart.

## TLS is not optional

The container speaks plain HTTP and expects your proxy to terminate TLS in front of
it. Service workers only register on a secure origin, so on plain HTTP or a bare LAN
IP the app quietly loses offline mode, caching and self-updating and degrades to an
ordinary web page. It needs a real hostname with a certificate.

The port is bound to `127.0.0.1` so only the proxy can reach it.

## Cache headers

Everything is served `no-cache`: the browser keeps its copy but always revalidates,
and an unchanged file costs a 304. This is deliberate. The service worker refreshes
itself by revalidating through the browser's HTTP cache, so a long `max-age` here
would throttle how fast a deploy reaches an installed app. The whole app is ~150 KB,
so there is nothing to win by caching harder.

If assets ever get content-hashed names, give those a long `max-age` and leave
`index.html` and `sw.js` on `no-cache`.

## Subpath

`start_url` and `scope` are relative and nothing in the app uses an absolute path,
so it works unchanged at a domain root or under `/post-run/`.

## Hourly training sync

```sh
docker compose -f compose.yaml -f compose.sync.yaml up -d      # add -f compose.tls.yaml too
docker compose logs -f sync
```

Every hour it asks intervals.icu what was planned and what was actually run, and
writes `data/training.json` into a volume the web container publishes read-only.
The app shows the line for whichever day you are looking at; without this overlay
the file is absent, the line stays hidden and nothing else changes.

intervals.icu is the only source. Garmin has no usable API, but the watch already
syncs there carrying the Stryd power with it, and the plan lives there too -- so
one call answers both halves of "was this executed" instead of reconciling two
services that disagree about where a day begins.

A failed sync never overwrites good data: the app keeps showing the last
successful pull rather than going blank because of one 500.

**This file is public.** It sits at `https://<your domain>/data/training.json`
with no authentication, so anyone with the URL can read your training. It is your
domain and an unguessable-ish path, which may well be enough -- but if not, put
basic auth on `location /data/` in `deploy/nginx.conf`, or serve it from a path
with a random component.

### Checking what the API actually returns

The field names below are taken from intervals.icu's documented shape and were
never exercised against the live API from the machine that wrote them. If the
line looks wrong or empty:

```sh
docker compose run --rm sync --once --dump /data --out /data/training.json
```

That saves the raw `events.json` and `activities.json` next to the output so you
can see exactly what came back.
