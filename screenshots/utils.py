from urllib.parse import urlsplit

from playwright.sync_api import sync_playwright


def take_screenshot(url, full_page=True):
    if urlsplit(url).scheme not in {"http", "https"}:
        raise ValueError("Only HTTP and HTTPS URLs are supported.")

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        try:
            page = browser.new_page(viewport={"width": 1280, "height": 800})
            page.set_default_timeout(30_000)
            response = page.goto(url, wait_until="load")
            if response is not None and response.status >= 400:
                raise ValueError(f"Website returned HTTP {response.status}.")
            image = page.screenshot(full_page=full_page, type="png")
        finally:
            browser.close()

    return image
