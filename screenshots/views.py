from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods
from django_tables2 import RequestConfig

from .forms import ScreenshotForm
from .models import STATUS_FAILED, Screenshot
from .tables import ScreenshotTable


@require_http_methods(["GET", "POST"])
def index_view(request):
    form = ScreenshotForm(request.POST if request.method == "POST" else None)

    if request.method == "POST" and form.is_valid():
        screenshot = form.save(commit=False)
        screenshot.status = STATUS_FAILED
        screenshot.save()
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
