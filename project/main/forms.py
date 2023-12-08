from zoneinfo import ZoneInfo
from datetime import datetime

from django import forms
from django.forms import widgets
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from . import models

zone = ZoneInfo('Asia/Yekaterinburg')

_input_class = 'form-control p-4'


def get_name(user) -> str:
    return f"{user.first_name} {user.last_name}"


def get_datetime_now():
    # return datetime.now(tz=pytz.timezone("Asia/Yekaterinburg"))
    return datetime.now(zone)


class BaseForm(forms.ModelForm):
    def get_name(self, user) -> str:
        return get_name(user)

    def get_datetime_now(self):
        return datetime.now(zone)


class UserRegisterForm(UserCreationForm):
    # _input_class = 'form-control p-4'
    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={
            'class': _input_class,
            'placeholder': 'Введите пароль'}))
    password2 = forms.CharField(
        label='Повтор пароля',
        widget=forms.PasswordInput(attrs={
            'class': _input_class,
            'placeholder': 'Повторите пароль'}))

    # class Meta(UserCreationForm.Meta):
    #     fields = UserCreationForm.Meta.fields + ('email', 'first_name', 'last_name')

    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields['username'].widget.attrs.update({"placeholder": 'Придумайте свой логин'})
            # self.fields['email'].widget.attrs.update({"placeholder": 'Введите свой email'})
            # self.fields['first_name'].widget.attrs.update({"placeholder": 'Ваше имя'})
            # self.fields["last_name"].widget.attrs.update({"placeholder": 'Ваша фамилия'})
            self.fields['password1'].widget.attrs.update({"placeholder": 'Придумайте свой пароль'})
            self.fields['password2'].widget.attrs.update({"placeholder": 'Повторите придуманный пароль'})
            self.fields[field].widget.attrs.update({"class": "form-control", "autocomplete": "off"})
    """

    class Meta:
        # _input_class = 'form-control p-4'
        model = User
        fields = 'username', 'password1', 'password2'
        widgets = {
            'username': forms.TextInput(attrs={
                'class': _input_class,
                'placeholder': 'Логин пользователя'}),
        }
        labels = {
            'username': 'Пользователь',
        }
        help_texts = {
        }


class ProfileForm(BaseForm):
    avatar = forms.ImageField(label='Аватар', required=True)
    birthday = forms.DateField(
        widget=forms.SelectDateWidget(
            # years=range(datetime.date.today().year - 15, 1920, -1),
            attrs={'class': 'form-control'}
        )
    )

    class Meta:
        model = models.Account
        fields = 'nickname', 'birthday', 'gender', 'avatar',
        widgets = {
            'nickname': forms.TextInput(attrs={
                'class': _input_class,
                'placeholder': 'Кличка'}),
            # 'birthday': forms.DateField(),
            'gender': forms.Select(attrs={
                'class': 'form-control'}),
        }
        labels = {
            'nickname': 'Кличка',
            'birthday': 'Дата рождения',
            'gender': 'Пол',
            'avatar': 'Аватар',
        }
        help_texts = {
        }
        error_messages = {
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = models.Category
        fields = 'title', 'banner',
        widgets = {
            'title': widgets.TextInput(attrs={'class': 'input', 'placeholder': 'Заголовок'}),
            'banner': widgets.FileInput(attrs={'class': 'input', 'placeholder': 'Image'}),
        }


class ArticleForm(BaseForm):
    banner = forms.ImageField(label='Баннер', required=True)

    def get_file(self) -> bool:
        uploaded_file = self.files.get('file')
        return uploaded_file

    class Meta:
        model = models.Article
        fields = 'category', 'title', 'annotation', 'content', 'banner',
        widgets = {
            'category': forms.Select(attrs={
                'class': 'form-control'}),
            'title': forms.TextInput(attrs={
                'class': _input_class,
                'placeholder': 'Заголовок статьи'}),
            'annotation': forms.Textarea(attrs={
                'cols': 80,
                'rows': 5,
                'class': _input_class,
                'placeholder': 'Аннотация статьи'}),
            'content': forms.Textarea(attrs={
                'cols': 80,
                'rows': 15,
                'class': _input_class,
                'placeholder': 'Текст статьи'}),
            # 'banner': forms.ImageField(
            #     label='Banner')
        }
        labels = {
            'category': 'Категория',
            'title': 'Заголовок',
            'annotation': 'Аннотация',
            'content': 'Статья',
            'banner': 'Баннер',
        }
        help_texts = {
        }
        error_messages = {
        }
