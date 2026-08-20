#!/usr/bin/env bash
# Deploy the app to postrun.zuacaldeira.com.
#
# There is no build step and no registry: the files in this directory are the
# app, and rsync puts them on the server. Run it from the repo root.
#
#   ./deploy.sh
#
# --delete is deliberate: the target holds nothing but these files, so a rename
# should remove the old name rather than leave it served forever. Only the app's
# own files are listed, so the repo's git history, scripts and docs stay here.
#
# plan.json is the exception and has to be excluded by name. It is written on the
# server by tools/stryd/sync.py, so it is exactly the "extraneous" file --delete
# exists to remove -- and deploying the app would otherwise throw away the plan
# every time.
set -euo pipefail

HOST="${POSTRUN_HOST:-root@217.154.2.230}"
ROOT="/var/www/postrun.zuacaldeira.com"

FILES=(index.html sw.js manifest.webmanifest
       icon-192.png icon-512.png icon-maskable-512.png
       poster.jpg bg.mp4 chroma-js-LICENSE.txt)

for f in "${FILES[@]}"; do
  [[ -f "$f" ]] || { echo "missing: $f" >&2; exit 1; }
done

ssh "$HOST" "mkdir -p $ROOT"
rsync -av --delete --exclude=plan.json --chmod=F644 "${FILES[@]}" "$HOST:$ROOT/"
ssh "$HOST" "chown -R www-data:www-data $ROOT"

# index.html and sw.js are served no-cache, so a reload picks the new build up;
# nothing needs restarting. Confirm what the browser will actually receive.
echo
curl -sS -I https://postrun.zuacaldeira.com/ \
  | grep -iE 'HTTP/|cache-control|content-security-policy' | cut -c1-80
