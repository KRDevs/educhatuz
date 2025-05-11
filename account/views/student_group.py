from django.shortcuts import render

from account.models import Group, StudentProfile


def one_group_students_view(request):
    student_profile = StudentProfile.objects.filter(user=request.user).first()
    students = StudentProfile.objects.filter(group=student_profile.group)
    group = student_profile.group

    return render(request, "account/one_group_students.html", {
        "group": group,
        "students": students
    })
