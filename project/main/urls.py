from django.urls import path
from . import views

app_name = 'main'
urlpatterns = [
    path('', views.index, name='home'),
    path('categories/', views.categories, name='categories'),
    path('category/<str:name>', views.category, name='category'),
    path('news/<int:pk>', views.news, name='news'),
    path('about/', views.about, name='about'),
    path('contacts/', views.contacts, name='contacts'),
]
