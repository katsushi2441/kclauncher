from playwright.sync_api import sync_playwright
import pathlib
url = pathlib.Path("/home/kojima/work/kclauncher/www/index.html").as_uri()
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width":390,"height":844}, device_scale_factor=2)
    pg.goto(url, wait_until="networkidle")
    pg.wait_for_timeout(1500)
    # 新着が入ったか
    apps = pg.eval_on_selector_all("#appShelf .pcard", "els=>els.length")
    vids = pg.eval_on_selector_all("#vidShelf .vcard", "els=>els.length")
    sw = pg.evaluate("document.documentElement.scrollWidth"); vw = pg.evaluate("document.documentElement.clientWidth")
    print(f"  appcards={apps} vidcards={vids} scrollWidth={sw} viewport={vw} {'OK収まる' if sw<=vw+1 else 'NGはみ出し'}")
    pg.screenshot(path="outputs/app-screen.png", full_page=True)
    b.close()
