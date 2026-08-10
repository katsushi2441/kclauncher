#!/usr/bin/env bash
# kclauncher.exbridge.jp を公開:
#   /              LP(index.html=英語 / kclauncher.html=日本語) + assets + kclauncher.apk
#   /iphone/       PWAランチャー本体(iPhoneはSafari→ホーム画面に追加)
set -euo pipefail
cd "$(dirname "$0")/.."
set -a; . /home/kojima/work/aixec/.env; set +a
R=/web/kclauncher_exbridge_jp
up(){ curl --fail --silent --show-error --ftp-create-dirs -T "$1" \
  "ftp://${FTP_USER}:${FTP_PASS}@${FTP_HOST}${R}/${2}"; echo "  up: $2"; }

echo "[LP] ルート"
up landing/index.html          index.html
up landing/kclauncher.html     kclauncher.html
up landing/kclauncher.apk      kclauncher.apk
for a in ogp.png screenshot.png kurage_avatar_face.webp; do up "landing/assets/$a" "assets/$a"; done

echo "[PWA] /iphone/"
up www/index.html              iphone/index.html
up www/manifest.webmanifest    iphone/manifest.webmanifest
up www/sw.js                   iphone/sw.js
for ic in icon-192.png icon-512.png icon-maskable.png; do up "www/assets/$ic" "iphone/assets/$ic"; done

echo
echo "  LP(JA): https://kclauncher.exbridge.jp/kclauncher.html"
echo "  LP(EN): https://kclauncher.exbridge.jp/"
echo "  PWA   : https://kclauncher.exbridge.jp/iphone/"
echo "  APK   : https://kclauncher.exbridge.jp/kclauncher.apk"
