
from django import forms
from .models import EducationalMethodicalWork
from .models import ResearchWork

class EducationalMethodicalWorkForm(forms.ModelForm):
    class Meta:
        model = EducationalMethodicalWork
        fields = ['title', 'start_date', 'end_date', 'completed'] 
        widgets = {
            'title': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
            'start_date': forms.TextInput(attrs={'class': 'form-control'}),
            'end_date': forms.TextInput(attrs={'class': 'form-control'}),
             'completed': forms.TextInput(attrs={'class': 'form-control'}),
        }

class ResearchWorkForm(forms.ModelForm):
    class Meta:
        model = ResearchWork
        fields = ['topic', 'start_date', 'end_date', 'completed']
        widgets = {
            'topic': forms.Textarea(attrs={'rows': 2, 'class': 'form-control', 'placeholder': 'Наименование темы, этап, задание'}),
            'start_date': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Начало работы'}),
            'end_date': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Окончание работы'}),
            'completed': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Отметка о выполнении'}),
        }