from django.utils import timezone
from django.db import models
from django.utils.text import slugify

from account.models import TeacherProfile
from subject.models import Lesson


class LiveSession(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="live_session")
    teacher = models.ForeignKey(TeacherProfile, on_delete=models.CASCADE, related_name="live_teachers")
    room_name = models.CharField(max_length=255, unique=True, blank=True)
    start_time = models.DateTimeField()
    duration_minutes = models.PositiveIntegerField(default=60)

    def save(self, *args, **kwargs):
        if not self.room_name:
            time_str = self.start_time.strftime('%Y-%m-%d-%H-%M')
            self.room_name = slugify(f"{self.lesson.title}-{time_str}")
        super().save(*args, **kwargs)

    @property
    def is_joinable(self):
        now = timezone.now()
        end = self.start_time + timezone.timedelta(minutes=self.duration_minutes)
        return self.start_time <= now <= end

    def __str__(self):
        return f"{self.lesson.title} uchun jonli sessiya"
