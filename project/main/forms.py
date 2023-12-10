from zoneinfo import ZoneInfo
from datetime import datetime

from django import forms
from django.forms import widgets, TextInput, EmailInput, FileInput, Select
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User

from betterforms.multiform import MultiModelForm

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


class UserUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = 'username', 'email', 'first_name', 'last_name'
        widgets = {
            'username': TextInput({
                'class': 'textinput form-control p-4',
                'placeholder': 'username',
                'readonly': True,
            }),
            'email': EmailInput({
                'class': 'textinput form-control p-4',
                'placeholder': 'e-mail'
            }),
            'first_name': TextInput({
                'class': 'textinput form-control p-4',
                'placeholder': 'Имя'
            }),
            'last_name': TextInput({
                'class': 'textinput form-control p-4',
                'placeholder': 'Фамилия'
            }),
        }
        labels = {
            'username': 'Имя пользователя',
            'email': 'E-Mail',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
        }
        help_texts = {
        }
        error_messages = {
        }


class AccountUpdateForm(forms.ModelForm):
    birthday = forms.DateField(
        label='Дата рождения (ДД.ММ.ГГГГ)',
        input_formats=('%d.%m.%Y',),
        widget=forms.DateInput(
            format='%d.%m.%Y',
            attrs={'class': 'form-control p-4'},
        ),
        # widget=forms.SelectDateWidget(
        #     years=range(datetime.today().year, datetime.today().year-120, -1),
        #     attrs={'class': 'form-control form-control-lg'},
        #     empty_label=('Год', 'Месяц', 'День'),
        # )
    )

    class Meta:
        model = models.Account
        fields = 'nickname', 'birthday', 'gender', 'avatar'
        widgets = {
            'nickname': TextInput({
                'class': 'form-control p-4',
                'placeholder': 'Nickname'}),
            'gender': forms.Select(attrs={
                'class': 'form-control form-control-lg'}),
        }
        labels = {
            'nickname': 'Nickname',
            'gender': 'Пол',
            'avatar': 'Аватар',
        }
        help_texts = {
        }
        error_messages = {
        }


class ProfileUpdateMultiForm(MultiModelForm):
    form_classes = {
        'user': UserUpdateForm,
        'account': AccountUpdateForm,
    }


class ProfileUpdateForm(forms.Form):
    first_name = forms.CharField(
        max_length=100,
        label='Имя',
        help_text='100 символов максимум',
        error_messages={
            'required': 'Please enter your name',
            'max_length': 'Слишком длинное имя',
        },
        # initial='Имя',
        widget=forms.TextInput(attrs={
            'placeholder': 'Введите имя',
            'class': 'form-control p-4',
        })
    )
    last_name = forms.CharField(
        max_length=100,
        label="Имя",
        initial='Фамилия',
        widget=forms.TextInput(attrs={
            'placeholder': 'Введите фамилию',
            'class': 'form-control p-4'
        })
    )
    email = forms.EmailField()
    nickname = forms.CharField(max_length=100, initial='Nickname')
    birthday = forms.DateField()
    gender = forms.Select()

    def update(self, user):
        ...

    class Meta:
        labels = {
            'first_name': 'Имя',
            'nickname': 'Кличка',
            'birthday': 'Дата рождения',
            'gender': 'Пол',
            'avatar': 'Аватар',
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
                'class': 'form-control col-md-4'}),
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


class CommentForm(forms.Form):
    message = forms.CharField(
        label='Комментарий',
        min_length=1,
        max_length=200,
        widget=forms.Textarea(
            attrs={
                'cols': 80,
                'rows': 5,
                'class': _input_class,
                'placeholder': 'Текст',
            }
        ),
        help_text='200 символов максимум',
        error_messages={
        },
    )
