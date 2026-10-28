import logging

from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_http_methods
from django_tables2 import RequestConfig
from kombu.exceptions import OperationalError

from .forms import ScreenshotForm
from .models import STATUS_FAILED, TYPE_FULL_PAGE, Screenshot
from .tables import ScreenshotTable
from .tasks import capture_screenshot

logger = logging.getLogger(__name__)


@require_http_methods(["GET", "POST"])
def index_view(request):
    form = ScreenshotForm(request.POST if request.method == "POST" else None)

    if request.method == "POST" and form.is_valid():
        screenshot = form.save()
        full_page = screenshot.type == TYPE_FULL_PAGE
        try:
            capture_screenshot.delay(screenshot.pk, screenshot.url, full_page=full_page)
        except OperationalError:
            Screenshot.objects.filter(pk=screenshot.pk).update(
                status=STATUS_FAILED, updated_at=timezone.now()
            )
            logger.exception("Could not queue screenshot %s", screenshot.pk)
            messages.error(request, "Could not start the capture. Please try again.")

        return redirect("index")

    table = ScreenshotTable(Screenshot.objects.all())
    RequestConfig(request, paginate={"per_page": 10}).configure(table)
    return render(
        request,
        "screenshots/index.html",
        {
            "form": form,
            "table": table,
        }
    )


@require_http_methods(["GET"])
def status_view(request, pk):
    screenshot = get_object_or_404(Screenshot, pk=pk)
    return JsonResponse(
        {
            "status": screenshot.status,
            "label": screenshot.get_status_display(),
            "file_url": screenshot.file.url if screenshot.file else None,
        }
    )
