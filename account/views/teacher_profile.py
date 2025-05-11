from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from account.models import TeacherProfile, LoginHistory


@login_required
def teacher_profile(request):
    teacher = TeacherProfile.objects.get(user=request.user)
    login_histories = LoginHistory.objects.filter(user=request.user).order_by('-date')[:10]
    return render(request, 'account/teacher_profile.html', {'teacher': teacher, 'login_histories': login_histories})
