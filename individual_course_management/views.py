from typing import Any
from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.views.generic import TemplateView
from .models import Strike, Enrolment, RoleAssignment
from .models import Course, CourseEnroll, Chapter, ChapterComplete, Lesson, Content, ContentComplete, Template, Quiz, QuizSubmit, ShortQuiz, ShortQuizSubmit
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
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
        enrolment = Enrolment.objects.filter(role_assignment__user=self.request.user, course_enroll__course=course_id).select_related('role_assignment','course_enroll__course__course_group').first()
        if not enrolment:
            return { 'course':''}
        
        chapters = Chapter.objects.filter(course=enrolment.course_enroll.course).select_related('course').order_by('index')
        
        # find first content related to each lesson and chapter        
        first_contents = list(Content.objects.filter(lesson__chapter__in=chapters).select_related('lesson').distinct('lesson__chapter'))
        first_chapter = chapters.first()
        
        # find last completed chapter
        last_completed_chapter = ChapterComplete.objects.filter(enrolment=enrolment).select_related('enrolment').last()
        
        # Find the next chapter after the last completed chapter
        if last_completed_chapter: 
            next_chapter = chapters.filter(index__gt=last_completed_chapter.chapter.index).order_by('index').first()
        else:
            next_chapter = first_chapter

        context = {
            'course': enrolment.course_enroll.course,
            'last_completed_chapter': last_completed_chapter,
            'active_chapter': next_chapter,
            'first_contents': first_contents
        }
        return context
    
class Contents(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return render(request, "individual_course_management/lesson/lesson.html", context)
    
    def get_context_data(self, **kwargs):
        content_id = self.kwargs.get('content_id')
        content = Content.objects.filter(id=content_id).first()

        # List of related Contents for handle paginator
        contents = Content.objects.filter(lesson=content.lesson).select_related('lesson')
        paginator = Paginator(contents, per_page=1)
        page_obj = paginator.get_page(content.index)
        
        context = {
            'page_obj': page_obj,
            # 'content': page_obj.object_list[0],
            'content': content,
        }
        return context