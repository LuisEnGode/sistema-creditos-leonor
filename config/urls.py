from django.contrib import admin
from django.urls import path

from apps.core import views
from config.api import api

urlpatterns = [
    path("", views.home, name="home"),
    path("htmx/test/", views.htmx_test, name="htmx_test"),
    path("admin/", admin.site.urls),
    path("api/", api.urls),
]
