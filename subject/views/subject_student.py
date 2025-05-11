from django.shortcuts import render, get_object_or_404
from subject.models import Subject, Lesson

from subject.models.lesson import AcademicPartView


def subject_lessons_student(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    student_profile = request.user.studentprofile

    lessons = Lesson.objects.filter(subject=subject).prefetch_related('academic')
    lesson_status = []

    for lesson in lessons:
        # Darsga biriktirilgan AcademicPart bo‘lsa
        academic_part = lesson.academic.first()
        if academic_part:
            has_seen = AcademicPartView.objects.filter(
                academic_part=academic_part,
                student=student_profile
            ).exists()
        else:
            has_seen = False

        lesson_status.append({
            'lesson': lesson,
            'has_seen': has_seen
        })

    context = {
        'subject': subject,
        'lesson_status': lesson_status
    }
    return render(request, 'subjects_student.html', context)
