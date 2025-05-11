from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from account.models import StudentProfile, LoginHistory


@login_required
def student_profile(request):
    student = StudentProfile.objects.get(user=request.user)
    login_histories = LoginHistory.objects.filter(user=request.user).order_by('-date')[:10]
    return render(request, 'account/student_profile.html', {'student': student,
                                                            'login_histories': login_histories})
