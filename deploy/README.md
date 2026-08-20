# Deploying

The app ships as a container: nginx plus the static files, no build step.

## On the server

```sh
docker compose pull && docker compose up -d
curl -sI http://127.0.0.1:8080/healthz     # 200 ok
```

The image is published to `ghcr.io/zuacaldeira/post-run` by
`.github/workflows/docker.yml` on every push. `:latest` only ever moves from the
default branch; feature branches publish under their own tag, so a work-in-progress
build cannot become what the server pulls next. GHCR packages start **private** --
either `docker login ghcr.io` on the server with a read:packages token, or mark the
package public in its GitHub settings.

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
