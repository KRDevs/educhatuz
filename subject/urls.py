from django.urls import path

from .views.lesson import lesson_detail, like_reaction, dislike_reaction, create_lesson, edit_lesson, delete_lesson, \
    delete_file, lesson_detail_student
from .views.live_sessions import teacher_live_sessions, create_live_session, edit_live_session, delete_live_session, \
    join_live_session
from .views.live_sessions_student import join_live_session_student, student_live_sessions
from .views.subject import subject_lessons
from .views.subject_student import subject_lessons_student

app_name = 'subject'

urlpatterns = [
    path('<int:subject_id>/', subject_lessons, name='subject_lessons'),
    path('<int:subject_id>/student/', subject_lessons_student, name='subject_lessons_student'),
    path('lesson/<int:pk>/', lesson_detail, name='lesson_detail'),
    path('lesson/<int:pk>/student/', lesson_detail_student, name='lesson_detail_student'),
    path('reaction/like/<int:part_id>/', like_reaction, name='like_reaction'),
    path('reaction/dislike/<int:part_id>/', dislike_reaction, name='dislike_reaction'),
    path('lessons/create/<int:subject_id>/', create_lesson, name='create_lesson'),
    path('lessons/<int:lesson_id>/edit/', edit_lesson, name='edit_lesson'),
    path('file/delete/<int:file_id>/', delete_file, name='delete_file'),
    path('lessons/<int:lesson_id>/delete/', delete_lesson, name='delete_lesson'),
    path('live-sessions/', teacher_live_sessions, name='teacher_live_sessions'),
    path('live-sessions/create/', create_live_session, name='create_live_session'),
    path('live-sessions/<int:pk>/edit/', edit_live_session, name='edit_live_session'),
    path('live-sessions/<int:pk>/delete/', delete_live_session, name='delete_live_session'),
    path('live-sessions/<int:session_id>/join/', join_live_session, name='join_live_session'),
    path('live-sessions/student/', student_live_sessions, name='student_live_sessions'),
    path('live-sessions/student/<int:session_id>/join/', join_live_session_student, name='join_live_session_student'),

]
