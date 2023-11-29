from django import forms
from django.forms import widgets
from . import models


class ProfileForm(forms.ModelForm):
    class Meta:
        model = models.Account
        fields = 'user', 'nickname', 'birthday', 'gender', 'account_image',
        widgets = {
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = models.Category
        fields = 'title', 'banner',
        widgets = {
            'title': widgets.TextInput(attrs={'class': 'input', 'placeholder': 'Заголовок'}),
            'banner': widgets.FileInput(attrs={'class': 'input', 'placeholder': 'Image'}),
        }


class ArticleForm(forms.ModelForm):
    class Meta:
        model = models.Article
        fields = 'category', 'author', 'title', 'content', 'banner',
        widgets = {
        }
