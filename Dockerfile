# Static app: no build step, nothing to compile. nginx:alpine is the whole runtime.
# For a rootless host, nginxinc/nginx-unprivileged:alpine is a drop-in swap -- it
# listens on 8080, so change the listen directive and the compose port with it.
FROM nginx:alpine

COPY deploy/nginx.conf /etc/nginx/conf.d/default.conf

# Files are listed rather than COPY . so the image can never pick up the repo's
# git history, notes or scratch files by accident.
COPY index.html sw.js manifest.webmanifest /usr/share/nginx/html/
COPY icon-192.png icon-512.png icon-maskable-512.png poster.jpg bg.mp4 /usr/share/nginx/html/
# chroma.js is inlined into index.html, so its licence ships with the app
COPY chroma-js-LICENSE.txt /usr/share/nginx/html/

EXPOSE 80

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD wget -qO- http://127.0.0.1/healthz || exit 1
