#!/usr/bin/env python3
"""Kurage Capacitor Launcher のアプリアイコン案を作る（正規キャラ素材を使用）。"""
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = "/home/kojima/work/kclauncher"
AVATAR = "/home/kojima/work/kurage_web/images/kurage-ecosystem-avatar.png"
OUT = ROOT + "/outputs"

CYAN = (11, 145, 167)
INDIGO = (47, 107, 216)
NAVY = (14, 33, 63)
MINT = (222, 246, 246)


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def diag_gradient(size, c1, c2):
    n = size
    xx, yy = np.meshgrid(np.linspace(0, 1, n), np.linspace(0, 1, n))
    t = (xx + yy) / 2.0
    arr = np.zeros((n, n, 3), np.uint8)
    for i in range(3):
        arr[..., i] = (c1[i] + (c2[i] - c1[i]) * t).astype(np.uint8)
    return Image.fromarray(arr, "RGB")


def radial_gradient(size, cin, cout):
    n = size
    xx, yy = np.meshgrid(np.linspace(-1, 1, n), np.linspace(-1, 1, n))
    r = np.clip(np.sqrt(xx ** 2 + yy ** 2), 0, 1)
    arr = np.zeros((n, n, 3), np.uint8)
    for i in range(3):
        arr[..., i] = (cin[i] + (cout[i] - cin[i]) * r).astype(np.uint8)
    return Image.fromarray(arr, "RGB")


def bubbles(img, seed=1, n=26, light=True):
    rng = np.random.default_rng(seed)
    d = ImageDraw.Draw(img, "RGBA")
    S = img.size[0]
    col = (255, 255, 255) if light else (180, 230, 240)
    for _ in range(n):
        x, y = rng.uniform(0, S), rng.uniform(0, S)
        r = rng.uniform(S * 0.006, S * 0.03)
        a = int(rng.uniform(30, 90))
        d.ellipse([x - r, y - r, x + r, y + r], fill=col + (a,))
    return img


def head(scale_w):
    av = Image.open(AVATAR).convert("RGBA")
    crop = av.crop((0, 45, 760, 545))          # 頭+クラゲ帽子+肩
    crop = crop.crop(crop.getbbox())
    w = int(scale_w)
    h = int(crop.height * w / crop.width)
    return crop.resize((w, h), Image.LANCZOS)


def compose(size, bg, seed, light, head_frac=0.82, drop=True):
    ic = bg.convert("RGBA")
    ic = bubbles(ic, seed=seed, light=light)
    hd = head(size * head_frac)
    x = (size - hd.width) // 2
    y = int(size * 0.13)                        # 上寄せ（頭がアイコンの主役）
    if drop:
        sh = Image.new("RGBA", ic.size, (0, 0, 0, 0))
        sh.paste((10, 30, 50, 120), (x, y + 10), hd.split()[3])
        sh = sh.filter(ImageFilter.GaussianBlur(14))
        ic = Image.alpha_composite(ic, sh)
    ic.paste(hd, (x, y), hd)
    return ic


def rounded(img, rad_frac=0.225):
    S = img.size[0]
    r = int(S * rad_frac)
    m = Image.new("L", img.size, 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, S, S], radius=r, fill=255)
    out = img.copy()
    out.putalpha(m)
    return out


S = 1024
# 案A: ブランド・グラデ（昼）
a = compose(S, diag_gradient(S, CYAN, INDIGO), seed=3, light=True)
# 案B: ミント・ソフト（白背景に映える）
b_bg = radial_gradient(S, MINT, (150, 205, 220))
b = compose(S, b_bg, seed=7, light=True)
draw = ImageDraw.Draw(b, "RGBA")
draw.ellipse([S*0.045, S*0.045, S*0.955, S*0.955], outline=CYAN + (255,), width=int(S*0.02))
# 案C: ナイト（深い藍→シアン）
c = compose(S, diag_gradient(S, NAVY, CYAN), seed=11, light=False)

for name, im in [("a", a), ("b", b), ("c", c)]:
    im.convert("RGB").save(f"{OUT}/icon_{name}_1024.png")
    rounded(im).save(f"{OUT}/icon_{name}_rounded.png")

# ---- 提案シート ----
Wd, Hd = 1240, 1180
sheet = Image.new("RGB", (Wd, Hd), "#f2f6f8")
ds = ImageDraw.Draw(sheet)
bold = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
blk = "/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc"
f_h = ImageFont.truetype(blk, 44)
f_l = ImageFont.truetype(bold, 26)
f_s = ImageFont.truetype(bold, 20)
ds.text((60, 40), "Kurage Capacitor Launcher — アイコン案", font=f_h, fill="#17324d")
ds.text((60, 96), "正規Kurageキャラ（クラゲ少女）を使用。丸角はスマホのホーム画面での見え方。", font=f_s, fill="#64788a")

labels = [("案A  ブランド・グラデ", a), ("案B  ミント・リング", b), ("案C  ナイト", c)]
x0, gap, isz = 70, 60, 300
for i, (lab, im) in enumerate(labels):
    x = x0 + i * (isz + gap)
    y = 170
    r = rounded(im).resize((isz, isz), Image.LANCZOS)
    # ソフトな影
    sh = Image.new("RGBA", sheet.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle([x+6, y+12, x+isz+6, y+isz+12], radius=int(isz*0.225), fill=(20, 50, 70, 70))
    sheet.paste(Image.alpha_composite(sheet.convert("RGBA"), sh.filter(ImageFilter.GaussianBlur(10))).convert("RGB"), (0, 0))
    sheet.paste(r, (x, y), r)
    ds.text((x + 4, y + isz + 16), lab, font=f_l, fill="#17324d")

# ホーム画面プレビュー（案Aを他アイコンと並べる）
py = 700
ds.text((70, py - 44), "ホーム画面での見え方（案A）", font=f_l, fill="#17324d")
ds.rounded_rectangle([60, py, Wd - 60, py + 360], radius=28, fill="#dfeaf2")
demo = [("#0b91a7", "電話"), ("#e67e22", "写真"), ("#2f6bd8", "地図"), ("#27ae60", "LINE")]
isz2 = 150
ax = 110
ay = py + 60
ka = rounded(a).resize((isz2, isz2), Image.LANCZOS)
sheet.paste(ka, (ax, ay), ka)
ds.text((ax + 8, ay + isz2 + 8), "Kurage", font=f_s, fill="#17324d")
for j, (col, nm) in enumerate(demo):
    x = ax + (j + 1) * (isz2 + 46)
    ic = Image.new("RGB", (isz2, isz2), col)
    sheet.paste(rounded(ic.convert("RGBA")).resize((isz2, isz2)), (x, ay), rounded(ic.convert("RGBA")).resize((isz2, isz2)))
    ds.text((x + 8, ay + isz2 + 8), nm, font=f_s, fill="#4a5c6a")
ds.text((110, ay + isz2 + 60), "※ 丸クラゲの帽子＋青い瞳で、小さくても『Kurage』と分かる想定", font=f_s, fill="#64788a")

sheet.save(f"{OUT}/icon-proposals.png")
print("done:", f"{OUT}/icon-proposals.png")
