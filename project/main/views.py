from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return render(request, 'main/index.html')
    # return HttpResponse('<h1> Главная страница </h1>')


def about(request):
    return HttpResponse('<h1> О сайте </h1>')


def contacts(request):
    return HttpResponse('<h1> Контакты </h1>')


def page_not_found(request, exception):
    return render(request, 'page_404.html')
