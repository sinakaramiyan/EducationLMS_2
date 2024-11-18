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
    
class Chapters(LoginRequiredMixin, TemplateView):
    template_name = "individual_course_management/chapter/chapter.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # description partial page
        # get course based on selected course in dashboard
        course_id = self.kwargs.get('course_id')
        course = Course.objects.filter(id=course_id).first()

        # steps parital page
        chapters = Chapter.objects.filter(course=course).order_by('index')
        first_chapter = chapters.first()

        # find last completed chapter
        role_assignment = RoleAssignment.objects.filter(user=self.request.user)
        enrolments = Enrolment.objects.filter(role_assignment__in=role_assignment)
        last_completed_chapter = ChapterComplete.objects.filter(enrolment__in=enrolments).last()
        
        # Find the next chapter after the last completed chapter
        if last_completed_chapter: 
            last_completed_chapter_instance = last_completed_chapter.chapter
            next_chapter = None
            for chapter in chapters:
                if chapter.index > last_completed_chapter_instance.index:
                    next_chapter = chapter
                    break
        else:
            next_chapter = first_chapter

        context = {
            'course': course,
            'course_group_title': course.course_group.title,
            'chapters': chapters,
            'first_chapter': first_chapter,
            'last_chapter': chapters.last(),
            'last_completed_chapter': last_completed_chapter,
            'active_chapter': next_chapter,
        }
        return context