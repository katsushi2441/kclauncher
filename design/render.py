from playwright.sync_api import sync_playwright
import pathlib
url = pathlib.Path("/home/kojima/work/kclauncher/design/mockup.html").as_uri()
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width":390,"height":844}, device_scale_factor=2)
    pg.goto(url, wait_until="networkidle")
    pg.screenshot(path="/home/kojima/work/kclauncher/outputs/mockup-screen.png", full_page=True)
    b.close()
print("shot ok")
