#!/bin/sh
# Put a fresh PowerCenter token in place. Run this on the server, as root.
#
#   ./place-stryd-token.sh
#   <paste the JWT, press Enter, then Ctrl-D>
#
# Reads the token on stdin rather than as an argument, so it never reaches the
# shell history or the process list. Writes it atomically, so the path unit sees
# one complete file rather than a truncation followed by a write.
set -eu

DEST="${STRYD_TOKEN_FILE:-/etc/postrun/stryd.token}"
TMP="$DEST.new"

printf 'Paste the JWT, then press Enter and Ctrl-D:\n' >&2
umask 077
mkdir -p "$(dirname "$DEST")"
tr -d ' \t\r\n' > "$TMP"

# A truncated paste is the usual failure, and it is worth catching before it
# becomes a 401 an hour later.
segments=$(tr '.' '\n' < "$TMP" | wc -l)
if [ "$segments" -ne 3 ]; then
  rm -f "$TMP"
  echo "That is not a JWT: expected three dot-separated segments, got $segments." >&2
  echo "Copy the whole value, or the part after 'Bearer ' in the Authorization header." >&2
  exit 1
fi

chown root:root "$TMP" 2>/dev/null || true
chmod 600 "$TMP"
mv "$TMP" "$DEST"
echo "Placed $DEST ($(wc -c < "$DEST") bytes)." >&2

if [ -d /opt/postrun-sync ]; then
  echo >&2
  cd /opt/postrun-sync && python3 -m tools.stryd.sync --check || true
fi
