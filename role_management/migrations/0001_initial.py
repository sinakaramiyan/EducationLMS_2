# Generated by Django 5.1.2 on 2024-11-18 07:53

import django.core.validators
import django.db.models.deletion
import role_management.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CoursePermission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='Name')),
                ('code_name', models.CharField(max_length=100, unique=True, verbose_name='Code Name')),
                ('description', models.TextField(verbose_name='Description')),
            ],
        ),
        migrations.CreateModel(
            name='RoleAssignment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='Id')),
                ('name', models.CharField(max_length=50, verbose_name='Name')),
                ('status', models.CharField(default=True, max_length=10, verbose_name='Status')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated At')),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='Name')),
                ('short_name', models.CharField(max_length=20, verbose_name='Short Name')),
                ('description', models.TextField(verbose_name='Description')),
            ],
        ),
        migrations.CreateModel(
            name='ManagerMoreDetails',
            fields=[
                ('role_assignment', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='role_management.roleassignment', verbose_name='Role Assignment')),
                ('resume', models.FileField(blank=True, null=True, upload_to=role_management.models.resume_directory_path, verbose_name='Resume')),
                ('expertise', models.TextField(blank=True, null=True, verbose_name='Expertise')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated At')),
            ],
        ),
        migrations.CreateModel(
            name='StudentMoreDetails',
            fields=[
                ('role_assignemnt', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='role_management.roleassignment', verbose_name='Role Assignment')),
                ('resume', models.FileField(blank=True, null=True, upload_to='resumes/', verbose_name='Resume')),
                ('father_number', models.CharField(max_length=15, validators=[django.core.validators.RegexValidator(message="شماره تلفن باید با فرمت '+989876543210' وارد شود. حداکثر ۱۵ رقم مجاز است.", regex='^\\+?1?\\d{9,15}$')], verbose_name='Father Number')),
                ('mother_number', models.CharField(max_length=15, validators=[django.core.validators.RegexValidator(message="شماره تلفن باید با فرمت '+989876543210' وارد شود. حداکثر ۱۵ رقم مجاز است.", regex='^\\+?1?\\d{9,15}$')], verbose_name='Mother Number')),
                ('home_number', models.CharField(max_length=15, verbose_name='Home Number')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated At')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
            ],
        ),
        migrations.CreateModel(
            name='RALevel',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='Id')),
                ('name', models.CharField(max_length=50, verbose_name='Name')),
                ('description', models.TextField(blank=True, verbose_name='Description')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated At')),
                ('role_assignment', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='role_management.roleassignment', verbose_name='Role Assignment')),
            ],
        ),
        migrations.AddField(
            model_name='roleassignment',
            name='role',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='role_management.role', verbose_name='Role'),
        ),
        migrations.CreateModel(
            name='RolePermission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='role_management.role', verbose_name='Role')),
                ('course_permission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='role_management.coursepermission', verbose_name='Course Permission')),
            ],
        ),
    ]