from django import forms

from .models import Screenshot


class ScreenshotForm(forms.ModelForm):
    class Meta:
        model = Screenshot
        fields = ["url", "type"]
        labels = {"url": "Website URL", "type": "Capture mode"}
        widgets = {
            "url": forms.URLInput(attrs={"placeholder": "https://example.com"}),
            "type": forms.RadioSelect,
        }

    def clean_url(self):
        url = self.cleaned_data["url"]
        if not url.lower().startswith(("http://", "https://")):
            raise forms.ValidationError("Enter an HTTP or HTTPS website URL.")
        return url
