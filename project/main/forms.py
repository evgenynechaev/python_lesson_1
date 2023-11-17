from django import forms
from django.forms import widgets
from . import models


class CategoryForm(forms.ModelForm):
    class Meta:
        model = models.Categories
        fields = 'name', 'banner',
        widgets = {
            'name': widgets.TextInput(attrs={'class': 'input', 'placeholder': 'Заголовок'}),
            'banner': widgets.FileInput(attrs={'class': 'input', 'placeholder': 'Image'}),
        }

