from django.shortcuts import render, get_object_or_404

from subject.models import Subject, Lesson


def subject_lessons(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    lessons = Lesson.objects.filter(subject=subject)

    context = {
        'subject': subject,
        'lessons': lessons,
    }
    return render(request, 'subjects_teacher.html', context)
