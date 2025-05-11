from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

from account.models.base_account import RoleChoices


def home(request):
    return render(request, 'account/main.html')

@login_required
def dashboard(request):
    if request.user.userRole == RoleChoices.TEACHER:
        return redirect("teacher_dashboard")
    elif request.user.userRole == RoleChoices.STUDENT:
        return redirect("student_dashboard")
    else:
        return HttpResponseForbidden("Sizning rolingizga mos dashboard mavjud emas")