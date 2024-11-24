from django.urls import path
from .views import Dashboard, Chapters, Contents, Templates, ShortQuizComplited

urlpatterns = [
    path("dashboard/", Dashboard.as_view(), name="dashboard"),
    path("chapters/<int:course_id>/", Chapters.as_view(), name="chapters"),
    path("lessons/content/<int:content_id>", Contents.as_view(), name="Contents"),
    path("lessons/content/template/<int:template_id>/", Templates.as_view(), name="templates"),
    path("shortQuizCompleted/", ShortQuizComplited.as_view(), name="shortQuizCompleted")
]