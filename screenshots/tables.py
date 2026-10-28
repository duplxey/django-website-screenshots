import django_tables2 as tables
from django.urls import reverse

from .models import Screenshot


class ScreenshotTable(tables.Table):
    url = tables.URLColumn(
        verbose_name="Website",
        attrs={
            "a": {
                "target": "_blank",
                "rel": "noopener noreferrer",
                "class": "text-break",
            }
        },
    )
    status = tables.TemplateColumn(template_name="screenshots/columns/status.html")
    file = tables.TemplateColumn(
        template_name="screenshots/columns/file.html",
        verbose_name="Screenshot",
    )
    created_at = tables.DateTimeColumn(
        format="M j, Y, H:i",
        verbose_name="Created",
        attrs={
            "th": {"class": "d-none d-md-table-cell"},
            "td": {"class": "d-none d-md-table-cell text-nowrap"},
        },
    )

    class Meta:
        model = Screenshot
        template_name = "django_tables2/bootstrap5.html"
        fields = ("url", "type", "status", "file", "created_at")
        orderable = False
        attrs = {"class": "table table-hover align-middle mb-0"}
        row_attrs = {
            "data-state": lambda record: record.status,
            "data-status-url": lambda record: reverse("status", args=[record.pk]),
        }
        empty_text = "No screenshots yet. Submit a website to get started."
