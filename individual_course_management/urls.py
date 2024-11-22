from django.urls import path
from .views import Dashboard, Chapters, Contents, Templates

urlpatterns = [
    path("dashboard/", Dashboard.as_view(), name="dashboard"),
    path("chapters/<int:course_id>/", Chapters.as_view(), name="chapters"),
    path("lessons/content/<int:content_id>", Contents.as_view(), name="Contents"),
    path("lessons/content/template/<int:template_id>", Templates.as_view(), name="templates"),
]