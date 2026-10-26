from django.contrib import admin
from django.urls import include, path

from catalog.views import health


urlpatterns = [
    path("admin/", admin.site.urls),
    path("health/", health, name="health"),
    path("accounts/", include("accounts.urls")),
    path("", include("catalog.urls")),
]
