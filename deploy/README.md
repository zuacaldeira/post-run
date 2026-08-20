# Deploying

The app ships as a container: nginx plus the static files, no build step.

## On the server

```sh
cp .env.example .env        # set APP_DOMAIN, and IMAGE_TAG if not on :latest
docker compose pull && docker compose up -d
curl -sI http://127.0.0.1:8081/healthz     # 200 ok, straight from the container
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
build cannot become what the server pulls next.

GHCR packages start **private**; this server is already logged in to `ghcr.io`
for images it pulls for other sites, so it can pull this one too. On a host
without that, either `docker login ghcr.io` with a read:packages token or mark
the package public in its GitHub settings.

## The subdomain

`postrun.zuacaldeira.com` already resolves to the server: DNS for the zone is at
Strato, and it answers for subdomains without a per-host record. Nothing had to
be created. If that ever changes, one A record at the server's public IP is the
whole requirement (AAAA too if it has IPv6).

`APP_DOMAIN` in `.env` only feeds the Caddy front end, which this deployment
does not use; the hostname that matters here is the `server_name` in
`deploy/nginx-host.conf`. Nothing else in the repo hardcodes it.

The zone is not behind Cloudflare, so the HTTP-01 challenge reaches this box
directly. Were it ever proxied, the record would have to stay DNS-only until the
first certificate is issued -- an orange cloud terminates TLS at the edge, and
the challenge would be answered for a hostname this server does not control.

### The deployed setup: host nginx + certbot

`postrun.zuacaldeira.com` runs this way. The box already terminates TLS for a
dozen other sites with nginx and certbot, so 80 and 443 are spoken for and Caddy
is not used. `deploy/nginx-host.conf` is that vhost, kept in the repo so the
served configuration is reviewable here rather than only on the server.

```sh
install -m644 deploy/nginx-host.conf /etc/nginx/sites-available/postrun.zuacaldeira.com
ln -s ../sites-available/postrun.zuacaldeira.com /etc/nginx/sites-enabled/
```

The 443 block will not load until the certificate exists, so issue it first with
the port-80 block alone in place, then enable the whole file:

```sh
certbot certonly --webroot -w /var/www/certbot -d postrun.zuacaldeira.com
nginx -t && systemctl reload nginx
```

Renewal is the same webroot the other certs on the box use; the timer picks it
up with no per-site hook.

### If nothing is terminating TLS on the box yet

```sh
docker compose -f compose.yaml -f compose.tls.yaml up -d
```

That adds Caddy, which gets a Let's Encrypt certificate on first start and
renews it on its own. Keep the `caddy_data` volume: certificates live there, and
recreating without it means re-issuing every time, which runs into rate limits.

Caddy wants 80 and 443 to itself, so this is for a fresh box only -- on a server
already running a web server it will fail to bind.

### If you already run a different reverse proxy

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

The port is bound to `127.0.0.1` so only the proxy can reach it. It is 8081
rather than the more obvious 8080, which is already taken on this server.

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
