from urllib.parse import urlsplit
from uuid import uuid4

from celery import shared_task
from django.core.files.base import ContentFile
from django.utils import timezone
from playwright.sync_api import sync_playwright

from .models import STATUS_FAILED, STATUS_SUCCESS, Screenshot


@shared_task
def capture_screenshot(screenshot_id, url, full_page=False):
    screenshot = Screenshot.objects.get(pk=screenshot_id)

    try:
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

        screenshot.file.save(f"{uuid4()}.png", ContentFile(image), save=False)
        screenshot.status = STATUS_SUCCESS
        screenshot.save(update_fields=["file", "status", "updated_at"])
    except Exception:
        Screenshot.objects.filter(pk=screenshot_id).update(
            status=STATUS_FAILED, updated_at=timezone.now()
        )
        # Raising also marks the Celery task as FAILURE instead of SUCCESS.
        raise

    return screenshot.file.name
