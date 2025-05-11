from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models

from account.models import User
from subject.models import AcademicPart


class Comment(models.Model):
    academic_part = models.ForeignKey(AcademicPart, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name="replies")
    text = RichTextUploadingField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} tomonidan {self.academic_part.lesson.title} darsga yozilgan izoh"

    class Meta:
        verbose_name = "Izoh"
        verbose_name_plural = "Izohlar"
