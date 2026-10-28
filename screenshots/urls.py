from django.urls import path

from . import views

urlpatterns = [
    path("", views.index_view, name="index"),
    path("screenshots/<int:pk>/status/", views.status_view, name="status"),
]
