from django.urls import path
from .views import Dashboard, Chapters, Contents

urlpatterns = [
    path("dashboard/", Dashboard.as_view(), name="dashboard"),
    path("chapters/<int:course_id>/", Chapters.as_view(), name="chapters"),
    path("lessons/content/<int:content_id>", Contents.as_view(), name="Contents"),
]