#!/usr/bin/env bash
# ランチャーをPWAとして exbridge.jp/launcher/ に公開(iPhone/Androidの「ホーム画面に追加」用)
set -euo pipefail
cd "$(dirname "$0")/.."
set -a; . /home/kojima/work/aixec/.env; set +a
R=/web/exbridge_jp/launcher
up(){ curl --fail --silent --show-error --ftp-create-dirs -T "$1" \
  "ftp://${FTP_USER}:${FTP_PASS}@${FTP_HOST}${R}/${2}"; echo "up: $2"; }
up www/index.html index.html
up www/manifest.webmanifest manifest.webmanifest
up www/sw.js sw.js
for ic in icon-192.png icon-512.png icon-maskable.png; do up "www/assets/$ic" "assets/$ic"; done
echo "https://exbridge.jp/launcher/"
