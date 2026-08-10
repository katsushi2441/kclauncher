#!/usr/bin/env bash
# Kurageランチャーの AAB/APK をビルド・署名する。
# 要: Node20 / ~/jdks の JDK21 / ~/.bubblewrap の Android SDK / android-keys + .env
set -euo pipefail
cd "$(dirname "$0")/.."
set -a; . ./.env; set +a
export JAVA_HOME="$HOME/jdks/$(ls "$HOME/jdks" | grep -m1 jdk-21)"
export ANDROID_HOME="$HOME/.bubblewrap/android_sdk"
export PATH="$JAVA_HOME/bin:$PATH"
npx cap sync android
cd android
./gradlew bundleRelease assembleRelease --no-daemon
BT="$(ls -d "$ANDROID_HOME"/build-tools/* | sort -V | tail -1)"
VN="1.0.0"
cp app/build/outputs/bundle/release/app-release.aab "../outputs/kclauncher-$VN.aab"
jarsigner -keystore ../android-keys/kclauncher.jks -storepass "$ANDROID_KEYSTORE_PASSWORD" -keypass "$ANDROID_KEYSTORE_PASSWORD" \
  -sigalg SHA256withRSA -digestalg SHA-256 "../outputs/kclauncher-$VN.aab" kclauncher
"$BT/zipalign" -f 4 app/build/outputs/apk/release/app-release-unsigned.apk aligned.apk
"$BT/apksigner" sign --ks ../android-keys/kclauncher.jks --ks-pass "pass:$ANDROID_KEYSTORE_PASSWORD" \
  --key-pass "pass:$ANDROID_KEYSTORE_PASSWORD" --out "../outputs/kclauncher-$VN.apk" aligned.apk
rm -f aligned.apk
echo "built: outputs/kclauncher-$VN.aab / outputs/kclauncher-$VN.apk"
