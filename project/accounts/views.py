# import os
# import sys
# parent_dir_name = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
# sys.path.append(parent_dir_name + "/main")
# import views
# your_script.a_function()
import sys
sys.path.append("..")

from django.shortcuts import render

from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic

from . import forms


class SignUpView(generic.CreateView):
    # form_class = UserCreationForm
    form_class = forms.UserRegisterForm
    success_url = reverse_lazy('login')
    template_name = 'main/signup.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'Регистрация',
            # 'navbar': main.views.navbar_active('signup'),
            'category_title': 'Категории',
            # 'category_list': get_category_list_db(),
            # 'tag_list': get_tag_list_db(),
        })
        return context
