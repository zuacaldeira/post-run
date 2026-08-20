# Deploying

The app is eight static files with no build step, so the deployment is the
simplest thing that can work: rsync them to the server and let nginx serve them
off disk. No image, no registry, no CI, no container runtime.

```sh
./deploy.sh
```

That copies the app to `/var/www/postrun.zuacaldeira.com` on the server and
prints the headers the browser will actually receive. Nothing needs restarting:
`index.html` and `sw.js` are served `no-cache`, so the next load picks the new
build up.

Set `POSTRUN_HOST` to deploy somewhere else; it defaults to the server that runs
the site today.

## nginx

`deploy/nginx-host.conf` is the served vhost, kept in the repo so the
configuration is reviewable here rather than only on the box. It is installed as
`/etc/nginx/sites-available/postrun.zuacaldeira.com` and symlinked into
`sites-enabled`. After editing it:

```sh
scp deploy/nginx-host.conf root@<server>:/tmp/postrun-vhost.conf
ssh root@<server> 'install -m644 /tmp/postrun-vhost.conf \
  /etc/nginx/sites-available/postrun.zuacaldeira.com && nginx -t && systemctl reload nginx'
```

Always `nginx -t` before reloading. The box serves a dozen other sites from the
same nginx, and a broken vhost takes all of them down together.

### The headers are the deployment

There is no framework here to fall back on -- if the vhost is wrong the app
quietly stops being an app:

- **`Cache-Control: no-cache`** on everything. The filenames are not
  content-hashed, so freshness has to come from revalidation rather than a
  `max-age` guess. The browser keeps its copy and always asks; an unchanged file
  costs a 304. The service worker refreshes itself through this same cache, so a
  long `max-age` would throttle how fast a deploy reaches an installed app. The
  whole app is ~150 KB; there is nothing to win by caching harder.
- **The CSP** allows this origin, YouTube frames and YouTube thumbnails, nothing
  else. Adding a third-party script, font or image means editing it.
- **`application/manifest+json`** is declared explicitly. It is not in nginx's
  `mime.types`, and a manifest served as `text/plain` is ignored -- no install
  prompt, no icon.
- **Every `add_header` sits at server level.** nginx replaces the whole
  inherited set the moment a location adds one of its own, so a single stray
  `add_header` inside a `location` would silently drop the CSP for that path.

If assets ever get content-hashed names, give those a long `max-age` and leave
`index.html` and `sw.js` on `no-cache`.

## TLS

The certificate comes from Let's Encrypt via certbot, webroot mode, the same way
every other site on this box gets one:

```sh
certbot certonly --webroot -w /var/www/certbot -d postrun.zuacaldeira.com
```

The port-80 block serves `/.well-known/acme-challenge/` from that webroot and
redirects everything else, so issuance and renewal work without touching the
443 block.

Renewal runs from `certbot.timer`. Webroot mode writes the new certificate and
stops there -- nothing tells nginx -- so nginx would go on presenting the old
certificate until something reloaded it, and a renewal that succeeded on disk
would still expire in the browser. `/etc/letsencrypt/renewal-hooks/deploy/reload-nginx.sh`
closes that: it runs `nginx -t && systemctl reload nginx` after any successful
renewal, for every certificate on the box.

TLS is not optional here. Service workers only register on a secure origin, so
over plain HTTP or a bare LAN IP the app silently loses offline mode, caching
and self-updating, and degrades to an ordinary web page.

## The subdomain

`postrun.zuacaldeira.com` already resolves to the server: DNS for the zone is at
Strato, which answers for subdomains without a per-host record, so nothing had
to be created. If that ever changes, one A record at the server's public IP is
the whole requirement (AAAA too if it has IPv6).

The zone is not behind Cloudflare, so the HTTP-01 challenge reaches this box
directly. Were it ever proxied, the record would have to stay DNS-only until the
first certificate is issued -- an orange cloud terminates TLS at the edge, and
the challenge would be answered for a hostname this server does not control.

## Subpath

`start_url` and `scope` are relative and nothing in the app uses an absolute
path, so it works unchanged at a domain root or under `/post-run/`.

## It used to be a container

Through commit `45a3ac0` this shipped as an nginx image built by GitHub Actions,
published to GHCR and pulled by the server behind a reverse proxy. That is a
reasonable shape for an app with a build step; for eight static files it was a
registry, a CI run and a second nginx standing between an edit and the server.
`git show 45a3ac0` has it all if it is ever wanted back.
