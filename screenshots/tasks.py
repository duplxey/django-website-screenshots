from uuid import uuid4

from celery import shared_task
from django.core.files.base import ContentFile
from django.utils import timezone

from .models import STATUS_FAILED, STATUS_SUCCESS, Screenshot
from .utils import take_screenshot


@shared_task
def capture_screenshot(screenshot_id, url, full_page=True):
    screenshot = Screenshot.objects.get(pk=screenshot_id)

    try:
        image = take_screenshot(url, full_page=full_page)
        screenshot.file.save(f"{uuid4()}.png", ContentFile(image), save=False)
        screenshot.status = STATUS_SUCCESS
        screenshot.save(update_fields=["file", "status", "updated_at"])
    except Exception:
        Screenshot.objects.filter(pk=screenshot_id).update(
            status=STATUS_FAILED, updated_at=timezone.now()
        )
        raise

    return screenshot.file.name
