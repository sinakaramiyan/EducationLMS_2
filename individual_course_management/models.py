from django.db import models
from datetime import timedelta, datetime
from django.utils.translation import gettext_lazy as _
from role_management.models import Role, RoleAssignment
from core.models import CustomUser
    
# in individual course this model stand for learning path that contain related courses
class CourseGroup(models.Model):
    id = models.AutoField(
        verbose_name=_("Id"),
        primary_key=True
    )

    title = models.CharField(
        verbose_name=_("Title"),
        max_length=255
    )

    description = models.TextField(
        verbose_name=_("Description"),
        blank=True
    )

    start_date = models.DateField(
        verbose_name=_("Start Date")
    )

    end_date = models.DateField(
        verbose_name=_("End Date"),
        null=True
    )

    edit_date = models.DateTimeField(
        verbose_name=_("Edit Date"),
        auto_now=True
    )

    visible = models.BooleanField(
        verbose_name=_("Visible"),
        default=False
    )

    enable_completed = models.BooleanField(
        verbose_name=_("Enable Completed"),
        default=False
    )

    def __str__(self):
        return self.title

# represent individual course in learning path for individual course group
class Course(models.Model):
    id = models.AutoField(
        verbose_name=_("Id"),
        primary_key=True
    )

    course_group = models.ForeignKey(
        CourseGroup, 
        verbose_name=_("Individual Course Group"),
        on_delete=models.CASCADE
    )

    role = models.ManyToManyField(
        Role,
        verbose_name=_("Role")
    )

    # in list of learning path ( individual course group ) this index tell, what queue this individual course has.
    index = models.IntegerField(
        verbose_name=_("Index")
    )

    prerequisite = models.OneToOneField(
        'self', 
        on_delete=models.CASCADE, 
        verbose_name=_("Prerequisite"),
        null=True, 
        parent_link=True
    )

    title = models.CharField(
        verbose_name=_("Title"),
        max_length=255
    )

    description = models.TextField(
        verbose_name=_("Description")
    )

    start_date = models.DateField(
        verbose_name=_("Start Date")
    )

    end_date = models.DateField(
        verbose_name=_("End Date"),
        null=True
    )

    edit_date = models.DateTimeField(
        verbose_name=_("Edit Date"),
        auto_now=True
    )

    visible = models.BooleanField(
        verbose_name=_("Visible"),
        default=False
    )
    
    enable_completed = models.BooleanField(
        verbose_name=_("Enable Completed"),
        default=False
    )

    score = models.DecimalField(
        verbose_name=_("Score"),
        max_digits=5, 
        decimal_places=2
    )

    def __str__(self):
        return self.title
    
    def set_index(self, *args, **kwargs):
        if self.pk is None: # Check if the object is being created
            # Get the maximum index value from the existing records
            max_index = Course.objects.aggregate(models.Max('index'))
            self.index = (max_index or 0) + 1 # Increment by 1, default to 1 if no records exist
        super().save(*args, **kwargs)

# set role for course 
class CourseEnroll(models.Model):
    id = models.AutoField(
        primary_key=True, 
        verbose_name="ID"
    )
    
    role = models.ForeignKey(
        Role, 
        on_delete=models.CASCADE, 
        verbose_name="Role"
    )
    
    course = models.ForeignKey(
        Course, 
        on_delete=models.CASCADE, 
        verbose_name="Individual Course"
    )

    name = models.CharField(
        max_length=255, 
        verbose_name="Name"
    )

    enroll_status = models.BooleanField(
        default=False, 
        verbose_name="Enroll"
    )

    period = models.IntegerField(
        verbose_name="Period"
    )

    start_date = models.DateField(
        verbose_name="Enrollment Start Date"
    )
    
    end_date = models.DateField(
        verbose_name="End Date"
    )

    expire_notify = models.BooleanField(
        default=False, 
        verbose_name="Expire Notification"
    )

    created_at = models.DateTimeField(
        auto_now_add=True, 
        verbose_name="Created At"
    )

    modified_at = models.DateTimeField(
        auto_now=True, 
        verbose_name="Modified At"
    )

    def __str__(self):
        return self.name

# When role for course assigned then role assignment user can participate in course with related assigned role 
class Enrolment(models.Model):
    id = models.AutoField(
        verbose_name=_("ID"),
        primary_key=True
    )

    role_assignment = models.ForeignKey(
        RoleAssignment, 
        verbose_name=_("Role Assignment"),
        on_delete=models.CASCADE
    )

    CourseEnroll = models.ForeignKey(
        CourseEnroll,
        verbose_name=_("Course Enroll"),
        on_delete=models.CASCADE
    )

    completed_course = models.BooleanField(
        verbose_name=_("Completed Course"),
    )

    status = models.BooleanField(
        verbose_name=_("status"),
        default=False
    )

    created_at = models.DateTimeField(
        verbose_name=_("Created At"),
        auto_now_add=True
    )

    modified_at = models.DateTimeField(
        verbose_name=_("Modified At"),
        auto_now=True
    )

    expirate = models.BooleanField(
        verbose_name=_("Expirate"),
        default=False
    )

    def __str__(self):
        if(self.status):
            return 'active'
        else:
            return 'not active'

# chapter means steps that require for pass individual course
class Chapter(models.Model):
    id = models.AutoField(
        verbose_name=_("Id"),
        primary_key=True
    )

    course = models.ForeignKey(
        Course, 
        verbose_name=_("Course"),
        on_delete=models.CASCADE
    )

    # in list of course chapters this index tell, what queue this chapter has.
    index = models.IntegerField(
        verbose_name=_("Index")
    )

    title = models.CharField(
        verbose_name=_("Title"),
        max_length=255
    )

    description = models.TextField(
        verbose_name=_("Description")
    )

    score = models.DecimalField(
        verbose_name=_("Score"),
        max_digits=5, 
        decimal_places=2
    )

    def __str__(self):
        return f'{self.title} - {self.index}'
    
    def set_index(self, *args, **kwargs):
        if self.pk is None: # Check if the object is being created
            # Get the maximum index value from the existing records
            max_index = Chapter.objects.aggregate(models.Max('index'))
            self.index = (max_index or 0) + 1 # Increment by 1, default to 1 if no records exist
        super().save(*args, **kwargs)

# model for enrollment user that complete chapter
class ChapterComplete(models.Model):
    id = models.AutoField(
        verbose_name=_("Id"),
        primary_key=True
    )

    chapter = models.ForeignKey(
        Chapter, 
        verbose_name=_("Chapter"),
        on_delete=models.CASCADE
    )

    enrolment = models.ForeignKey(
        Enrolment, 
        on_delete=models.CASCADE
    )

    created_at = models.DateField(
        verbose_name=_("Created At"),
        auto_now_add=False
    )

# in every faze we have collection of group that in ui can see as slaty progressbar
class Lesson(models.Model):
    id = models.AutoField(
        verbose_name=_("Id"),
        primary_key=True
    )

    chapter = models.ForeignKey(
        Chapter, 
        verbose_name=_("Chapter"),
        on_delete=models.CASCADE
    )

    # in list of courses lessons this index tell, what queue this lesson has.
    index = models.IntegerField(
        verbose_name=_("Index")
    )

    title = models.CharField(
        verbose_name=_("Title"),
        max_length=255
    )

    description = models.TextField(
        verbose_name=_("Description")
    )

    score = models.DecimalField(
        verbose_name=_("Score"),
        max_digits=5, 
        decimal_places=2
    )

    def __str__(self):
        return f'{self.title} - {self.index}'
    
    def set_index(self, *args, **kwargs):
        if self.pk is None: # Check if the object is being created
            # Get the maximum index value from the existing records
            max_index = Lesson.objects.aggregate(models.Max('index'))
            self.index = (max_index or 0) + 1 # Increment by 1, default to 1 if no records exist
        super().save(*args, **kwargs)
    
# model for user that complete lessons
class LessonComplete(models.Model):
    id = models.AutoField(
        verbose_name=_("Id"),
        primary_key=True
    )

    lesson = models.ForeignKey(
        Lesson, 
        verbose_name=_("Lesson"),
        on_delete=models.CASCADE
    )

    enrolment = models.ForeignKey(
        Enrolment, 
        on_delete=models.CASCADE
    )

    created_at = models.DateField(
        verbose_name=_("Created At"),
        auto_now_add=False
    )

# every progressbar( lesson contain collection of progresssbar ) has section in it that contain related content
class Content(models.Model):
    id = models.AutoField(
        verbose_name=_("Id"),
        primary_key=True
    )

    lesson = models.ForeignKey(
        Lesson, 
        verbose_name=_("Lessons Id"),
        on_delete=models.CASCADE
    )

    # in list of courses contents this index tell, what queue this content has.
    index = models.IntegerField(
        verbose_name=_("Index")
    )

    title = models.CharField(
        verbose_name=_("Title"),
        max_length=255
    )

    description = models.TextField(
        verbose_name=_("Description")
    )

    next_content = models.BooleanField(
        verbose_name=_("Next Content"),
        default=False
    )

    score = models.DecimalField(
        verbose_name=_("Score"),
        max_digits=5, 
        decimal_places=2
    )

    def __str__(self):
        return f'{self.title} - {self.index}'
    
    def set_index(self, *args, **kwargs):
        if self.pk is None: # Check if the object is being created
            # Get the maximum index value from the existing records
            max_index = Content.objects.aggregate(models.Max('index'))
            self.index = (max_index or 0) + 1 # Increment by 1, default to 1 if no records exist
        super().save(*args, **kwargs)

# model for user that complete contents ( single progressbar )
class ContentComplete(models.Model):
    id = models.AutoField(
        verbose_name=_("Id"),
        primary_key=True
    )

    content = models.ForeignKey(
        Content, 
        verbose_name=_("Lessons"),
        on_delete=models.CASCADE
    )

    enrolment = models.ForeignKey(
        Enrolment, 
        on_delete=models.CASCADE
    )

    created_at = models.DateField(
        verbose_name=_("Created At"),
        auto_now_add=False
    )

# every content ( single progressbar ) have plenty of content that been save in this model
class Template(models.Model):
    id = models.AutoField(
        verbose_name=_("Id"),
        primary_key=True
    )

    content = models.ForeignKey(
        Content,
        verbose_name=_("Contents"), 
        on_delete=models.CASCADE
    )

    # in list of template this index tell, what queue this template has.
    index = models.IntegerField(
        verbose_name=_("Index")
    )

    title = models.CharField(
        verbose_name=_("Title"),
        max_length=255
    )

    description = models.TextField(
        verbose_name=_("Description")
    )

    TYPE_CHOICES = [
        ('quiz', _('Quiz')),
        ('shortquiz', _('ShortQuiz')),
        ('textbook', _('TextBook')),
        # Add more types as needed
    ]

    type = models.CharField(
        max_length=50, 
        choices=TYPE_CHOICES
    )

    score = models.DecimalField(
        verbose_name=_("Score"),
        max_digits=5, 
        decimal_places=2
    )

    # contain html content
    template_content = models.TextField(
        verbose_name=_("Template content"),
        blank=True, 
    )  # or use custom models.HTMLField()

    completed = models.BooleanField(
        verbose_name= _("Completed"),
        default=False
    )

    next_template = models.BooleanField(
        verbose_name=_("Next Template"),
        default=False
    )

    def __str__(self):
        return self.title
    
    def set_index(self, *args, **kwargs):
        if self.pk is None: # Check if the object is being created
            # Get the maximum index value from the existing records
            max_index = Content.objects.aggregate(models.Max('index'))
            self.index = (max_index or 0) + 1 # Increment by 1, default to 1 if no records exist
        super().save(*args, **kwargs)
    
    def check_next_template(self, *args, **kwargs):
        if self.pk is None:
            max_index = Content.objects.aggregate(models.Max('index'))
            if self.index == max_index :
                self.next_template = True
            else:
                self.next_template = False

# quiz for template related content
class Quiz(models.Model):
    id = models.AutoField(
        verbose_name=_("Id"),
        primary_key=True
    )

    template = models.ForeignKey(
        Template, 
        verbose_name=_("Individual Course Template"),
        on_delete=models.CASCADE
    )

    question = models.TextField(
        verbose_name=_("Question")
    )

    option1 = models.CharField(
        max_length=255, 
        verbose_name=_("Option 1")
    )

    option2 = models.CharField(
        max_length=255, 
        verbose_name=_("Option 2")
    )

    option3 = models.CharField(
        max_length=255, 
        verbose_name=_("Option 3")
    )

    option4 = models.CharField(
        max_length=255, 
        verbose_name=_("Option 4")
    )

    # Define choices for the correct option
    CORRECT_OPTION_CHOICES = [
        ('option1', 'Option 1'),
        ('option2', 'Option 2'),
        ('option3', 'Option 3'),
        ('option4', 'Option 4'),
    ]

    correct_option = models.CharField(
        max_length=10, 
        verbose_name=_("Correct Option"),
        choices=CORRECT_OPTION_CHOICES
    )

    score = models.DecimalField(
        verbose_name=_("Score"),
        max_digits=5, 
        decimal_places=2,
        default=0.00
    )

    def __str__(self):
        return self.question
    
    def save(self, *args, **kwargs):
        # Ensure that the correct_option points to one of the options
        if self.correct_option not in ['option1', 'option2', 'option3', 'option4']:
            raise ValueError("Correct option must be one of the defined options.")
        super().save(*args, **kwargs)
    
# define role assignment answer for related quiz
class QuizSubmit(models.Model):
    id = models.AutoField(
        verbose_name=_("Id"),
        primary_key=True
    )

    quiz = models.ForeignKey(
        Quiz, 
        on_delete=models.CASCADE, 
        verbose_name=_("Quiz")
    )

    enrolment = models.ForeignKey(
        Enrolment,
        verbose_name=_("Individual Course Enrolment"),
        on_delete=models.CASCADE
    )

    # Define choices for the correct option
    CORRECT_OPTION_CHOICES = [
        ('option1', 'Option 1'),
        ('option2', 'Option 2'),
        ('option3', 'Option 3'),
        ('option4', 'Option 4'),
    ]

    answer = models.CharField(
        max_length=10, 
        verbose_name=_("Answer"),
        choices=CORRECT_OPTION_CHOICES
    )

    is_correct = models.BooleanField(
        verbose_name=_("Is correct"),
        default=False
    )

    created_at = models.DateField(
        verbose_name=_("Created At"),
        auto_now_add=True
    )

    modified_at = models.DateField(
        verbose_name=_("Modified At"),
        auto_now=True
    )
    def __str__(self):
        return f'answer for quiz {self.quiz.question}'

# short quiz for template related content
class ShortQuiz(models.Model):
    id = models.AutoField(
        verbose_name=_("Id"),
        primary_key=True
    )

    template = models.ForeignKey(
        Template, 
        verbose_name=_("Individual Course Template"),
        on_delete=models.CASCADE
    )

    question = models.TextField(
        verbose_name=_("Question")
    )

    option1 = models.CharField(
        max_length=255, 
        verbose_name=_("Option 1")
    )

    option2 = models.CharField(
        max_length=255, 
        verbose_name=_("Option 2")
    )

    CORRECT_OPTION_CHOICES = [
        ('option1', 'Option 1'),
        ('option2', 'Option 2'),
    ]

    correct_option = models.CharField(
        max_length=10, 
        verbose_name=_("Correct Option"),
        choices=CORRECT_OPTION_CHOICES
    )

    score = models.DecimalField(
        verbose_name=_("Score"),
        max_digits=5, 
        decimal_places=2,
        default=0.00
    )

    def __str__(self):
        return self.question

# define user answer for related short quiz
class ShortQuizSubmit(models.Model):
    id = models.AutoField(
        verbose_name=_("Id"),
        primary_key=True
    )

    short_quiz = models.ForeignKey(
        ShortQuiz, 
        verbose_name=_("Individual Short Quiz"),
        on_delete=models.CASCADE
    )

    enrolment = models.ForeignKey(
        Enrolment,
        verbose_name=_("Individual Course Enrolment"),
        on_delete=models.CASCADE
    )

    CORRECT_OPTION_CHOICES = [
        ('option1', 'Option 1'),
        ('option2', 'Option 2'),
    ]
    
    answer = models.CharField(
        max_length=10, 
        verbose_name=_("Answer"),
        choices=CORRECT_OPTION_CHOICES
    )

    is_correct = models.BooleanField(
        verbose_name=_("Is correct"),
        default=False
    )

    created_at = models.DateField(
        verbose_name=_("Created At"),
        auto_now_add=True
    )

    modified_at = models.DateField(
        verbose_name=_("Modified At"),
        auto_now=True
    )

    def __str__(self):
        return f'answer for short_quiz {self.short_quiz.question}'

DAYS_OF_WEEK = [
    ('saturday', 'Saturday'),
    ('sunday', 'Sunday'),
    ('monday', 'Monday'),
    ('tuesday', 'Tuesday'),
    ('wednesday', 'Wednesday'),
]

# maintain strike for users in individual course
class Strike(models.Model):
    id = models.AutoField(
        verbose_name=_("Id"),
        primary_key=True
    )

    user = models.ForeignKey(
        CustomUser, 
        verbose_name=_("User"),
        on_delete=models.CASCADE
    )

    created_at = models.DateField(
        verbose_name=_("Created At"),
        auto_now_add=True
    )

    modified_at = models.DateField(
        verbose_name=_("Modified At"),
        auto_now=True
    )

    day_name = models.CharField(
        max_length=10, 
        verbose_name=_("Day Name"),
        choices=DAYS_OF_WEEK
    )
    
    battery_status = models.SmallIntegerField(
        verbose_name=_("Battery Status"),
        choices=[
            ( 0 , 'zero'),
            ( 1 , 'One'),
            ( 2 , 'Two'),
        ],
        default=0
    )

    # how many day this strike can be active
    length = models.SmallIntegerField(
        verbose_name=_("Length"),choices=[
            ( 0 , 'zero'),
            ( 1 , 'One'),
            ( 2 , 'Two'),
            ( 3 , 'three'),
            ( 4 , 'four'),
            ( 5 , 'five'),
        ],
        default=0
    )
    # change to datetime
    expired_at = models.DateField(
        verbose_name=_("Expired At")
    )

    strike_status = models.CharField(
        max_length=50, 
        choices=[
            ('active', 'Active'),
            ('inactive', 'Inactive'),
            ('expired', 'Expired'),
        ]
    )

    def __str__(self):
        return self.day_name
    
    def check_expired(self):
        """
        Check if the instance has expired based on the given length and created_at date.
        If expired, set the status to "expired".

        :param instance: The instance to check (e.g. a model instance)
        :param length: The length of time before expiration (e.g. 30 days)
        :return: None
        """
        created_at = self.created_at  # assume created_at is a DateField
        expired_at = created_at + timedelta(days=self.length)

        if datetime.date.today() > expired_at:
            self.strike_status = "expired"

# contain history of strikes that user had
class StrikeHistory(models.Model):
    id = models.AutoField(
        verbose_name=_("Id"),
        primary_key=True
    )

    user = models.ForeignKey(
        CustomUser, 
        verbose_name=_("User"),
        on_delete=models.CASCADE
    )

    created_at = models.DateField(
        verbose_name=_("Created At"),
        auto_now_add=True
    )

    day_name = models.CharField(
        max_length=10, 
        verbose_name=_("Day Name"),
        choices=DAYS_OF_WEEK
    )

    battery_status = models.SmallIntegerField(
        verbose_name=_("Battery Status"),
        choices=[
            ( 0 , 'zero'),
            ( 1 , 'One'),
            ( 2 , 'Two'),
        ],
        default=0
    )
    
    expired_at = models.DateField(
        verbose_name=_("Expired At")
    )

    strike_status = models.CharField(
        max_length=50, 
        choices=[
            ('active', 'Active'),
            ('inactive', 'Inactive'),
            ('expired', 'Expired'),
        ]
    )
