from django.db import models

TYPE_VIEWPORT = "VP"
TYPE_FULL_PAGE = "FP"
TYPE_CHOICES = {
    TYPE_VIEWPORT: "Viewport",
    TYPE_FULL_PAGE: "Full page",
}

STATUS_PENDING = "PE"
STATUS_SUCCESS = "SU"
STATUS_FAILED = "FA"
STATUS_CHOICES = {
    STATUS_PENDING: "PENDING",
    STATUS_SUCCESS: "SUCCESS",
    STATUS_FAILED: "FAILED",
}


class Screenshot(models.Model):
    url = models.URLField()
    type = models.CharField(max_length=2, choices=TYPE_CHOICES, default=TYPE_VIEWPORT)
    file = models.ImageField(upload_to="screenshots/", null=True, blank=True, default=None)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default=STATUS_PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.url
