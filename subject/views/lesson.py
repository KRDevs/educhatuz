from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from account.models import TeacherProfile
from subject.forms import LessonForm, AcademicPartForm, AcademicPartFileForm
from subject.models import Lesson, AcademicPart, Comment, AcademicPartReaction, Subject, AcademicPartFile
from django.contrib import messages

app_name = 'subject'


@login_required
def lesson_detail(request, pk):
    lesson = get_object_or_404(Lesson, pk=pk)
    academic_parts = lesson.academic.all().prefetch_related('files', 'reactions', 'comments')

    for part in academic_parts:
        part.views += 1
        part.save(update_fields=['views'])
        part.likes_count = part.reactions.filter(reaction=AcademicPartReaction.LIKE).count()
        part.dislikes_count = part.reactions.filter(reaction=AcademicPartReaction.DISLIKE).count()

    # Foydalanuvchi tomonidan yuborilgan izoh (comment) ni qabul qilish
    if request.method == 'POST':
        comment_text = request.POST.get('comment_text')
        part_id = request.POST.get('part_id')
        parent_id = request.POST.get('parent_id')

        if comment_text and part_id:
            part = get_object_or_404(AcademicPart, id=part_id)
            parent = Comment.objects.filter(id=parent_id).first() if parent_id else None
            Comment.objects.create(academic_part=part, user=request.user, text=comment_text, parent=parent)
            return redirect(request.path_info)  # sahifani yangilaydi

    context = {
        'lesson': lesson,
        'academic_parts': academic_parts,
    }
    return render(request, 'lesson_detail.html', context)


@login_required
def like_reaction(request, part_id):
    part = get_object_or_404(AcademicPart, pk=part_id)
    reaction, created = AcademicPartReaction.objects.update_or_create(
        academic_part=part,
        user=request.user,
        defaults={'reaction': AcademicPartReaction.LIKE}
    )
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def dislike_reaction(request, part_id):
    part = get_object_or_404(AcademicPart, pk=part_id)
    reaction, created = AcademicPartReaction.objects.update_or_create(
        academic_part=part,
        user=request.user,
        defaults={'reaction': AcademicPartReaction.DISLIKE}
    )
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def create_lesson(request, subject_id):
    teacher_profile = TeacherProfile.objects.filter(user=request.user).first()
    subject = get_object_or_404(Subject, id=subject_id)

    if not teacher_profile:
        return redirect('some_error_page')

    if request.method == 'POST':
        lesson_form = LessonForm(request.POST)
        part_form = AcademicPartForm(request.POST, request.FILES)
        files = request.FILES.getlist('file')  # Fayllarni ajratib olamiz

        if lesson_form.is_valid() and part_form.is_valid():
            # Darsni saqlaymiz
            lesson = lesson_form.save(commit=False)
            lesson.subject = subject
            lesson.save()
            lesson.teachers.add(teacher_profile)

            # Nazariy qismni saqlaymiz
            academic_part = part_form.save(commit=False)
            academic_part.lesson = lesson
            academic_part.save()

            # Fayllarni saqlaymiz
            for f in files:
                AcademicPartFile.objects.create(academic_part=academic_part, file=f)

            return redirect('subject:subject_lessons', subject_id=subject.id)
    else:
        lesson_form = LessonForm()
        part_form = AcademicPartForm()
        file_form = AcademicPartFileForm()

    return render(request, 'lesson_create.html', {
        'lesson_form': lesson_form,
        'part_form': part_form,
        'file_form': file_form,
        'subject': subject,
    })


@login_required
def edit_lesson(request, lesson_id):
    teacher_profile = TeacherProfile.objects.filter(user=request.user).first()
    lesson = get_object_or_404(Lesson, id=lesson_id, teachers=teacher_profile)
    academic_part = AcademicPart.objects.filter(lesson=lesson).first()

    existing_files = AcademicPartFile.objects.filter(academic_part=academic_part)

    if request.method == 'POST':
        lesson_form = LessonForm(request.POST, instance=lesson)
        part_form = AcademicPartForm(request.POST, request.FILES, instance=academic_part)
        file_form = AcademicPartFileForm(request.POST, request.FILES)

        files = request.FILES.getlist('file')

        if lesson_form.is_valid() and part_form.is_valid():
            lesson_form.save()
            part_form.save()

            for f in files:
                AcademicPartFile.objects.create(academic_part=academic_part, file=f)

            return redirect('subject:subject_lessons', subject_id=lesson.subject.id)

    else:
        lesson_form = LessonForm(instance=lesson)
        part_form = AcademicPartForm(instance=academic_part)
        file_form = AcademicPartFileForm()

    return render(request, 'lesson_edit.html', {
        'lesson_form': lesson_form,
        'part_form': part_form,
        'file_form': file_form,
        'existing_files': existing_files,
        'subject': lesson.subject,
    })

@login_required
def delete_file(request, file_id):
    try:
        file = AcademicPartFile.objects.get(id=file_id)
        lesson = file.academic_part.lesson

        if lesson.teachers.filter(user=request.user).exists():
            file.delete()
            messages.success(request, "Fayl muvaffaqiyatli o‘chirildi.")
        else:
            messages.error(request, "Siz bu faylni o‘chira olmaysiz.")
    except AcademicPartFile.DoesNotExist:
        messages.error(request, "Fayl topilmadi yoki allaqachon o‘chirilgan.")

    return redirect('subject:edit_lesson', lesson_id=lesson.id if 'lesson' in locals() else 0)


@login_required
def delete_lesson(request, lesson_id):
    teacher_profile = TeacherProfile.objects.filter(user=request.user).first()
    lesson = get_object_or_404(Lesson, id=lesson_id, teachers=teacher_profile)

    if request.method == 'POST':
        subject_id = lesson.subject.id
        lesson.delete()
        return redirect('subject:subject_lessons', subject_id=subject_id)

    return render(request, 'lesson_delete.html', {'lesson': lesson})


@login_required
def lesson_detail_student(request, pk):
    lesson = get_object_or_404(Lesson, pk=pk)
    academic_parts = lesson.academic.all().prefetch_related('files', 'reactions', 'comments')

    for part in academic_parts:
        part.views += 1
        part.save(update_fields=['views'])
        part.likes_count = part.reactions.filter(reaction=AcademicPartReaction.LIKE).count()
        part.dislikes_count = part.reactions.filter(reaction=AcademicPartReaction.DISLIKE).count()

    # Foydalanuvchi tomonidan yuborilgan izoh (comment) ni qabul qilish
    if request.method == 'POST':
        comment_text = request.POST.get('comment_text')
        part_id = request.POST.get('part_id')
        parent_id = request.POST.get('parent_id')

        if comment_text and part_id:
            part = get_object_or_404(AcademicPart, id=part_id)
            parent = Comment.objects.filter(id=parent_id).first() if parent_id else None
            Comment.objects.create(academic_part=part, user=request.user, text=comment_text, parent=parent)
            return redirect(request.path_info)  # sahifani yangilaydi

    context = {
        'lesson': lesson,
        'academic_parts': academic_parts,
    }
    return render(request, 'lesson_detail_student.html', context)