from django.urls import path
from .views import Dashboard, Chapters

urlpatterns = [
    path("dashboard/", Dashboard.as_view(), name="dashboard"),
    path("<str:course_name>-<int:course_id>/", Chapters.as_view(), name="chapters"),
]