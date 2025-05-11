from django.db import models
from account.models.base_account import User, RoleChoices


class Group(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Guruh"
        verbose_name_plural = "Guruhlar"


class Faculty(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Fakultet"
        verbose_name_plural = "Fakultetlar"


class Speciality(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Yo'nalish"
        verbose_name_plural = "Yo'nalishlar"


class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                limit_choices_to={'userRole': RoleChoices.STUDENT})
    name = models.CharField(max_length=255)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name="Guruhi")
    faculty = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Fakulteti")
    speciality = models.ForeignKey(Speciality, on_delete=models.SET_NULL, null=True, blank=True,
                                   verbose_name="Yo'nalishi")

    def __str__(self):
        return f"{self.user.username} - {self.group.name if self.group else 'No Group'}"

    class Meta:
        verbose_name = "Student"
        verbose_name_plural = "Studentlar"
