
from django import forms
from .models import EducationalMethodicalWork

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