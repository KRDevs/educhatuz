from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.hashers import make_password
from phonenumber_field.modelfields import PhoneNumberField

from .manager import CustomUserManager


class RoleChoices(models.TextChoices):
    ADMIN = "ADMIN"
    TEACHER = "TEACHER"
    STUDENT = "STUDENT"


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True)
    phoneNumber = PhoneNumberField(region='UZ',
                                   help_text="Telefon raqam shunday ko'rinishda bo'lishi kerak: +998991234567",
                                   unique=True)
    userRole = models.CharField(max_length=15, choices=RoleChoices.choices, default=RoleChoices.STUDENT)
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    objects = CustomUserManager()

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if self.password and not self.password.startswith(('pbkdf2_sha256$', 'bcrypt$', 'argon2')):
            self.password = make_password(self.password)

        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-id']


class LoginHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    browser = models.CharField(max_length=127)
    device = models.CharField(max_length=127)
    date = models.DateTimeField()
    ipAddress = models.CharField(max_length=127)

    def __str__(self):
        return self.device

    class Meta:
        verbose_name = "Login Histories"
        verbose_name_plural = "Login Histories"
