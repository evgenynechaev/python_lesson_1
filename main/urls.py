from django.urls import path, re_path
from django.views.generic.dates import ArchiveIndexView

from . import models
from . import views

app_name = 'main'
urlpatterns = [
    path('', views.IndexView.as_view(), name='home'),

    path('categories/', views.CategoriesView.as_view(), name='categories'),

    # path('category/<int:id>', views.category, name='category'),
    path('category/<int:pk>/', views.CategoryView.as_view(), name='category'),

    path('article/create', views.ArticleCreateView.as_view(), name='article_create'),
    path('article/<int:pk>/', views.ArticleDetailView.as_view(), name='article_detail'),
    path('article/<int:pk>/update/', views.ArticleUpdateView.as_view(), name='article_update'),
    path('article/<int:pk>/delete/', views.ArticleDeleteView.as_view(), name='article_delete'),

    re_path(r'^find/$', views.FindView.as_view(), name='find'),
    re_path(r'^tags/$', views.TagsView.as_view(), name='tags'),

    path('contacts/', views.ContactView.as_view(), name='contacts'),
    path('about/', views.AboutView.as_view(), name='about'),

    path('writer/<int:pk>/', views.UserView.as_view(), name='user'),
    path('writer/<int:pk>/articles/', views.UserArticlesView.as_view(), name='user_articles'),

    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/update/', views.ProfileUpdateMultiView.as_view(), name='profile_update'),
    path('profile/articles/', views.ProfileArticlesView.as_view(), name='profile_articles'),
    path('profile/favorites/', views.ProfileFavoritesView.as_view(), name='profile_favorites'),

    # url(r'^(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<day>[0-9]{2})/(?P<slug>[\w-]+)$', views.post_details),
    # re_path(r'^archive/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<day>[0-9]{2})$/',
    #         views.ArchiveView.as_view(), name='archive'),
    # path('archive/', ArchiveIndexView.as_view(model=models.Article, date_field="created_at"), name="archive"),
    path('archive/', views.ArchiveArticleView.as_view(), name='archive'),
    path('archive/<int:year>/', views.ArchiveArticleYearView.as_view(), name='archive_year'),
    path('archive/<int:year>/<int:month>/', views.ArchiveArticleMonthView.as_view(), name='archive_month'),
    path('archive/<int:year>/<int:month>/<int:day>/', views.ArchiveArticleDayView.as_view(), name='archive_day'),

    # path('formcats/', views.formcats, name='formcats'),
    # path('show/', views.get_image, name='show'),
]
