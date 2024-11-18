from django.http.response import HttpResponse as HttpResponse
from django.views.generic import TemplateView
from .models import Strike, Enrolment, RoleAssignment
from .models import Course, CourseEnroll, Chapter, ChapterComplete, Lesson, Content, ContentComplete, Template, Quiz, QuizSubmit, ShortQuiz, ShortQuizSubmit
from django.contrib.auth.mixins import LoginRequiredMixin

class Dashboard(LoginRequiredMixin,TemplateView):
    template_name = "individual_course_management/dashboard/dashboard.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        strike = Strike.objects.filter(user=self.request.user, strike_status="active").first()
        role_assignments = RoleAssignment.objects.filter(user=self.request.user)
        enrolments = Enrolment.objects.filter(role_assignment__in=role_assignments).select_related('CourseEnroll', 'CourseEnroll__course')
        
        courses = []
        for enrolment in enrolments:
            courses.append(enrolment.CourseEnroll.course)

        context = {
            'strike': strike,
            'courses': courses,
            'days_of_week': [
                {'name': 'saturday', 'short_name': 'ش'},
                {'name': 'sunday', 'short_name': 'ی'},
                {'name': 'monday', 'short_name': 'د'},
                {'name': 'tuesday', 'short_name': 'س'},
                {'name': 'wednesday', 'short_name': 'چ'},
            ]
        }
        return context