import sys
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from . import forms
from main.views import get_db_lists, navbar_active # , get_category_list_db, get_tag_list_db


class SignUpView(generic.CreateView):
    # form_class = UserCreationForm
    form_class = forms.UserRegisterForm
    success_url = reverse_lazy('login')
    template_name = 'main/signup.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'Регистрация',
            'navbar': navbar_active('signup'),
        })
        context.update(get_db_lists())
        return context
