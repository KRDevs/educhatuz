from django.shortcuts import render
from account.models import Group, StudentProfile

def group_list_view(request):
    groups = Group.objects.all()

    group_data = []
    for group in groups:
        student_count = StudentProfile.objects.filter(group=group).count()
        group_data.append({
            "group": group,
            "student_count": student_count
        })

    return render(request, "account/group_list.html", {
        "group_data": group_data
    })

def group_students_view(request, group_id):
    group = Group.objects.get(id=group_id)
    students = StudentProfile.objects.filter(group=group)

    return render(request, "account/group_students.html", {
        "group": group,
        "students": students
    })
