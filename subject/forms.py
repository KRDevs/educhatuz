from django import forms
from .models import Lesson, AcademicPart, AcademicPartFile
from .models.live_lesson import LiveSession


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = [single_file_clean(data, initial)]
        return result


class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['title', 'description']


class AcademicPartForm(forms.ModelForm):
    class Meta:
        model = AcademicPart
        fields = ['body', 'video']


class AcademicPartFileForm(forms.ModelForm):
    file = MultipleFileField()

    class Meta:
        model = AcademicPartFile
        fields = ['file']


class LiveSessionForm(forms.ModelForm):
    class Meta:
        model = LiveSession
        fields = ['lesson', 'start_time', 'duration_minutes']
        widgets = {
            'lesson': forms.Select(attrs={
                'class': 'block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500'
            }),
            'start_time': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500'
            }),
            'duration_minutes': forms.NumberInput(attrs={
                'class': 'block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500'
            }),
        }

    def __init__(self, *args, **kwargs):
        teacher = kwargs.pop('teacher', None)
        super().__init__(*args, **kwargs)
        if teacher:
            self.fields['lesson'].queryset = Lesson.objects.filter(teachers=teacher)
        self.fields['lesson'].widget.attrs.update({'class': 'border rounded w-full'})
