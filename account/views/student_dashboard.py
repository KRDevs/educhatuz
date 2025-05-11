from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from subject.models import Subject
from account.models import StudentProfile


@login_required
def student_dashboard(request):
    student_profile = StudentProfile.objects.filter(user=request.user).first()

    subjects = Subject.objects.filter(groups=student_profile.group).prefetch_related(
        'groups').order_by('-created_at')
    context = {
        'subjects': subjects,
    }

    return render(request, 'account/student_dashboard.html', context)
