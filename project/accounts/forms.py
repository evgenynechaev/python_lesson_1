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
        _input_class = 'form-control p-4'
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
