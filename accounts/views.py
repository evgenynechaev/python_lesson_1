# import sys
# from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Group

from . import forms
from main.views import get_db_lists, navbar_active


class SignUpView(generic.CreateView):
    template_name = 'accounts/signup.html'
    form_class = forms.UserRegisterForm
    # success_url = reverse_lazy('login')
    success_url = reverse_lazy('main:profile_update')

    def form_valid(self, form):
        valid = super().form_valid(form)
        username, password = form.cleaned_data.get('username'), form.cleaned_data.get('password1')
        new_user = authenticate(username=username, password=password)

        group_name = form.cleaned_data.get('group')
        group = Group.objects.get(name=group_name)
        new_user.groups.add(group)

        login(self.request, new_user)
        return valid

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'Регистрация',
            'navbar': navbar_active('signup'),
        })
        context.update(get_db_lists())
        return context
