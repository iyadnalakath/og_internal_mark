from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from rest_framework.authtoken.models import Token
from django.dispatch import receiver
from django.conf import settings
from django.contrib.auth import authenticate
from django.db.models.signals import post_save

# from store.models import Subject




# Create your models here.


class AccountManager(BaseUserManager):
    def create_user(self, email=None, username=None, phone=None, password=None):
        if not username:
            raise ValueError("User must have a username")

        user = self.model(
            email=self.normalize_email(email) if email else None,
            username=username,
            phone=phone,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email=None, username=None, phone=None, password=None):
        user = self.create_user(
            email=self.normalize_email(email) if email else None,
            username=username,
            phone=phone,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.role = "admin"
        user.save(using=self._db)
        return user


class Semester(models.Model):
    name = models.CharField(max_length=50,null=True,blank=True)

class Subject(models.Model):
    name = models.CharField(max_length=50,null=True,blank=True)
    semester = models.ForeignKey(
        Semester, on_delete=models.CASCADE, related_name="semester_subject", null=True, blank=True
    )
    role = models.CharField(max_length=50,null=True,blank=True)

class Account(AbstractBaseUser):
    user_admin = "admin"
    user_teacher = "teacher"
    user_student = "student"

    user_choices = [
        (user_admin, "admin"),
        (user_teacher, "teacher"),
        (user_student, "student"),
    ]

    email = models.EmailField(verbose_name="email", max_length=60, unique=True,null=True,blank=True)
    username = models.CharField(max_length=60, unique=True)
    date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
    is_admin = models.BooleanField(default=False, null=True, blank=True)
    is_active = models.BooleanField(default=True, null=True, blank=True)
    is_staff = models.BooleanField(default=False, null=True, blank=True)
    is_superuser = models.BooleanField(default=False, null=True, blank=True)
    full_name = models.CharField(max_length=30,null=True, blank=True)
    phone = models.IntegerField(null=True, blank=True)
    subject = models.ManyToManyField(
        Subject, related_name="subject_name"
    )
    # semester = models.ForeignKey(
    #     Semester, on_delete=models.CASCADE, related_name="semester_name", null=True, blank=True
    # )
    semester = models.ManyToManyField(
        Semester, related_name="semester_name"
    )
    copy_pass = models.CharField(max_length=140, null=True, blank=True)
    register_number = models.IntegerField(null=True, blank=True)
    roll_number = models.IntegerField( null=True, blank=True)

    role = models.CharField(
        max_length=30,
        null=True,
        blank=True,
        choices=user_choices,
        default=user_admin,
    )

    objects = AccountManager()

    USERNAME_FIELD = "username"
    # REQUIRED_FIELDS = [
    #     "phone",
    #     "email",
    # ]

    # def __str__(self) -> str:
    #     return self.username

    # def __str__(self) -> str:
    #     return self.full_name

    def __str__(self) -> str:
        return f"{self.username} - {self.full_name}"


    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
    

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
