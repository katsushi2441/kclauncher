#!/usr/bin/env python3
"""Kurage Capacitor Launcher の画面デザイン案HTMLを生成（キャラ埋め込み）。"""
import base64, pathlib

ROOT = pathlib.Path("/home/kojima/work/kclauncher")
face = base64.b64encode((ROOT / "landing/assets/kurage_avatar_face.webp").read_bytes()).decode()
body = base64.b64encode(pathlib.Path("/home/kojima/work/kurage_web/images/kurage-ecosystem-avatar.png").read_bytes()).decode()
FACE = f"data:image/webp;base64,{face}"
BODY = f"data:image/png;base64,{body}"

# アプリ新着（実名・kappstore台帳より）
apps = [
    ("🗓", "予約・受付", "kreserve", "55,000円"),
    ("🗓", "カレンダー同期", "kcaldav", "55,000円"),
    ("🚀", "アプリランチャー", "kclauncher", "無料"),
    ("🗄", "DB管理", "kdbagent", "デモ"),
    ("🎨", "ロゴ生成", "klogogen", "従量"),
    ("🧾", "請求書発行", "kbilling", "55,000円"),
    ("💳", "決済ページ", "kpaylink", "55,000円"),
    ("🔔", "情報監視", "kcheckit", "55,000円"),
    ("📈", "アクセス解析", "ktrackgeo", "55,000円"),
    ("✉️", "領収書メール", "kinvoice", "55,000円"),
]
# 動画新着（kuragev・キャラサムネ）
vids = [
    "AI OSSを2分で解説", "新機能デモ", "Kurageの使い方", "今週のアップデート",
    "はじめての予約システム", "kcaldavで同期", "AIで業務自動化", "ロゴを作ってみた",
    "決済ページの作り方", "アプリランチャー紹介",
]

app_cards = "\n".join(
    f'<a class="pcard"><span class="pth">{e}</span><b>{n}</b><small>{s}</small><span class="pp">{p}</span></a>'
    for e, n, s, p in apps
)
vid_cards = "\n".join(
    f'<a class="vcard"><span class="vth"><img src="{FACE}"><span class="play">▶</span></span><b>{t}</b><small>kuragev</small></a>'
    for t in vids
)

tiles = [
    ("🗓", "カレンダー", "kcaldav"),
    ("🎬", "Kurage動画", "kuragev"),
    ("🔮", "タロット占い", "ゲーム"),
    ("🧗", "クライミング", "ゲーム"),
]

tile_html = "\n".join(
    f'<a class="tile"><span class="em">{e}</span><b>{n}</b><small>{s}</small></a>'
    for e, n, s in tiles
)

HTML = f"""<!doctype html><html lang="ja"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:-apple-system,"Hiragino Sans","Noto Sans JP",sans-serif;background:#eef2f5;color:#22303c;padding-bottom:26px}}
header{{background:linear-gradient(120deg,#0b91a7,#2f6bd8);color:#fff;padding:14px 16px 16px;display:flex;align-items:center;gap:11px}}
header .av{{width:44px;height:44px;border-radius:50%;border:2px solid rgba(255,255,255,.85);object-fit:cover;background:#fff}}
header .ttl{{font-weight:900;font-size:17px;line-height:1.15}}
header .sub{{font-size:11px;opacity:.9;font-weight:600}}
main{{padding:14px 14px 0}}
.hero{{position:relative;background:linear-gradient(180deg,#ffffff,#f3fbfd);border:1px solid #dbe6ee;border-radius:18px;
  padding:16px 130px 16px 16px;margin-bottom:16px;min-height:112px;overflow:hidden;box-shadow:0 8px 20px rgba(20,40,60,.05)}}
.hero h2{{font-size:16px;color:#17324d;font-weight:900;margin-bottom:4px}}
.hero p{{font-size:12px;color:#5a6b7a;line-height:1.5}}
.hero img{{position:absolute;right:-6px;bottom:-14px;width:150px;filter:drop-shadow(0 6px 12px rgba(20,60,80,.18))}}
.grid{{display:grid;grid-template-columns:1fr 1fr;gap:11px;margin-bottom:20px}}
.tile{{display:flex;flex-direction:column;gap:2px;min-height:96px;background:#fff;border:1px solid #dbe3ea;border-radius:16px;
  padding:13px;text-decoration:none;color:#22303c;box-shadow:0 6px 14px rgba(20,40,60,.05)}}
.tile .em{{font-size:28px}}
.tile b{{font-size:14px;margin-top:auto}}
.tile small{{color:#8394a1;font-size:10.5px}}
.sec{{display:flex;align-items:baseline;justify-content:space-between;margin:0 2px 9px}}
.sec h3{{font-size:15px;font-weight:900;color:#17324d;display:flex;align-items:center;gap:7px}}
.sec h3 .tag{{font-size:10px;font-weight:800;color:#0b91a7;background:#e2f5f8;border-radius:6px;padding:2px 7px}}
.sec .more{{font-size:11.5px;color:#2f6bd8;font-weight:800;text-decoration:none}}
.hint{{font-size:10.5px;color:#9aa8b5;margin:0 2px 8px}}
/* 横スクロール・2段シェルフ */
.shelf{{display:grid;grid-auto-flow:column;grid-template-rows:repeat(2,auto);gap:10px;
  overflow-x:auto;padding:2px 14px 14px;margin:0 -14px;scroll-snap-type:x proximity;-webkit-overflow-scrolling:touch}}
.shelf::-webkit-scrollbar{{height:0}}
.pcard{{width:128px;background:#fff;border:1px solid #dbe3ea;border-radius:14px;padding:10px;text-decoration:none;color:#22303c;
  scroll-snap-align:start;box-shadow:0 5px 12px rgba(20,40,60,.05);display:flex;flex-direction:column;gap:2px}}
.pcard .pth{{height:56px;border-radius:10px;background:linear-gradient(135deg,#eaf6f8,#e6edfb);display:grid;place-items:center;font-size:26px;margin-bottom:5px}}
.pcard b{{font-size:12.5px}}
.pcard small{{color:#93a2af;font-size:10px}}
.pcard .pp{{font-size:11px;font-weight:800;color:#16805f;margin-top:2px}}
.vcard{{width:158px;background:#fff;border:1px solid #dbe3ea;border-radius:14px;padding:8px;text-decoration:none;color:#22303c;
  scroll-snap-align:start;box-shadow:0 5px 12px rgba(20,40,60,.05)}}
.vcard .vth{{position:relative;display:block;height:90px;border-radius:10px;overflow:hidden;background:#cfe8ee;margin-bottom:6px}}
.vcard .vth img{{width:100%;height:100%;object-fit:cover;object-position:50% 22%}}
.vcard .play{{position:absolute;inset:0;margin:auto;width:34px;height:34px;border-radius:50%;background:rgba(0,0,0,.45);
  color:#fff;display:grid;place-items:center;font-size:13px}}
.vcard b{{font-size:12px;display:block;padding:0 2px;line-height:1.3}}
.vcard small{{color:#93a2af;font-size:10px;padding:0 2px}}
.edge{{position:relative}}
.edge::after{{content:"";position:absolute;top:0;right:0;bottom:14px;width:34px;
  background:linear-gradient(90deg,rgba(238,242,245,0),#eef2f5);pointer-events:none}}
</style></head>
<body>
<header>
  <img class="av" src="{FACE}">
  <div><div class="ttl">Kurage Capacitor Launcher</div><div class="sub">Kurageのサービスをホーム画面から</div></div>
</header>
<main>
  <div class="hero">
    <h2>こんにちは、Kurage です🪼</h2>
    <p>カレンダー・動画・ゲーム・新着アプリを、<br>タイルから1タップで開けます。</p>
    <img src="{BODY}">
  </div>

  <div class="grid">
    {tile_html}
    <a class="tile" style="grid-column:1/3;flex-direction:row;align-items:center;gap:12px;min-height:auto">
      <span class="em">➕</span><b style="margin:0">リンクを追加</b>
      <small style="margin-left:auto">自分のカレンダーURLも</small>
    </a>
  </div>

  <div class="sec"><h3>アプリ新着 <span class="tag">Kurage App Store</span></h3><a class="more" href="#">すべて →</a></div>
  <p class="hint">← 横スクロールで10件（2段）／初期表示3件 →</p>
  <div class="edge"><div class="shelf">{app_cards}</div></div>

  <div class="sec" style="margin-top:18px"><h3>動画新着 <span class="tag">kuragev</span></h3><a class="more" href="#">すべて →</a></div>
  <p class="hint">← 横スクロールで10件（2段）／初期表示3件 →</p>
  <div class="edge"><div class="shelf">{vid_cards}</div></div>
</main>
</body></html>"""

(ROOT / "design/mockup.html").write_text(HTML, encoding="utf-8")
print("wrote design/mockup.html")
