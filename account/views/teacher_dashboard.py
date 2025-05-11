from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from account.models import TeacherProfile
from subject.models import Subject


@login_required
def teacher_dashboard(request):
    teacher_profile = TeacherProfile.objects.filter(user=request.user).first()

    subjects = Subject.objects.filter(teachers=teacher_profile).select_related('year', 'faculty').prefetch_related(
        'groups').order_by('-created_at')
    return render(request, "account/teacher_dashboard.html", {'subjects': subjects})
