import datetime
import jwt
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from account.models import StudentProfile
from core import settings
from subject.models.live_lesson import LiveSession


@login_required
def student_live_sessions(request):
    student = StudentProfile.objects.get(user=request.user)
    sessions = LiveSession.objects.filter(lesson__subject__groups=student.group).order_by('-start_time')
    return render(request, 'live_lessons_student.html', {'sessions': sessions})


@login_required
def join_live_session_student(request, session_id):
    session = get_object_or_404(LiveSession, pk=session_id)
    user = request.user
    is_teacher = hasattr(user, 'teacherprofile')

    room_name = f"{session.lesson.title}_{session.start_time.strftime('%Y%m%d%H%M')}".replace(" ", "_")

    payload = {
        'aud': 'jitsi',
        'iss': 'meet.educhat',
        'sub': 'meet.educhat.uz',
        'room': room_name,
        'exp': datetime.datetime.now() + datetime.timedelta(hours=1),
        'moderator': is_teacher,
        'context': {
            'user': {
                'name': user.username,
                'avatar': request.build_absolute_uri(user.avatar.url) if hasattr(user,
                                                                                 'avatar') and user.avatar else "",
            }
        }
    }

    token = jwt.encode(payload, settings.JWT_SECRET, algorithm='HS256')

    jitsi_url = f"https://meet.educhat.uz/{room_name}?jwt={token}"

    return render(request, 'live_session_room_student.html', {
        'session': session,
        'jitsi_url': jitsi_url
    })
