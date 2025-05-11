from django.contrib import admin

from subject.models import Subject, Lesson, Comment, AcademicPart
from subject.models.lesson import AcademicPartReaction, AcademicPartFile
from subject.models.live_lesson import LiveSession
from subject.models.subject import Year

admin.site.register(Subject)
admin.site.register(Lesson)
admin.site.register(AcademicPartReaction)
admin.site.register(AcademicPartFile)
admin.site.register(Comment)
admin.site.register(AcademicPart)
admin.site.register(Year)
admin.site.register(LiveSession)
