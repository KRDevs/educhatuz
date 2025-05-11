from django.urls import path

from account.views.login import login_view, logout_view
from account.views.main import home, dashboard
from account.views.student_dashboard import student_dashboard
from account.views.student_group import one_group_students_view
from account.views.student_profile import student_profile
from account.views.teacher_dashboard import teacher_dashboard
from account.views.teacher_group import group_list_view, group_students_view
from account.views.teacher_profile import teacher_profile

urlpatterns = [
    path('', home, name='home'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path("dashboard/", dashboard, name="dashboard"),
    path("dashboard/teacher", teacher_dashboard, name="teacher_dashboard"),
    path('teacher_profile/', teacher_profile, name='teacher_profile'),
    path('student_profile/', student_profile, name='student_profile'),
    path("dashboard/student", student_dashboard, name="student_dashboard"),
    path("groups/", group_list_view, name="group_list"),
    path("group/<int:group_id>/students/", group_students_view, name="group_students"),
    path("student_group/", one_group_students_view, name="one_group_students")
]
