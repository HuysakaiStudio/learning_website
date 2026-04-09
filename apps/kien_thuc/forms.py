from django import forms
from .models import FlashcardSet, Flashcard

class FlashcardSetForm(forms.ModelForm):
    class Meta:
        model = FlashcardSet
        fields = ['mon', 'tieu_de', 'mo_ta']
        widgets = {
            'mon': forms.Select(attrs={'class': 'form-control'}),
            'tieu_de': forms.TextInput(attrs={'class': 'form-control'}),
            'mo_ta': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class FlashcardForm(forms.ModelForm):
    class Meta:
        model = Flashcard
        fields = ['mat_truoc', 'mat_sau']
        widgets = {
            'mat_truoc': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'mat_sau': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }
