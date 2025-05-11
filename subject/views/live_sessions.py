import datetime

import jwt
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from account.models import TeacherProfile
from core import settings
from subject.forms import LiveSessionForm
from subject.models.live_lesson import LiveSession


@login_required
def teacher_live_sessions(request):
    teacher = TeacherProfile.objects.get(user=request.user)
    sessions = LiveSession.objects.filter(teacher=teacher).order_by('-start_time')
    return render(request, 'live_lessons.html', {'sessions': sessions})


@login_required
def create_live_session(request):
    teacher = TeacherProfile.objects.get(user=request.user)
    if request.method == 'POST':
        form = LiveSessionForm(request.POST, teacher=teacher)
        if form.is_valid():
            session = form.save(commit=False)
            session.teacher = teacher
            session.save()
            return redirect('subject:teacher_live_sessions')
    else:
        form = LiveSessionForm(teacher=teacher)

    return render(request, 'live_lesson_create.html', {'form': form})


@login_required
def edit_live_session(request, pk):
    session = get_object_or_404(LiveSession, pk=pk, teacher__user=request.user)
    if request.method == 'POST':
        form = LiveSessionForm(request.POST, instance=session, teacher=session.teacher)
        if form.is_valid():
            form.save()
            return redirect('subject:teacher_live_sessions')
    else:
        form = LiveSessionForm(instance=session, teacher=session.teacher)
    return render(request, 'live_lesson_create.html', {'form': form})


@login_required
def delete_live_session(request, pk):
    session = get_object_or_404(LiveSession, pk=pk, teacher__user=request.user)
    if request.method == 'POST':
        session.delete()
        return redirect('subject:teacher_live_sessions')
    return render(request, 'live_lesson_delete_confirm.html', {'session': session})


@login_required
def join_live_session(request, session_id):
    session = get_object_or_404(LiveSession, pk=session_id)

    user = request.user
    is_teacher = hasattr(user, 'teacherprofile')

    room_name = f"{session.lesson.title}_{session.start_time.strftime('%Y%m%d%H%M')}".replace(" ", "_")

    payload = {
        'aud': 'jitsi',
        'iss': 'educhat',
        'sub': 'educhat.uz',
        'room': room_name,
        'exp': datetime.datetime.now() + datetime.timedelta(hours=1),
        'moderator': is_teacher,
        'context': {
            'user': {
                'name': user.username,
                'avatar': request.build_absolute_uri(user.avatar.url) if hasattr(user,'avatar') and user.avatar else "",
            }
        }
    }

    token = jwt.encode(payload, settings.JWT_SECRET, algorithm='HS256')

    jitsi_url = f"https://educhat.uz/{room_name}?jwt={token}"

    return render(request, 'live_session_room.html', {
        'session': session,
        'jitsi_url': jitsi_url
    })
