# Kurageランチャー (kclauncher)

Capacitor製のAndroidアプリ。URLで中身が変わる「Kurageサービス・ランチャー」。
kcaldav.php を指定すればカレンダー、kuragev.php を指定すれば動画、というように、
**開くURL次第でアプリの中身が変わる**汎用WebViewランチャー。

- 起動画面 `www/index.html`: Kurageサービスのタイル＋「マイリンク」(自分のサーバーURLを追加)
- タイルはアプリ内WebViewで開く(capacitor.config の allowNavigation:["*"])
- パッケージ `jp.exbridge.kclauncher` / 表示名「Kurageランチャー」

## ビルド
要: Node 20 / JDK21 / Android SDK(~/.bubblewrap) / 署名鍵(android-keys, .env)
```
bash scripts/build_android.sh   # AAB(Play用)とAPK(直接配布)を署名生成
```
配布APK: https://exbridge.jp/cal/kclauncher.apk

## 既知の制限
- 動画の全画面再生はWebChromeClient未対応(インライン再生は可)。今後の課題
- iOSはMac必須のため未ビルド(iPhoneは各サービスを「ホーム画面に追加」で代替)
