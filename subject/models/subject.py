from django.db import models

from account.models import Faculty, TeacherProfile, Group


class SemesterChoices(models.TextChoices):
    SPRING = "SPRING", "Bahorgi"
    AUTUMN = "AUTUMN", "Kuzgi"


class Year(models.Model):
    name = models.CharField(max_length=155)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Yil"
        verbose_name_plural = "Yillar"


class Subject(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(verbose_name="Qisqacha ma'lumot",blank=True)
    image = models.ImageField(upload_to="subject_images/", null=True, blank=True)
    year = models.ForeignKey(Year, on_delete=models.CASCADE, blank=True)
    semester = models.CharField(max_length=15, choices=SemesterChoices.choices, default=SemesterChoices.AUTUMN)
    begin_at = models.DateField(auto_now=True)
    end_at = models.DateField(auto_now=True)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, blank=True)
    teachers = models.ManyToManyField(TeacherProfile, related_name="subjects_teacher")
    groups = models.ManyToManyField(Group, related_name="subjects_group")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Fan"
        verbose_name_plural = "Fanlar"
