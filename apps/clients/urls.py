from django.urls import path
from .views import MyProjectsView

urlpatterns = [
    path("my-projects/", MyProjectsView.as_view(), name="my-projects"),
]
