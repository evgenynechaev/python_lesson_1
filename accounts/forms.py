from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class UserRegisterForm(UserCreationForm):
    _input_class = 'form-control p-4'
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

    GROUP_CHOICES = ('Читатели', 'Читатель'), ('Запрос_На_Писатели', 'Запрос на Писателя'),
    group = forms.ChoiceField(
        label='Группа пользователя',
        choices=GROUP_CHOICES,
        widget=forms.RadioSelect(attrs={
            'class': 'p-2',
        })
    )

    # class Meta(UserCreationForm.Meta):
    #     fields = UserCreationForm.Meta.fields + ('email', 'first_name', 'last_name')

    class Meta:
        _input_class = 'form-control p-4'
        model = User
        fields = 'username', 'first_name', 'last_name', 'email', 'password1', 'password2',
        widgets = {
            'username': forms.TextInput(attrs={
                'class': _input_class,
                'placeholder': 'Логин пользователя'}),
            'first_name': forms.TextInput(attrs={
                'class': _input_class,
                'placeholder': 'Введите имя'}),
            'last_name': forms.TextInput(attrs={
                'class': _input_class,
                'placeholder': 'Введите фамилию'}),
            'email': forms.TextInput(attrs={
                'class': _input_class,
                'placeholder': 'Введите электронную почту'}),
        }
        labels = {
            'username': 'Пользователь',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'email': 'Электронная почта',
        }
        help_texts = {
        }
