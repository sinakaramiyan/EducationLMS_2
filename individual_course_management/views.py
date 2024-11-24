from django.http.response import HttpResponse as HttpResponse
from django.views.generic import TemplateView
from .models import Strike, Enrolment, RoleAssignment
from .models import Course, CourseEnroll, Chapter, ChapterComplete, Lesson, Content, ContentComplete, Template, Quiz, QuizSubmit, ShortQuiz, ShortQuizSubmit
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import render
from django.views.generic import View
from django.urls import reverse

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
        if self.get_context_data(**kwargs)['course']:
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
        
        templates = Template.objects.filter(content=content_id).select_related('content').order_by('index')

        first_uncomplete_template = None
        next_first_uncomplete_template = None

        for template in templates:
            if template.completed == False:
                first_uncomplete_template = template
                next_first_uncomplete_template = Template.objects.filter(content=template.content, index=first_uncomplete_template.index+1).first()
                break
        
        context = {
            'page_obj': page_obj,
            # 'content': page_obj.object_list[0],
            'content': content,
            'templates': templates,
            'first_uncomplete_template': first_uncomplete_template,
            'next_first_uncomplete_template': next_first_uncomplete_template
        }

        # Show next content button in template
        if templates.last():
            all_templates_completed = templates.last().completed
            context.update({
                'all_templates_completed': all_templates_completed
            })
        return context
    
class Templates(LoginRequiredMixin, TemplateView):
    
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if self.get_context_data(**kwargs)['type'] == 'quiz':
            template_name = "individual_course_management/template/quiz.html"
        elif self.get_context_data(**kwargs)['type'] == 'shortquiz':
            template_name = "individual_course_management/template/short_quiz.html"
        else:
            template_name = 'individual_course_management/template/text_book.html'
        
        return render(request, template_name, context)
    
    def get_context_data(self, **kwargs):
        template_id = self.kwargs.get('template_id')
        template = Template.objects.filter(id=template_id).first()
        enrolment = Enrolment.objects.filter(role_assignment__user=self.request.user, course_enroll__course=template.content.lesson.chapter.course).select_related('role_assignment','course_enroll__course__course_group').first()

        context = {
            'template': template,
            'type': template.type,
        }
        next_template = Template.objects.filter(content=template.content, index=template.index+1).select_related('content').first()
        if next_template:
            context.update({
                'next_template': next_template,
            })
        else:
            next_content = Content.objects.filter(lesson=template.content.lesson, index=template.content.index+1).select_related('lesson').first()
            if next_content:
                context.update({
                    'next_content': next_content
                })
        
        if template.type == 'quiz':
            quiz = Quiz.objects.filter(template=template_id).select_related('template').first()
            quiz_completed = QuizSubmit.objects.filter(quiz=quiz, enrolment=enrolment).select_related('quiz', 'enrolment').first()
            context.update({
                'quiz': quiz,
                'quiz_completed': quiz_completed
            })
        elif template.type == 'shortquiz':
            short_quiz = ShortQuiz.objects.filter(template=template_id).select_related('template').first()
            short_quiz_completed = ShortQuizSubmit.objects.filter(short_quiz=short_quiz, enrolment=enrolment).select_related('short_quiz', 'enrolment').first()
            context.update({
                'short_quiz': short_quiz,
                'short_quiz_completed': short_quiz_completed
            })

        return context

class TextBookComplited(View):
    def post(self, request, *args, **kwargs):
        template_id = request.POST.get('template_id')
        template = Template.objects.filter(id=template_id).first()
        next_template = Template.objects.filter(content=template.content, index=template.index+1).select_related('content').first()

        template.completed = True
        template.save()

        html_response = ''
        if next_template:
            next_template_url = reverse("templates", args=[next_template.id])
            html_response += (
                '<div class="flex justify-end border-y py-4 w-full">'
                f'<a hx-get="{next_template_url}" hx-trigger="click" hx-target="#templates" hx-swap="beforeend" hx-on::after-request="this.closest(\'.flex\').remove()" class="w-fit inline-flex items-center px-6 py-2 text-base font-light text-center cursor-pointer border border-blue-500 text-blue-500 bg-white hover:bg-blue-100 focus:ring-2 focus:ring-blue-300">بخش بعد</a>'
                '</div>'
            )
        else:
            next_content = Content.objects.filter(lesson=template.content.lesson, id=template.content.id+1).select_related('lesson').first()
            next_content_url = reverse("Contents", args=[next_content.id])
            html_response += (
                '<div class="flex justify-end w-full border-y py-4">'
                f'<a href="{next_content_url}" class="w-fit inline-flex items-center px-6 py-2 text-base font-light text-center cursor-pointer text-white bg-blue-700 hover:bg-blue-800 focus:ring-2 focus:ring-blue-300">پایان بخش</a>'
                '</div>'
            )

        return HttpResponse(html_response)

class ShortQuizComplited(View):
    def post(self, request, *args, **kwargs):
        answer = request.POST.get('answer')
        short_quiz_id = request.POST.get('short_quiz_id') 
        short_quiz = ShortQuiz.objects.filter(id=short_quiz_id).first()
        enrolment = Enrolment.objects.filter(role_assignment__user=self.request.user, course_enroll__course=short_quiz.template.content.lesson.chapter.course).select_related('role_assignment','course_enroll__course__course_group').first()
        next_template = Template.objects.filter(content=short_quiz.template.content, index=short_quiz.template.index+1).select_related('content').first()

        short_quiz_submit = ShortQuizSubmit(
            short_quiz = short_quiz,
            enrolment = enrolment,
            answer = f'option{answer}',
            is_correct = True if short_quiz.correct_option == f'option{answer}' else False,
        )
        short_quiz_submit.save()

        template = Template.objects.get(id=short_quiz.template.id)
        template.completed = True
        template.save()
            
        html_response = ''
        if f'option{answer}' == short_quiz.correct_option:
            if short_quiz.correct_option == 'option1':
                html_response = f'<div class="border border-zinc-300 p-1 select-none" style="background-color: green">{short_quiz.option1}</div>' + f'<div class="border border-zinc-300 p-1 select-none">{short_quiz.option2}</div>'
            else:
                html_response = f'<div class="border border-zinc-300 p-1 select-none">{short_quiz.option1}</div>' + f'<div class="border border-zinc-300 p-1 select-none" style="background-color: green">{short_quiz.option2}</div>'
        else:
            if short_quiz.correct_option == 'option1':
                html_response = f'<div class="border border-zinc-300 p-1 select-none">{short_quiz.option1}</div>' + f'<div class="border border-zinc-300 p-1 select-none" style="background-color: red">{short_quiz.option2}</div>'
            else:
                html_response = f'<div class="border border-zinc-300 p-1 select-none" style="background-color: red">{short_quiz.option1}</div>' + f'<div class="border border-zinc-300 p-1 select-none">{short_quiz.option2}</div>'
        if next_template:
            next_template_url = reverse("templates", args=[next_template.id])
            html_response += (
                '<div class="flex justify-end border-y py-4 w-full">'
                f'<a hx-get="{next_template_url}" hx-trigger="click" hx-target="#templates" hx-swap="beforeend" hx-on::after-request="this.closest(\'.flex\').remove()" class="w-fit inline-flex items-center px-6 py-2 text-base font-light text-center cursor-pointer border border-blue-500 text-blue-500 bg-white hover:bg-blue-100 focus:ring-2 focus:ring-blue-300">بخش بعد</a>'
                '</div>'
            )
        else:
            next_content = Content.objects.filter(lesson=short_quiz.template.content.lesson, id=short_quiz.template.content.id+1).select_related('lesson').first()
            next_content_url = reverse("Contents", args=[next_content.id])
            html_response += (
                '<div class="flex justify-end w-full border-y py-4">'
                f'<a href="{next_content_url}" class="w-fit inline-flex items-center px-6 py-2 text-base font-light text-center cursor-pointer text-white bg-blue-700 hover:bg-blue-800 focus:ring-2 focus:ring-blue-300">پایان بخش</a>'
                '</div>'
            )

        return HttpResponse(html_response)
    
class QuizComplited(View):
    def post(self, request, *args, **kwargs):
        answer = request.POST.get('answer')
        quiz_id = request.POST.get('quiz_id')
        
        quiz = Quiz.objects.filter(id=quiz_id).first()
        enrolment = Enrolment.objects.filter(role_assignment__user=self.request.user, course_enroll__course=quiz.template.content.lesson.chapter.course).select_related('role_assignment','course_enroll__course__course_group').first()
        next_template = Template.objects.filter(content=quiz.template.content, index=quiz.template.index+1).select_related('content').first()
        quiz_submit = QuizSubmit(
            quiz = quiz,
            enrolment = enrolment,
            answer = f'option{answer}',
            is_correct = True if quiz.correct_option == f'option{answer}' else False,
        )
        quiz_submit.save()

        template = Template.objects.get(id=quiz.template.id)
        template.completed = True
        template.save()
            
        html_response = ''
        if f'option{answer}' == 'option1':
            html_response = f'<li class="flex items-center gap-4"><input type="checkbox" class="w-5 h-5" disabled="" checked  /><span>{quiz.option1}</span></li><li class="flex items-center gap-4"><input type="checkbox" class="w-5 h-5" disabled=""  /><span>{quiz.option2}</span></li><li class="flex items-center gap-4"><input type="checkbox" class="w-5 h-5" disabled=""  /><span>{quiz.option3}</span></li><li class="flex items-center gap-4"><input type="checkbox" class="w-5 h-5" disabled=""  /><span>{quiz.option4}</span></li>'
        elif f'option{answer}' == 'option2':
            html_response = f'<li class="flex items-center gap-4"><input type="checkbox" class="w-5 h-5" disabled="" /><span>{quiz.option1}</span></li><li class="flex items-center gap-4"><input type="checkbox" class="w-5 h-5" disabled="" checked /><span>{quiz.option2}</span></li><li class="flex items-center gap-4"><input type="checkbox" class="w-5 h-5" disabled=""  /><span>{quiz.option3}</span></li><li class="flex items-center gap-4"><input type="checkbox" class="w-5 h-5" disabled=""  /><span>{quiz.option4}</span></li>'
        elif f'option{answer}' == 'option3':
            html_response = f'<li class="flex items-center gap-4"><input type="checkbox" class="w-5 h-5" disabled="" /><span>{quiz.option1}</span></li><li class="flex items-center gap-4"><input type="checkbox" class="w-5 h-5" disabled=""  /><span>{quiz.option2}</span></li><li class="flex items-center gap-4"><input type="checkbox" class="w-5 h-5" disabled="" checked /><span>{quiz.option3}</span></li><li class="flex items-center gap-4"><input type="checkbox" class="w-5 h-5" disabled=""  /><span>{quiz.option4}</span></li>'
        elif f'option{answer}' == 'option4':
            html_response = f'<li class="flex items-center gap-4"><input type="checkbox" class="w-5 h-5" disabled="" /><span>{quiz.option1}</span></li><li class="flex items-center gap-4"><input type="checkbox" class="w-5 h-5" disabled=""  /><span>{quiz.option2}</span></li><li class="flex items-center gap-4"><input type="checkbox" class="w-5 h-5" disabled=""  /><span>{quiz.option3}</span></li><li class="flex items-center gap-4"><input type="checkbox" class="w-5 h-5" disabled="" checked /><span>{quiz.option4}</span></li>'


        if f'option{answer}' == quiz.correct_option:
            html_response += f'<div class="flex justify-between w-full"><div class="flex gap-2"><span class="font-bold">درست</span></div><div class="p-1 text-sm bg-blue-200">{quiz.score}</div></div>'
        else: 
            html_response += f'<div class="flex justify-between w-full"><div class="flex gap-2"><span class="font-bold text-red-700">غلط</span></div></div>'

        if next_template:
            next_template_url = reverse("templates", args=[next_template.id])
            html_response += (
                '<div class="flex justify-end border-y py-4 w-full">'
                f'<a hx-get="{next_template_url}" hx-trigger="click" hx-target="#templates" hx-swap="beforeend" hx-on::after-request="this.closest(\'.flex\').remove()" class="w-fit inline-flex items-center px-6 py-2 text-base font-light text-center cursor-pointer border border-blue-500 text-blue-500 bg-white hover:bg-blue-100 focus:ring-2 focus:ring-blue-300">بخش بعد</a>'
                '</div>'
            )
        else:
            next_content = Content.objects.filter(lesson=quiz.template.content.lesson, id=quiz.template.content.id+1).select_related('lesson').first()
            next_content_url = reverse("Contents", args=[next_content.id])
            html_response += (
                '<div class="flex justify-end w-full py-4 mt-2">'
                f'<a href="{next_content_url}" class="w-fit inline-flex items-center px-6 py-2 text-base font-light text-center cursor-pointer text-white bg-blue-700 hover:bg-blue-800 focus:ring-2 focus:ring-blue-300">پایان بخش</a>'
                '</div>'
            )

        return HttpResponse(html_response)