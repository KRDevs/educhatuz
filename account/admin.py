from django.contrib import admin

from account.models import Group, Faculty, Speciality, StudentProfile, Rank, TeacherProfile
from account.models import User,LoginHistory

admin.site.register(User)
admin.site.register(LoginHistory)
admin.site.register(Group)
admin.site.register(Faculty)
admin.site.register(Speciality)
admin.site.register(StudentProfile)
admin.site.register(Rank)
admin.site.register(TeacherProfile)





