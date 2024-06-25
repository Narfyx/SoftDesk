from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("user/", include("users.urls")),
    path("project/", include("projects.urls")),
    path("issues/", include("issues.urls")),
]
