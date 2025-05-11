from django.shortcuts import render, get_object_or_404
from account.models import StudentProfile
from django.contrib.auth.decorators import login_required

from subject.models.lesson import AcademicPartView, Lesson, AcademicPart


@login_required
def lesson_students_view(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    groups = lesson.subject.groups.all()
    students = StudentProfile.objects.filter(group__in=groups).distinct()

    try:
        academic_part = lesson.academic.get()  # 1ta nazariy qism mavjud bo‘lsa
    except AcademicPart.DoesNotExist:
        academic_part = None

    student_data = []
    for student in students:
        has_seen = False
        if academic_part:
            has_seen = AcademicPartView.objects.filter(student=student, academic_part=academic_part).exists()
        student_data.append({
            'student': student,
            'has_seen': has_seen
        })

    return render(request, 'lesson_students.html', {
        'lesson': lesson,
        'student_data': student_data
    })


