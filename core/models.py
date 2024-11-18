from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.conf import settings
from django.templatetags.static import static
from django.urls import reverse
from django_jalali.db import models as jmodel
import os
import re

def user_directory_path(instance, filename):
    user_id = instance.user.id
    path = os.path.join('profile_pics', str(user_id))
    os.makedirs(os.path.join(settings.MEDIA_ROOT, path), exist_ok=True)

    return os.path.join(path, filename)


def is_valid_iran_national_id(nat_id):
    if not re.search(r'^\d{10}$', nat_id): raise ValidationError("!کد ملی وارد شده صحیح نمی باشد")
    check = int(nat_id[9])
    s = sum(int(nat_id[x]) * (10 - x) for x in range(9)) % 11
    if s < 2:
        if not check == s:
            raise ValidationError("!کد ملی وارد شده صحیح نمی باشد")
    else:
        if not check + s == 11:
            raise ValidationError("!کد ملی وارد شده صحیح نمی باشد")


class CustomUser(AbstractUser):
    class CustomUserManager(BaseUserManager):

        def create_user(self, email, password, **extra_fields):
            """
            Create and save a user with the given email and password.
            """
            if not email:
                raise ValueError(_("The Email must be set"))
            email = self.normalize_email(email)
            user = self.model(email=email, **extra_fields)
            user.set_password(password)
            user.save()
            return user

        def create_superuser(self, email, password, **extra_fields):
            """
            Create and save a SuperUser with the given email and password.
            """
            extra_fields.setdefault("is_staff", True)
            extra_fields.setdefault("is_superuser", True)
            extra_fields.setdefault("is_active", True)

            if extra_fields.get("is_staff") is not True:
                raise ValueError(_("Superuser must have is_staff=True."))
            if extra_fields.get("is_superuser") is not True:
                raise ValueError(_("Superuser must have is_superuser=True."))
            return self.create_user(email, password, **extra_fields)
    
    first_name = models.CharField(max_length=50, verbose_name=_("Firstname"))
    last_name = models.CharField(max_length=50, verbose_name=_("Lastname"))
    email = models.EmailField(unique=True, verbose_name=_("Email"))
    phone = models.CharField(
        max_length=16,
        default="",
        blank=False,
        null=False,
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message="شماره تلفن باید با فرمت '+989876543210' وارد شود. حداکثر ۱۵ رقم مجاز است."),
        ],
        verbose_name=_("Phone")
    )
    address = models.TextField(max_length=1000, blank=False, null=True, verbose_name=_("Address"))
    national_id = models.CharField(
        unique=True,
        null=True,
        blank=True,
        max_length=10,
        validators=[is_valid_iran_national_id],
        verbose_name=_("National ID")
    )

    class GenderChoices(models.TextChoices):
        MALE = 'M', "Male"
        FEMALE = 'F', "Female"

    gender = models.CharField(
        max_length=1,
        choices=GenderChoices.choices,
        default=GenderChoices.MALE,
        verbose_name=_("Gender")
    )
    profile_img = models.ImageField(
        upload_to=user_directory_path,
        default=static(settings.DEFAULT_PROFILE_IMG),
        verbose_name=_("Profile Picture")
    )
    birthdate = jmodel.jDateField(verbose_name=_("Birth Date"), null=True )
    city = models.CharField(max_length=50, verbose_name=_("City"))
    province = models.CharField(max_length=50, verbose_name=_("Province"))
    country = models.CharField(max_length=50, verbose_name=_("Country"))

    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def get_absolute_url(self):
        return reverse("user_update", args=[self.id])