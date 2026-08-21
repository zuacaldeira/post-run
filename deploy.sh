#!/usr/bin/env bash
# Deploy the app to postrun.zuacaldeira.com.
#
# There is no build step and no registry: the files in this directory are the
# app, and rsync puts them on the server. Run it from the repo root.
#
#   ./deploy.sh
#
# No --delete. It only removes extraneous files when rsync is mirroring a
# directory, and this passes a list of individual files, so it never deleted
# anything -- which was discovered when bg.mp4 stayed on the server after the
# backdrop stopped using it. A file dropped from the list below has to be
# removed from the web root by hand.
#
# That also means plan.json was never at risk: it is written on the server by
# tools/stryd/sync.py and no deploy was ever going to remove it.
set -euo pipefail

HOST="${POSTRUN_HOST:-root@217.154.2.230}"
ROOT="/var/www/postrun.zuacaldeira.com"

FILES=(index.html sw.js manifest.webmanifest
       icon-192.png icon-512.png icon-maskable-512.png
       bg.jpg chroma-js-LICENSE.txt)

for f in "${FILES[@]}"; do
  [[ -f "$f" ]] || { echo "missing: $f" >&2; exit 1; }
done

ssh "$HOST" "mkdir -p $ROOT"
rsync -av --chmod=F644 "${FILES[@]}" "$HOST:$ROOT/"
ssh "$HOST" "chown -R www-data:www-data $ROOT"

# index.html and sw.js are served no-cache, so a reload picks the new build up;
# nothing needs restarting. Confirm what the browser will actually receive.
echo
curl -sS -I https://postrun.zuacaldeira.com/ \
  | grep -iE 'HTTP/|cache-control|content-security-policy' | cut -c1-80
