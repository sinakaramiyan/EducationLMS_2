# Generated by Django 5.1.2 on 2024-11-18 11:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('individual_course_management', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='enrolment',
            old_name='CourseEnroll',
            new_name='course_enroll',
        ),
    ]