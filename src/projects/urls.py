from django.urls import path

from .views import ProjectCreate

urlpatterns = [
    path("create/", ProjectCreate.as_view(), name="project-list-create"),
]
