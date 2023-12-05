from django.urls import path
from . import views

app_name = 'main'
urlpatterns = [
    path('', views.IndexView.as_view(), name='home'),

    # path('signup/', views.SignUpView.as_view(), name='signup'),

    # path('categories/', views.categories, name='categories'),
    path('categories/', views.CategoriesView.as_view(), name='categories'),

    # path('category/<int:id>', views.category, name='category'),
    path('category/<int:pk>/', views.CategoryView.as_view(), name='category'),

    path('article/create', views.ArticleCreateView.as_view(), name='article_create'),
    path('article/<int:pk>/', views.ArticleDetailView.as_view(), name='article_detail'),
    path('article/<int:pk>/update/', views.ArticleUpdateView.as_view(), name='article_update'),
    path('article/<int:pk>/delete/', views.ArticleDeleteView.as_view(), name='article_delete'),

    # path('news/<int:pk>', views.news, name='news'),
    path('news/<int:pk>', views.ArticleView.as_view(), name='news'),

    # path('about/', views.about, name='about'),

    # path('contacts/', views.contacts, name='contacts'),
    path('contacts/', views.ContactView.as_view(), name='contacts'),

    # path('profile/', views.profile, name='profile'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile_info/', views.ProfileInfoView.as_view(), name='profile_info'),

    path('formcats/', views.formcats, name='formcats'),
    path('show/', views.get_image, name='show'),
]
