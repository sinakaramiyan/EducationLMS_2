# Generated by Django 5.1.2 on 2024-11-18 08:42

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('role_management', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='Id')),
                ('index', models.IntegerField(verbose_name='Index')),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('description', models.TextField(verbose_name='Description')),
                ('next_content', models.BooleanField(default=False, verbose_name='Next Content')),
                ('score', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Score')),
            ],
        ),
        migrations.CreateModel(
            name='CourseGroup',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='Id')),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('description', models.TextField(blank=True, verbose_name='Description')),
                ('start_date', models.DateField(verbose_name='Start Date')),
                ('end_date', models.DateField(null=True, verbose_name='End Date')),
                ('edit_date', models.DateTimeField(auto_now=True, verbose_name='Edit Date')),
                ('visible', models.BooleanField(default=False, verbose_name='Visible')),
                ('enable_completed', models.BooleanField(default=False, verbose_name='Enable Completed')),
            ],
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='Id')),
                ('question', models.TextField(verbose_name='Question')),
                ('option1', models.CharField(max_length=255, verbose_name='Option 1')),
                ('option2', models.CharField(max_length=255, verbose_name='Option 2')),
                ('option3', models.CharField(max_length=255, verbose_name='Option 3')),
                ('option4', models.CharField(max_length=255, verbose_name='Option 4')),
                ('correct_option', models.CharField(choices=[('option1', 'Option 1'), ('option2', 'Option 2'), ('option3', 'Option 3'), ('option4', 'Option 4')], max_length=10, verbose_name='Correct Option')),
                ('score', models.DecimalField(decimal_places=2, default=0.0, max_digits=5, verbose_name='Score')),
            ],
        ),
        migrations.CreateModel(
            name='ShortQuiz',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='Id')),
                ('question', models.TextField(verbose_name='Question')),
                ('option1', models.CharField(max_length=255, verbose_name='Option 1')),
                ('option2', models.CharField(max_length=255, verbose_name='Option 2')),
                ('correct_option', models.CharField(choices=[('option1', 'Option 1'), ('option2', 'Option 2')], max_length=10, verbose_name='Correct Option')),
                ('score', models.DecimalField(decimal_places=2, default=0.0, max_digits=5, verbose_name='Score')),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='Id')),
                ('index', models.IntegerField(verbose_name='Index')),
                ('prerequisite', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, to='individual_course_management.course', verbose_name='Prerequisite')),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('description', models.TextField(verbose_name='Description')),
                ('start_date', models.DateField(verbose_name='Start Date')),
                ('end_date', models.DateField(null=True, verbose_name='End Date')),
                ('edit_date', models.DateTimeField(auto_now=True, verbose_name='Edit Date')),
                ('visible', models.BooleanField(default=False, verbose_name='Visible')),
                ('enable_completed', models.BooleanField(default=False, verbose_name='Enable Completed')),
                ('score', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Score')),
                ('role', models.ManyToManyField(to='role_management.role', verbose_name='Role')),
                ('course_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='individual_course_management.coursegroup', verbose_name='Individual Course Group')),
            ],
        ),
        migrations.CreateModel(
            name='Chapter',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='Id')),
                ('index', models.IntegerField(verbose_name='Index')),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('description', models.TextField(verbose_name='Description')),
                ('score', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Score')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='individual_course_management.course', verbose_name='Course')),
            ],
        ),
        migrations.CreateModel(
            name='CourseEnroll',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('enroll_status', models.BooleanField(default=False, verbose_name='Enroll')),
                ('period', models.IntegerField(verbose_name='Period')),
                ('start_date', models.DateField(verbose_name='Enrollment Start Date')),
                ('end_date', models.DateField(verbose_name='End Date')),
                ('expire_notify', models.BooleanField(default=False, verbose_name='Expire Notification')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='Modified At')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='individual_course_management.course', verbose_name='Individual Course')),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='role_management.role', verbose_name='Role')),
            ],
        ),
        migrations.CreateModel(
            name='Enrolment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID')),
                ('completed_course', models.BooleanField(verbose_name='Completed Course')),
                ('status', models.BooleanField(default=False, verbose_name='status')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='Modified At')),
                ('expirate', models.BooleanField(default=False, verbose_name='Expirate')),
                ('CourseEnroll', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='individual_course_management.courseenroll', verbose_name='Course Enroll')),
                ('role_assignment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='role_management.roleassignment', verbose_name='Role Assignment')),
            ],
        ),
        migrations.CreateModel(
            name='ContentComplete',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='Id')),
                ('created_at', models.DateField(verbose_name='Created At')),
                ('content', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='individual_course_management.content', verbose_name='Lessons')),
                ('enrolment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='individual_course_management.enrolment')),
            ],
        ),
        migrations.CreateModel(
            name='ChapterComplete',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='Id')),
                ('created_at', models.DateField(verbose_name='Created At')),
                ('chapter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='individual_course_management.chapter', verbose_name='Chapter')),
                ('enrolment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='individual_course_management.enrolment')),
            ],
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='Id')),
                ('index', models.IntegerField(verbose_name='Index')),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('description', models.TextField(verbose_name='Description')),
                ('score', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Score')),
                ('chapter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='individual_course_management.chapter', verbose_name='Chapter')),
            ],
        ),
        migrations.AddField(
            model_name='content',
            name='lesson',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='individual_course_management.lesson', verbose_name='Lessons Id'),
        ),
        migrations.CreateModel(
            name='LessonComplete',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='Id')),
                ('created_at', models.DateField(verbose_name='Created At')),
                ('enrolment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='individual_course_management.enrolment')),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='individual_course_management.lesson', verbose_name='Lesson')),
            ],
        ),
        migrations.CreateModel(
            name='QuizSubmit',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='Id')),
                ('answer', models.CharField(choices=[('option1', 'Option 1'), ('option2', 'Option 2'), ('option3', 'Option 3'), ('option4', 'Option 4')], max_length=10, verbose_name='Answer')),
                ('is_correct', models.BooleanField(default=False, verbose_name='Is correct')),
                ('created_at', models.DateField(auto_now_add=True, verbose_name='Created At')),
                ('modified_at', models.DateField(auto_now=True, verbose_name='Modified At')),
                ('enrolment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='individual_course_management.enrolment', verbose_name='Individual Course Enrolment')),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='individual_course_management.quiz', verbose_name='Quiz')),
            ],
        ),
        migrations.CreateModel(
            name='ShortQuizSubmit',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='Id')),
                ('answer', models.CharField(choices=[('option1', 'Option 1'), ('option2', 'Option 2')], max_length=10, verbose_name='Answer')),
                ('is_correct', models.BooleanField(default=False, verbose_name='Is correct')),
                ('created_at', models.DateField(auto_now_add=True, verbose_name='Created At')),
                ('modified_at', models.DateField(auto_now=True, verbose_name='Modified At')),
                ('enrolment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='individual_course_management.enrolment', verbose_name='Individual Course Enrolment')),
                ('short_quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='individual_course_management.shortquiz', verbose_name='Individual Short Quiz')),
            ],
        ),
        migrations.CreateModel(
            name='Strike',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='Id')),
                ('created_at', models.DateField(auto_now_add=True, verbose_name='Created At')),
                ('modified_at', models.DateField(auto_now=True, verbose_name='Modified At')),
                ('day_name', models.CharField(choices=[('saturday', 'Saturday'), ('sunday', 'Sunday'), ('monday', 'Monday'), ('tuesday', 'Tuesday'), ('wednesday', 'Wednesday')], max_length=10, verbose_name='Day Name')),
                ('battery_status', models.SmallIntegerField(choices=[(0, 'zero'), (1, 'One'), (2, 'Two')], default=0, verbose_name='Battery Status')),
                ('length', models.SmallIntegerField(choices=[(0, 'zero'), (1, 'One'), (2, 'Two'), (3, 'three'), (4, 'four'), (5, 'five')], default=0, verbose_name='Length')),
                ('expired_at', models.DateField(verbose_name='Expired At')),
                ('strike_status', models.CharField(choices=[('active', 'Active'), ('inactive', 'Inactive'), ('expired', 'Expired')], max_length=50)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
        ),
        migrations.CreateModel(
            name='StrikeHistory',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='Id')),
                ('created_at', models.DateField(auto_now_add=True, verbose_name='Created At')),
                ('day_name', models.CharField(choices=[('saturday', 'Saturday'), ('sunday', 'Sunday'), ('monday', 'Monday'), ('tuesday', 'Tuesday'), ('wednesday', 'Wednesday')], max_length=10, verbose_name='Day Name')),
                ('battery_status', models.SmallIntegerField(choices=[(0, 'zero'), (1, 'One'), (2, 'Two')], default=0, verbose_name='Battery Status')),
                ('expired_at', models.DateField(verbose_name='Expired At')),
                ('strike_status', models.CharField(choices=[('active', 'Active'), ('inactive', 'Inactive'), ('expired', 'Expired')], max_length=50)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
        ),
        migrations.CreateModel(
            name='Template',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='Id')),
                ('index', models.IntegerField(verbose_name='Index')),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('description', models.TextField(verbose_name='Description')),
                ('type', models.CharField(choices=[('quiz', 'Quiz'), ('shortquiz', 'ShortQuiz'), ('textbook', 'TextBook')], max_length=50)),
                ('score', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Score')),
                ('template_content', models.TextField(blank=True, verbose_name='Template content')),
                ('completed', models.BooleanField(default=False, verbose_name='Completed')),
                ('next_template', models.BooleanField(default=False, verbose_name='Next Template')),
                ('content', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='individual_course_management.content', verbose_name='Contents')),
            ],
        ),
        migrations.AddField(
            model_name='shortquiz',
            name='template',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='individual_course_management.template', verbose_name='Individual Course Template'),
        ),
        migrations.AddField(
            model_name='quiz',
            name='template',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='individual_course_management.template', verbose_name='Individual Course Template'),
        ),
    ]