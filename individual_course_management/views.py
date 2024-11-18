from typing import Any
from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.views.generic import TemplateView
from .models import Strike, Enrolment, RoleAssignment
from .models import Course, CourseEnroll, Chapter, ChapterComplete, Lesson, Content, ContentComplete, Template, Quiz, QuizSubmit, ShortQuiz, ShortQuizSubmit
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render

class Dashboard(LoginRequiredMixin,TemplateView):
    template_name = "individual_course_management/dashboard/dashboard.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        strike = Strike.objects.filter(user=self.request.user, strike_status="active").first()
        role_assignments = RoleAssignment.objects.filter(user=self.request.user)
        enrolments = Enrolment.objects.filter(role_assignment__in=role_assignments)
        courses = []
        for enrolment in enrolments:
            courses.append(enrolment.course_enroll.course)

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
    
    def get(self, request, *args, **kwargs):
        if (self.get_context_data(**kwargs)['course']):
            context = self.get_context_data(**kwargs)
            return render(request, "individual_course_management/chapter/chapter.html", context)
        else: 
            return HttpResponse("This page doesn't exist")
        
    def get_context_data(self, **kwargs):        
        # get course based on selected course in dashboard
        course_id = self.kwargs.get('course_id')
        enrolment = Enrolment.objects.filter(role_assignment__user=self.request.user, course_enroll__course=course_id).select_related('role_assignment','course_enroll', 'course_enroll__course', 'course_enroll__course__course_group').first()
        if not enrolment:
            return { 'course':''}
        
        # steps parital page
        chapters = Chapter.objects.filter(course=enrolment.course_enroll.course).order_by('index').select_related('course')
        first_chapter = chapters.first()
        last_chapter = chapters.last()

        # find last completed chapter
        last_completed_chapter = ChapterComplete.objects.filter(enrolment=enrolment).last()
        
        # Find the next chapter after the last completed chapter
        if last_completed_chapter: 
            next_chapter = Chapter.objects.filter(course=enrolment.course_enroll.course, index__gt=last_completed_chapter.chapter.index).order_by('index').first()
        else:
            next_chapter = first_chapter

        context = {
            'course': enrolment.course_enroll.course,
            'course_group_title': enrolment.course_enroll.course.course_group.title,
            'chapters': chapters,
            'first_chapter': first_chapter,
            'last_chapter': last_chapter,
            'last_completed_chapter': last_completed_chapter,
            'active_chapter': next_chapter,
        }
        return context
    
