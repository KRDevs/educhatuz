from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField

from account.models import TeacherProfile, User, StudentProfile
from subject.models import Subject


class Lesson(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True,
                                related_name="lesson_subject")
    title = models.CharField(max_length=255)
    description = models.TextField(verbose_name="Qisqacha ma'lumot",blank=True)
    teachers = models.ManyToManyField(TeacherProfile, related_name="lesson_teacher")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Dars"
        verbose_name_plural = "Darslar"


class AcademicPart(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="academic")
    body = RichTextUploadingField()
    video = models.FileField(upload_to="lesson_videos/", null=True, blank=True)
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.lesson.title} ning nazariy qismi"

    class Meta:
        verbose_name = "Darsning nazariy qismi"
        verbose_name_plural = "Darsning nazariy qismlari"


class AcademicPartFile(models.Model):
    academic_part = models.ForeignKey(AcademicPart, on_delete=models.CASCADE, related_name="files")
    file = models.FileField(upload_to="lesson_files/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Files for {self.academic_part.lesson.title}"

    class Meta:
        verbose_name = "Fayl"
        verbose_name_plural = "Fayllar"


class AcademicPartReaction(models.Model):
    LIKE = "like"
    DISLIKE = "dislike"

    REACTION_CHOICES = [
        (LIKE, "Like"),
        (DISLIKE, "Dislike")
    ]

    academic_part = models.ForeignKey(AcademicPart, on_delete=models.CASCADE, related_name="reactions",
                                      verbose_name="Nazariy qism")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reaction = models.CharField(max_length=10, choices=REACTION_CHOICES)

    class Meta:
        unique_together = ("academic_part", "user")
        verbose_name = "Reaksiya"
        verbose_name_plural = "Reaksiyalar"

    def __str__(self):
        return f"{self.user.username} - {self.reaction} - {self.academic_part.lesson.title}"

class AcademicPartView(models.Model):
    academic_part = models.ForeignKey(AcademicPart, on_delete=models.CASCADE, related_name="views_by_students")
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('academic_part', 'student')

    def __str__(self):
        return f"{self.student.user.username} {self.academic_part.lesson.title} ni ko'rgan"