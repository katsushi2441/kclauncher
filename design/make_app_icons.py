#!/usr/bin/env python3
"""アイコンA を全用途に書き出す: PWA(www/assets) と Android適応アイコン(全密度)。"""
import numpy as np, pathlib
from PIL import Image, ImageDraw, ImageFilter

ROOT = pathlib.Path("/home/kojima/work/kclauncher")
AVATAR = "/home/kojima/work/kurage_web/images/kurage-ecosystem-avatar.png"
CYAN, INDIGO = (11, 145, 167), (47, 107, 216)


def diag(size, c1, c2):
    xx, yy = np.meshgrid(np.linspace(0, 1, size), np.linspace(0, 1, size))
    t = (xx + yy) / 2.0
    arr = np.zeros((size, size, 3), np.uint8)
    for i in range(3):
        arr[..., i] = (c1[i] + (c2[i] - c1[i]) * t).astype(np.uint8)
    return Image.fromarray(arr, "RGB").convert("RGBA")


def bubbles(img, seed=3, n=24):
    rng = np.random.default_rng(seed)
    d = ImageDraw.Draw(img, "RGBA")
    S = img.size[0]
    for _ in range(n):
        x, y = rng.uniform(0, S), rng.uniform(0, S)
        r = rng.uniform(S * 0.006, S * 0.03)
        d.ellipse([x - r, y - r, x + r, y + r], fill=(255, 255, 255, int(rng.uniform(30, 85))))
    return img


def head(w):
    av = Image.open(AVATAR).convert("RGBA")
    c = av.crop((0, 45, 760, 545)); c = c.crop(c.getbbox())
    return c.resize((int(w), int(c.height * w / c.width)), Image.LANCZOS)


def full_bleed(S, head_frac=0.82, y_frac=0.13):
    bg = bubbles(diag(S, CYAN, INDIGO), seed=3)
    hd = head(S * head_frac)
    x = (S - hd.width) // 2; y = int(S * y_frac)
    sh = Image.new("RGBA", bg.size, (0, 0, 0, 0))
    sh.paste((10, 30, 50, 120), (x, y + 10), hd.split()[3])
    bg = Image.alpha_composite(bg, sh.filter(ImageFilter.GaussianBlur(int(S*0.014))))
    bg.paste(hd, (x, y), hd)
    return bg


def circle(img):
    S = img.size[0]; m = Image.new("L", img.size, 0)
    ImageDraw.Draw(m).ellipse([0, 0, S, S], fill=255)
    o = img.copy(); o.putalpha(m); return o


def rounded(img, r=0.22):
    S = img.size[0]; m = Image.new("L", img.size, 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, S, S], radius=int(S * r), fill=255)
    o = img.copy(); o.putalpha(m); return o


def maskable(S):
    bg = bubbles(diag(S, CYAN, INDIGO), seed=3)
    hd = head(S * 0.62)               # セーフゾーン内に収める
    x = (S - hd.width) // 2; y = int(S * 0.19)
    bg.paste(hd, (x, y), hd); return bg


def fg_transparent(S):
    canvas = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    hd = head(S * 0.86)
    x = (S - hd.width) // 2; y = int(S * 0.08)
    canvas.paste(hd, (x, y), hd); return canvas


MASTER = full_bleed(1024)
MASTER_BG = bubbles(diag(1024, CYAN, INDIGO), seed=3)
MASTER_FG = fg_transparent(1024)

# ---- PWA (www/assets) ----
wa = ROOT / "www/assets"
MASTER.resize((192, 192), Image.LANCZOS).save(wa / "icon-192.png")
MASTER.resize((512, 512), Image.LANCZOS).save(wa / "icon-512.png")
maskable(512).save(wa / "icon-maskable.png")
print("  PWA icons ->", wa)

# ---- LP/kappstore用の丸角＆マスターも更新 ----
out = ROOT / "outputs"
rounded(MASTER).save(out / "icon_a_rounded.png")
MASTER.convert("RGB").save(out / "icon_a_1024.png")

# ---- Android 適応アイコン(既存ファイルと同じ寸法で上書き) ----
res = ROOT / "android/app/src/main/res"
for d in sorted(res.glob("mipmap-*")):
    for f in d.glob("*.png"):
        w, h = Image.open(f).size
        name = f.name
        if name == "ic_launcher_background.png":
            img = MASTER_BG.resize((w, h), Image.LANCZOS).convert("RGB")
        elif name == "ic_launcher_foreground.png":
            img = MASTER_FG.resize((w, h), Image.LANCZOS)
        elif name == "ic_launcher_round.png":
            img = circle(MASTER).resize((w, h), Image.LANCZOS)
        elif name == "ic_launcher.png":
            img = rounded(MASTER).resize((w, h), Image.LANCZOS)
        else:
            continue
        img.save(f)
print("  Android mipmaps updated")

# 適応アイコンの合成プレビュー(確認用)
prev = Image.alpha_composite(MASTER_BG.copy(), MASTER_FG)
circle(prev).resize((256, 256)).save(out / "android_adaptive_preview.png")
print("done")
