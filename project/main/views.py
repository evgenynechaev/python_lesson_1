from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from django.views import generic
from django.urls import reverse, reverse_lazy
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.contrib.auth.models import User
from django.contrib.auth import mixins

from . import models
from . import forms


def navbar_active(page: str):
    navbar: dict = {
        'home': '',
        'category': '',
        'user': '',
        'article': '',
        'find': '',
        'tags': '',
        'archive': '',
        'contacts': '',
        'profile': '',
        'signup': '',
    }
    navbar.update({'article': 'd-none'})
    navbar.update({'find': 'd-none'})
    navbar.update({'tags': 'd-none'})
    navbar.update({'archive': 'd-none'})
    navbar.update({'contacts': 'd-none'})
    navbar.update({'profile': 'd-none'})
    navbar.update({page: 'active'})
    return navbar


def get_category_list(category_id=''):
    all_category_list = [
        {'pk': 1, 'id': 'business', 'name': 'Бизнес', 'banner': 'img/cat-500x80-1.jpg'},
        {'pk': 2, 'id': 'technology', 'name': 'Технологии', 'banner': 'img/cat-500x80-2.jpg'},
        {'pk': 3, 'id': 'entertainment', 'name': 'Развлечения', 'banner': 'img/cat-500x80-3.jpg'},
        {'pk': 4, 'id': 'sports', 'name': 'Спорт', 'banner': 'img/cat-500x80-4.jpg'},
        {'pk': 5, 'id': 'politics', 'name': 'Политика', 'banner': 'img/cat-500x80-1.jpg'},
        {'pk': 6, 'id': 'corporate', 'name': 'Корпорации', 'banner': 'img/cat-500x80-2.jpg'},
        {'pk': 7, 'id': 'health', 'name': 'Здоровье', 'banner': 'img/cat-500x80-3.jpg'},
        {'pk': 8, 'id': 'education', 'name': 'Образование', 'banner': 'img/cat-500x80-4.jpg'},
        {'pk': 9, 'id': 'science', 'name': 'Наука', 'banner': 'img/cat-500x80-1.jpg'},
        {'pk': 10, 'id': 'foods', 'name': 'Еда', 'banner': 'img/cat-500x80-2.jpg'},
        {'pk': 11, 'id': 'travel', 'name': 'Путешествия', 'banner': 'img/cat-500x80-3.jpg'},
        {'pk': 12, 'id': 'lifestyle', 'name': 'Стиль жизни', 'banner': 'img/cat-500x80-4.jpg'},
    ]
    # if category_id == '':
    #     return all_category_list
    # category_list = [item for item in all_category_list if item.get('id') == category_id]
    # return category_list
    return all_category_list


def get_db_lists():
    user_list = User.objects.all().values('id', 'username', 'first_name', 'last_name')
    category_list = models.Category.objects.all().values('id', 'title', 'banner')
    tag_list = models.Tag.objects.all().values('id', 'title')
    # print('user_list')
    # print(user_list)
    # print('category_list')
    # print(category_list)
    return {
        'user_list': user_list,
        'category_list': category_list,
        'tag_list': tag_list,
    }


"""
def get_user_list_db():
    user_list = User.objects.all().values('id', 'username', 'first_name', 'last_name')
    print('get_user_list_db')
    print(user_list)
    # for category in category_list:
    #     print(category.get('banner'))
    return user_list
"""


"""
def get_category_list_db():
    category_list = models.Category.objects.all().values('id', 'title', 'banner')
    # print('get_category_list_db')
    # print(category_list)
    # for category in category_list:
    #     print(category.get('banner'))
    return category_list
"""


"""
def get_tag_list_db():
    tag_list = models.Tag.objects.all().values('id', 'title')
    return tag_list
"""


def get_category_name_by_pk(category_pk):
    for item in get_category_list():
        if item.get('pk') == category_pk:
            return item.get('name')
    return ''


def get_category_pk_by_id(category_id):
    for item in get_category_list():
        if item.get('id') == category_id:
            return item.get('pk')
    return ''


def get_category_name(category_id):
    for item in get_category_list():
        if item.get('id') == category_id:
            return item.get('name')
    return ''


def get_category_id(category_pk):
    for item in get_category_list():
        if item.get('pk') == category_pk:
            return item.get('id')
    return ''


def get_all_news_list():
    all_news_list = [
        {'id': 1, 'category': 'business', 'author': 'John Doe', 'headline': 'Бизнес новость 1',
         'content': 'Вот это новость 1. Новость. Новость. Новость. Новость. Новость.',
         'banner': 'img/news-500x280-1.jpg', 'pub_date': '2023-11-01 1:00'},
        {'id': 2, 'category': 'business', 'author': 'John Doe', 'headline': 'Бизнес новость 2',
         'content': 'Вот это новость 2. Новость. Новость. Новость. Новость. Новость.',
         'banner': 'img/news-500x280-2.jpg', 'pub_date': '2023-11-02 2:00'},
        {'id': 3, 'category': 'business', 'author': 'John Doe', 'headline': 'Бизнес новость 3',
         'content': 'Вот это новость 3. Новость. Новость. Новость. Новость. Новость.',
         'banner': 'img/news-500x280-3.jpg', 'pub_date': '2023-11-03 3:00'},
        {'id': 4, 'category': 'business', 'author': 'John Doe', 'headline': 'Бизнес новость 4',
         'content': 'Вот это новость 4. Новость. Новость. Новость. Новость. Новость.',
         'banner': 'img/news-500x280-4.jpg', 'pub_date': '2023-11-04 4:00'},

        {'id': 5, 'category': 'technology', 'author': 'Jane Doe', 'headline': 'Технологическая новость 1',
         'content': 'Вот это новость 5. Новость. Новость. Новость. Новость. Новость.',
         'banner': 'img/news-500x280-1.jpg', 'pub_date': '2023-11-05 5:00'},
        {'id': 6, 'category': 'technology', 'author': 'Jane Doe', 'headline': 'Технологическая новость 2',
         'content': 'Вот это новость 6. Новость. Новость. Новость. Новость. Новость.',
         'banner': 'img/news-500x280-2.jpg', 'pub_date': '2023-11-06 6:00'},
        {'id': 7, 'category': 'technology', 'author': 'Jane Doe', 'headline': 'Технологическая новость 3',
         'content': 'Вот это новость 7. Новость. Новость. Новость. Новость. Новость.',
         'banner': 'img/news-500x280-3.jpg', 'pub_date': '2023-11-07 7:00'},
        {'id': 8, 'category': 'technology', 'author': 'Jane Doe', 'headline': 'Технологическая новость 4',
         'content': 'Вот это новость 8. Новость. Новость. Новость. Новость. Новость.',
         'banner': 'img/news-500x280-4.jpg', 'pub_date': '2023-11-08 8:00'},

        {'id': 9, 'category': 'entertainment', 'author': 'Karl Mine', 'headline': 'Новость развлечений 1',
         'content': 'Вот это новость 9. Новость. Новость. Новость. Новость. Новость.',
         'banner': 'img/cat-500x80-1.jpg', 'pub_date': '2023-11-09 9:00'},
        {'id': 10, 'category': 'entertainment', 'author': 'Karl Mine', 'headline': 'Новость развлечений 2',
         'content': 'Вот это новость 10. Новость. Новость. Новость. Новость. Новость.',
         'banner': 'img/cat-500x80-2.jpg', 'pub_date': '2023-11-10 10:00'},
        {'id': 11, 'category': 'entertainment', 'author': 'Karl Mine', 'headline': 'Новость развлечений 3',
         'content': 'Вот это новость 11. Новость. Новость. Новость. Новость. Новость.',
         'banner': 'img/cat-500x80-3.jpg', 'pub_date': '2023-11-11 11:00'},
        {'id': 12, 'category': 'entertainment', 'author': 'Karl Mine', 'headline': 'Новость развлечений 4',
         'content': 'Вот это новость 12. Новость. Новость. Новость. Новость. Новость.',
         'banner': 'img/cat-500x80-4.jpg', 'pub_date': '2023-11-12 12:00'},

        {'id': 13, 'category': 'sports', 'author': 'Nick Name', 'headline': 'Спортивная новость 1',
         'content': 'Вот это новость 13. Новость. Новость. Новость. Новость. Новость.',
         'banner': 'img/cat-500x80-1.jpg', 'pub_date': '2023-11-13 13:00'},
        {'id': 14, 'category': 'sports', 'author': 'Nick Name', 'headline': 'Спортивная новость 2',
         'content': 'Вот это новость 14. Новость. Новость. Новость. Новость. Новость.',
         'banner': 'img/cat-500x80-2.jpg', 'pub_date': '2023-11-14 14:00'},
        {'id': 15, 'category': 'sports', 'author': 'Nick Name', 'headline': 'Спортивная новость 3',
         'content': 'Вот это новость 15. Новость. Новость. Новость. Новость. Новость.',
         'banner': 'img/cat-500x80-3.jpg', 'pub_date': '2023-11-15 15:00'},
        {'id': 16, 'category': 'sports', 'author': 'Nick Name', 'headline': 'Спортивная новость 4',
         'content': 'Вот это новость 16. Новость. Новость. Новость. Новость. Новость.',
         'banner': 'img/cat-500x80-4.jpg', 'pub_date': '2023-11-16 16:00'},

        {'id': 17, 'category': 'politics', 'author': 'Nick Name', 'headline': 'Политика',
         'content': 'Вот это новость 17. Новость. Новость. Новость. Новость. Новость.',
         'banner': 'img/cat-500x80-1.jpg', 'pub_date': '2023-11-17 17:00'},
        {'id': 18, 'category': 'politics', 'author': 'Nick Name', 'headline': 'Политика',
         'content': 'Вот это новость 18. Новость. Новость. Новость. Новость. Новость.',
         'banner': 'img/cat-500x80-1.jpg', 'pub_date': '2023-11-18 18:00'},

        {'id': 19, 'category': 'corporate', 'author': 'Nick Name', 'headline': 'Корпорации',
         'content': 'Вот это новость 19. Новость. Новость. Новость. Новость. Новость.',
         'banner': 'img/cat-500x80-2.jpg', 'pub_date': '2023-11-19 19:00'},
        {'id': 20, 'category': 'corporate', 'author': 'Nick Name', 'headline': 'Корпорации',
         'content': 'Вот это новость 20. Новость. Новость. Новость. Новость. Новость.',
         'banner': 'img/cat-500x80-2.jpg', 'pub_date': '2023-11-20 20:00'},

        {'id': 21, 'category': 'health', 'author': 'Nick Name', 'headline': 'Здоровье',
         'content': 'Вот это новость 21. Новость. Новость. Новость. Новость. Новость.',
         'banner': 'img/cat-500x80-3.jpg', 'pub_date': '2023-11-21 21:00'},
        {'id': 22, 'category': 'health', 'author': 'Nick Name', 'headline': 'Здоровье',
         'content': 'Вот это новость 22. Новость. Новость. Новость. Новость. Новость.',
         'banner': 'img/cat-500x80-3.jpg', 'pub_date': '2023-11-22 22:00'},

        {'id': 23, 'category': 'education', 'author': 'Nick Name', 'headline': 'Образование',
         'content': 'Вот это новость 23. Новость. Новость. Новость. Новость. Новость.',
         'banner': 'img/cat-500x80-4.jpg', 'pub_date': '2023-11-23 23:00'},
        {'id': 24, 'category': 'education', 'author': 'Nick Name', 'headline': 'Образование',
         'content': 'Вот это новость 24. Новость. Новость. Новость. Новость. Новость.',
         'banner': 'img/cat-500x80-4.jpg', 'pub_date': '2023-11-24 00:00'},

        {'id': 25, 'category': 'science', 'author': 'Nick Name', 'headline': 'Наука',
         'content': 'Вот это новость 25. Новость. Новость. Новость. Новость. Новость.',
         'banner': 'img/cat-500x80-1.jpg', 'pub_date': '2023-11-25 1:00'},
        {'id': 26, 'category': 'science', 'author': 'Nick Name', 'headline': 'Наука',
         'content': 'Вот это новость 26. Новость. Новость. Новость. Новость. Новость.',
         'banner': 'img/cat-500x80-1.jpg', 'pub_date': '2023-11-26 2:00'},

        {'id': 27, 'category': 'foods', 'author': 'Nick Name', 'headline': 'Еда',
         'content': 'Вот это новость 27. Новость. Новость. Новость. Новость. Новость.',
         'banner': 'img/cat-500x80-2.jpg', 'pub_date': '2023-11-27 3:00'},
        {'id': 28, 'category': 'foods', 'author': 'Nick Name', 'headline': 'Еда',
         'content': 'Вот это новость 28. Новость. Новость. Новость. Новость. Новость.',
         'banner': 'img/cat-500x80-2.jpg', 'pub_date': '2023-11-28 4:00'},

        {'id': 29, 'category': 'travel', 'author': 'Nick Name', 'headline': 'Путешествия',
         'content': 'Вот это новость 29. Новость. Новость. Новость. Новость. Новость.',
         'banner': 'img/cat-500x80-3.jpg', 'pub_date': '2023-11-29 5:00'},
        {'id': 30, 'category': 'travel', 'author': 'Nick Name', 'headline': 'Путешествия',
         'content': 'Вот это новость 30. Новость. Новость. Новость. Новость. Новость.',
         'banner': 'img/cat-500x80-3.jpg', 'pub_date': '2023-11-30 6:00'},

        {'id': 31, 'category': 'lifestyle', 'author': 'Nick Name', 'headline': 'Стиль жизни',
         'content': 'Вот это новость 31. Новость. Новость. Новость. Новость. Новость.',
         'banner': 'img/cat-500x80-4.jpg', 'pub_date': '2023-12-01 7:00'},
        {'id': 32, 'category': 'lifestyle', 'author': 'Nick Name', 'headline': 'Стиль жизни',
         'content': 'Вот это новость 32. Новость. Новость. Новость. Новость. Новость.',
         'banner': 'img/cat-500x80-4.jpg', 'pub_date': '2023-12-03 8:00'},
    ]
    for news in all_news_list:
        category_pk = get_category_pk_by_id(news.get('category'))
        news.update({
            'category_pk': category_pk,
        })
    return all_news_list


def get_news_list(category_name: str = ''):
    all_news_list = get_all_news_list()
    if category_name == '':
        return all_news_list
    news_list = [item for item in all_news_list if item.get('category') == category_name]
    # print(news_list)
    return news_list


def get_news_list_pk(category_pk: int = 0):
    all_news_list = get_all_news_list()
    if category_pk == 0:
        return all_news_list
    category_id = get_category_id(category_pk)
    news_list = [item for item in all_news_list if item.get('category') == category_id]
    # print(news_list)
    return news_list


def get_comments_list(news_id: int = 1):
    if news_id == 1:
        return [
            {'id': 1, 'news': 1, 'user_name': 'John Doe',
             'message': 'Комментарий 1. Комментарий. Комментарий. Комментарий. Комментарий. Комментарий.',
             'pub_date': '2023-11-01 1:00'},
            {'id': 2, 'news': 1, 'user_name': 'John Doe',
             'message': 'Комментарий 2. Комментарий. Комментарий. Комментарий. Комментарий. Комментарий.',
             'pub_date': '2023-11-02 2:00'},
            {'id': 3, 'news': 1, 'user_name': 'John Doe',
             'message': 'Комментарий 3. Комментарий. Комментарий. Комментарий. Комментарий. Комментарий.',
             'pub_date': '2023-11-03 3:00'},
            {'id': 4, 'news': 1, 'user_name': 'John Doe',
             'message': 'Комментарий 4. Комментарий. Комментарий. Комментарий. Комментарий. Комментарий.',
             'pub_date': '2023-11-04 4:00'},
        ]
    if news_id == 2:
        return [
            {'id': 1, 'news': 2, 'user_name': 'Jane Doe',
             'message': 'Комментарий 1. Комментарий. Комментарий. Комментарий. Комментарий. Комментарий.',
             'pub_date': '2023-11-01 1:00'},
            {'id': 2, 'news': 2, 'user_name': 'Jane Doe',
             'message': 'Комментарий 2. Комментарий. Комментарий. Комментарий. Комментарий. Комментарий.',
             'pub_date': '2023-11-02 2:00'},
            {'id': 3, 'news': 2, 'user_name': 'Jane Doe',
             'message': 'Комментарий 3. Комментарий. Комментарий. Комментарий. Комментарий. Комментарий.',
             'pub_date': '2023-11-03 3:00'},
            {'id': 4, 'news': 2, 'user_name': 'Jane Doe',
             'message': 'Комментарий 4. Комментарий. Комментарий. Комментарий. Комментарий. Комментарий.',
             'pub_date': '2023-11-04 4:00'},
        ]
    if news_id == 3:
        return [
            {'id': 1, 'news': 3, 'user_name': 'Jane Doe',
             'message': 'Комментарий 1. Комментарий. Комментарий. Комментарий. Комментарий. Комментарий.',
             'pub_date': '2023-11-01 1:00'},
            {'id': 2, 'news': 3, 'user_name': 'Jane Doe',
             'message': 'Комментарий 2. Комментарий. Комментарий. Комментарий. Комментарий. Комментарий.',
             'pub_date': '2023-11-02 2:00'},
            {'id': 3, 'news': 3, 'user_name': 'Jane Doe',
             'message': 'Комментарий 3. Комментарий. Комментарий. Комментарий. Комментарий. Комментарий.',
             'pub_date': '2023-11-03 3:00'},
            {'id': 4, 'news': 3, 'user_name': 'Jane Doe',
             'message': 'Комментарий 4. Комментарий. Комментарий. Комментарий. Комментарий. Комментарий.',
             'pub_date': '2023-11-04 4:00'},
        ]


def get_main_news_list():
    main_news_list = []
    for news in get_news_list()[4:4+6]:
        new_news = news.copy()
        category_name = get_category_name(news.get('category'))
        # print('category_name')
        # print(category_name)
        category_pk = get_category_pk_by_id(news.get('category'))
        # print('category_pk')
        # print(category_pk)
        new_news.update({
            'category_pk': category_pk,
            'category_name': category_name,
        })
        main_news_list.append(new_news)
    # print(main_news_list)
    return main_news_list


def get_category_news_dict():
    main_news_dict = {}
    for news in get_news_list()[0:16]:
        new_news = news.copy()
        category_name = get_category_name(news.get('category'))
        category_pk = get_category_pk_by_id(news.get('category'))
        new_news.update({
            'category_pk': category_pk,
            'category_name': category_name,
        })
        if category_name in main_news_dict:
            lst = main_news_dict.get(category_name)
            lst.append(new_news)
        else:
            main_news_dict.update({category_name: [new_news]})
    # print(main_news_dict)
    return main_news_dict


def get_categories_news_list():
    categories_news_list = []
    for news in get_news_list():
        new_news = news.copy()
        category_name = get_category_name(news.get('category'))
        new_news.update({'category_name': category_name})
        categories_news_list.append(new_news)
    # print(categories_news_list)
    return categories_news_list


def get_news(id):
    for item in get_news_list():
        if item.get('id') == id:
            new_news = item.copy()
            category_name = get_category_name(item.get('category'))
            new_news.update({'category_name': category_name})
            return new_news


def index(request):
    context = {'title': 'Главная страница',
               'navbar': navbar_active('home'),
               'category_title': 'Категории',
               'category_list': get_category_list(),
               # 'category_list_db': get_category_list_db(),
               'main_news_list': get_main_news_list(),
               'category_news_dict': get_category_news_dict(),
               'news_list': get_news_list(),
               }
    # return HttpResponse('<h1> Главная страница </h1>')
    return render(request, 'main/index.html', context)


def categories(request):
    # print(name)
    context = {'title': 'Категории',
               'navbar': navbar_active('category'),
               'category_title': 'Категории',
               'category_list': get_category_list(),
               'categories_news_list': get_categories_news_list(),
               }
    return render(request, 'main/categories.html', context)


def category(request, title):
    # print(name)
    context = {'title': 'Категория',
               'navbar': navbar_active('category'),
               'category_title': 'Категории',
               'category_list': get_category_list(),
               'category_name': get_category_name(title),
               'news_list': get_news_list(title),
               }
    return render(request, 'main/category.html', context)


def news(request, pk):
    context = {'title': 'Новость',
               'navbar': navbar_active('news'),
               'category_title': 'Категории',
               'category_list': get_category_list(),
               'news': get_news(pk),
               'comment_list': get_comments_list(pk),
               }
    return render(request, 'main/news.html', context)


def profile(request):
    context = {'title': 'Пользователь',
               'navbar': navbar_active('profile'),
               'category_title': 'Категории',
               'category_list': get_category_list(),
               'profile': request.user,
               }
    return render(request, 'main/profile.html', context)


def contacts(request):
    context = {'title': 'Контакты',
               'navbar': navbar_active('contacts'),
               'category_title': 'Категории',
               'category_list': get_category_list(),
               }
    return render(request, 'main/contacts.html', context)
    # return HttpResponse('<h1> Контакты </h1>')


def page_not_found(request, exception):
    return render(request, 'page_404.html')


def formcats(request):
    form = forms.CategoryForm()

    if request.method == 'POST':
        new_item = forms.CategoryForm(request.POST, request.FILES)
        new_item.save()

    context = {
        'form': form,
    }
    return render(request, 'main/image_form.html', context)


def get_image(request):
    model = models.Categories.objects.all().first()
    context = {
        'model': model,
    }
    return render(request, 'main/image_form.html', context)


class IndexView(generic.TemplateView):
    template_name = 'main/index.html'
    # model = models.Article
    # form_class = forms.ArticleForm
    # success_url = reverse_lazy('main:home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        main_article_list: list = []
        for category in models.Category.objects.all().values('pk', 'title'):
            article = models.Article.objects.filter(category=category.get('pk')).order_by('-views__count').\
                select_related('category', 'views').\
                values('pk', 'title', 'content', 'banner', 'created_at',
                       'category__pk', 'category__title', 'views__count').first()
            if article is not None:
                # print(article)

                # count_views = models.ArticleViews.objects.get(article=article.get('pk')).count_views
                # print(count_views)

                main_article_list.append(article)
                # main_article_list.append({
                #     'category': category,
                #     'article': article,
                # })
        # print(main_article_list)

        category_article_list: list = []
        for category in models.Category.objects.all().values('pk', 'title')[:4]:
            article_list = models.Article.objects.filter(category=category.get('pk')).order_by('-created_at').values(
                'pk', 'title', 'content', 'banner', 'created_at', 'category__pk', 'category__title')[:4]
            if article_list.exists():
                category_article_list.append({
                    'category': category,
                    'article_list': article_list,
                })

        # print(get_category_list_db())
        # dt = forms.get_datetime_now()
        # print(f'{dt=}')
        # context['work_create_dt_date'] = f'{dt.year:04}-{dt.month:02}-{dt.day:02}'
        # context['work_create_dt_time'] = f'{dt.hour:02}:{dt.minute:02}'
        context.update({
            'title': 'Главная страница',
            'navbar': navbar_active('home'),
            # 'category_list': get_category_list(),
            # 'category_list_db': get_category_list_db(),
            # 'user_list': get_user_list_db(),
            # 'category_list': get_category_list_db(),
            # 'tag_list': get_tag_list_db(),

            # 'main_news_list': get_main_news_list(),
            'main_article_list': main_article_list,
            # 'category_news_dict': get_category_news_dict(),
            # 'news_list': get_news_list(),
            'category_article_list': category_article_list,
        })
        context.update(get_db_lists())
        return context


"""
def categories(request):
    # print(name)
    context = {'title': 'Категории',
               'navbar': navbar_active('category'),
               'category_title': 'Категории',
               'category_list': get_category_list(),
               'categories_news_list': get_categories_news_list(),
               }
    return render(request, 'main/categories.html', context)
"""


class CategoriesView(generic.TemplateView):
    template_name = 'main/categories.html'
    # model = models.Article
    # context_object_name = 'article_list'

    """
    def _get_data(self, query):
        return query.order_by('-created_at').values(
            'pk', 'title', 'content', 'banner', 'created_at', 'category__pk', 'category__title')
    """

    """
    def get_queryset(self):
        category_list = models.Category.objects.all()
        # print(category_list)
        articles_list = models.Article.objects.none()
        for category in category_list:
            category_article_list = models.Article.objects.filter(category=category).order_by('-created_at')[:4]
            # print(category_article_list)
            if category_article_list.exists():
                articles_list |= category_article_list
                print(category_article_list)
            # print(category['id'])

        print(articles_list.order_by('category__title', '-created_at'))
        # self.category = self.request.GET.get('id')
        # pk = self.kwargs.get('pk')
        # return self._get_data(models.Article.objects.filter(category=pk))
        # return self.get_data(models.Article.objects.all()) if pk is None else \
        #     self.get_data(models.Article.objects.filter(category=pk))
    """

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_article_list: list = []
        for category in models.Category.objects.all().values('pk', 'title'):
            article_list = models.Article.objects.filter(category=category.get('pk'))[:4]
            # article_list = models.Article.objects.filter(category=category.get('pk')).\
            #     order_by('-created_at').select_related('category', 'views').\
            #     values('pk', 'title', 'annotation', 'content', 'banner', 'created_at',
            #            'category__pk', 'category__title', 'views__count')[:4]
            if article_list.exists():
                category_article_list.append({
                    'category': category,
                    'article_list': article_list,
                })

        # print('category_article_list')
        # print(category_article_list)
        # print(context)
        # dt = forms.get_datetime_now()
        # print(f'{dt=}')
        # context['work_create_dt_date'] = f'{dt.year:04}-{dt.month:02}-{dt.day:02}'
        # context['work_create_dt_time'] = f'{dt.hour:02}:{dt.minute:02}'
        context.update({
            'title': 'Категории',
            'navbar': navbar_active('category'),
            # 'category_list': get_category_list_db(),
            # 'tag_list': get_tag_list_db(),
            'category_article_list': category_article_list,
        })
        context.update(get_db_lists())
        return context


class CategoryView(generic.ListView):
    template_name = 'main/category.html'
    model = models.Article
    context_object_name = 'article_list'

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        return models.Article.objects.filter(category=pk).order_by('-created_at')
        # return models.Article.objects.filter(category=pk).order_by('-created_at').values(
        #     'pk', 'title', 'annotation', 'content', 'banner',
        #     'created_by', 'created_by__username', 'created_by__first_name', 'created_by__last_name', 'created_at',
        #     'category__pk', 'category__title', 'views__count')

    def get_context_data(self, **kwargs):
        pk = self.kwargs.get('pk')
        context = super().get_context_data(**kwargs)

        category_object = models.Category.objects.filter(pk=pk)
        if not category_object.exists():
            raise Http404
        category_item = category_object.get()
        # print(f'{user=}')
        # print(context)
        # dt = forms.get_datetime_now()
        # print(f'{dt=}')
        # context['work_create_dt_date'] = f'{dt.year:04}-{dt.month:02}-{dt.day:02}'
        # context['work_create_dt_time'] = f'{dt.hour:02}:{dt.minute:02}'
        context.update({
            'title': 'Категория',
            'navbar': navbar_active('category'),
            # 'category_title': 'Категории',
            'category': category_item,
            # 'category_list': get_category_list_db(),
            # 'tag_list': get_tag_list_db(),
            # 'category_name': get_category_name_by_pk(context.get('pk')),
            # 'news_list': get_news_list_pk(context.get('pk')),
        })
        context.update(get_db_lists())
        return context


"""
class ArticleView(generic.TemplateView):
    template_name = 'main/news.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'Новость',
            'navbar': navbar_active('news'),
            # 'category_list': get_category_list_db(),
            # 'tag_list': get_tag_list_db(),
            'news': get_news(context.get('pk')),
            'comment_list': get_comments_list(context.get('pk')),
        })
        context.update(get_db_lists())
        return context
"""


class ArticleDetailView(generic.edit.FormMixin, generic.DetailView):
    template_name = 'main/article_detail.html'
    model = models.Article
    context_object_name = 'article'
    form_class = forms.CommentForm
    # success_url = reverse_lazy('main:article_detail' kwargs={'pk': self.object.id})

    def get_success_url(self):
        return reverse_lazy('main:article_detail', kwargs={'pk': self.get_object().pk})

    def post(self, request, **kwargs):
        # print('post')
        user = request.user
        # print(user)
        article = self.get_object()
        # print(article)
        # print(request.POST)
        message = request.POST.get('message')
        # print(message)
        if len(message) > 0:
            models.Comment.objects.create(
                article=article,
                message=message,
                created_by=request.user)
        form = self.get_form()
        # return self.form_valid(form)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    # def form_valid(self, form):
        # print('form_valid')
        # instance = self.get_object()
        # form.instance.article = instance
        # form.instance.created_by = self.request.user
        # form.save()
    #     return super().form_valid(form)

    def get_context_data(self, **kwargs):
        # print('get_context_data')
        instance = self.get_object()
        instance.views.count += 1
        instance.views.save()
        # print(f'{instance.views.count=}')

        comment_list = models.Comment.objects.filter(article=instance).order_by('-created_at')

        # from django.db.models import F
        # from myapp.models import Product
        # Product.objects.update(price=F('price') * 1.1)

        # article_views = models.ArticleViews.objects.get(pk=self.kwargs.get('pk'))
        # print(f'{article_views=}')
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'Статья',
            'navbar': navbar_active('article'),
            'article_count_views': instance.views.count,
            'comment_list': comment_list,
        })
        context.update(get_db_lists())
        return context


class ArticleCreateView(generic.edit.CreateView):
    template_name = 'main/article_create.html'
    model = models.Article
    form_class = forms.ArticleForm
    success_url = reverse_lazy('main:home')

    def form_valid(self, form):
        # offset: str = '+0500'
        # date_name: str = self.request.POST.get('work_create_dt_date')
        # time_name: str = self.request.POST.get('work_create_dt_time')
        # print(f'{date_name=}')
        # print(datetime.strptime(f'{date_name} {time_name}{offset}', '%Y-%m-%d %H:%M%z'))
        # form.instance.dt = datetime.strptime(f'{date_name} {time_name}{offset}', '%Y-%m-%d %H:%M%z')
        form.instance.created_by = self.request.user

        views = models.Views.objects.create(count=0)
        form.instance.views = views

        # form.instance.created_name = form.get_name(self.request.user)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # dt = forms.get_datetime_now()
        # print(f'{dt=}')
        # context['work_create_dt_date'] = f'{dt.year:04}-{dt.month:02}-{dt.day:02}'
        # context['work_create_dt_time'] = f'{dt.hour:02}:{dt.minute:02}'
        context.update({
            'title': 'Новая статья',
            'navbar': navbar_active('article'),
            # 'category_list': get_category_list_db(),
            # 'tag_list': get_tag_list_db(),
            # 'news': get_news(context.get('pk')),
            # 'comment_list': get_comments_list(context.get('pk')),
        })
        context.update(get_db_lists())
        return context


class ArticleUpdateView(generic.UpdateView):
    template_name = 'main/article_update.html'
    model = models.Article
    form_class = forms.ArticleForm
    success_url = reverse_lazy('main:home')
    # fields = ['title','anouncement','text','tags']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # dt = forms.get_datetime_now()
        # print(f'{dt=}')
        # context['work_create_dt_date'] = f'{dt.year:04}-{dt.month:02}-{dt.day:02}'
        # context['work_create_dt_time'] = f'{dt.hour:02}:{dt.minute:02}'
        context.update({
            'title': 'Изменить статью',
            'navbar': navbar_active('news'),
            'category_title': 'Категории',
            # 'category_list': get_category_list_db(),
            # 'tag_list': get_tag_list_db(),
        })
        context.update(get_db_lists())
        return context


class ArticleDeleteView(generic.DeleteView):
    template_name = 'main/article_delete.html'
    model = models.Article
    success_url = reverse_lazy('main:home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # dt = forms.get_datetime_now()
        # print(f'{dt=}')
        # context['work_create_dt_date'] = f'{dt.year:04}-{dt.month:02}-{dt.day:02}'
        # context['work_create_dt_time'] = f'{dt.hour:02}:{dt.minute:02}'
        context.update({
            'title': 'Удалить статью',
            'navbar': navbar_active('news'),
            'category_title': 'Категории',
            # 'category_list': get_category_list_db(),
            # 'tag_list': get_tag_list_db(),
        })
        context.update(get_db_lists())
        return context


class FindView(generic.ListView):
    template_name = 'main/find.html'
    model = models.Article
    context_object_name = 'article_list'

    def add_to_query(self, value):
        return None if value in ('', None) else Q(title__icontains=value)

    def _get_objects(self, query):
        return models.Article.objects.all() if query is None else models.Article.objects.filter(query)

    def get_queryset(self):
        filter_value = self.request.GET.get('filter')
        # print(f'{filter_value=}')
        query = self.add_to_query(filter_value)
        return self._get_objects(query).order_by('-created_at').values(
            'pk', 'title', 'annotation', 'content', 'banner', 'created_at',
            'category__pk', 'category__title', 'views__count')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'Поиск',
            'navbar': navbar_active('find'),
            # 'category_title': 'Категории',
            # 'category_list': get_category_list_db(),
            # 'tag_list': get_tag_list_db(),
            # 'news': get_news(context.get('pk')),
            # 'comment_list': get_comments_list(context.get('pk')),
        })
        context.update(get_db_lists())
        return context


class TagsView(generic.edit.FormMixin, generic.ListView):
    template_name = 'main/tags.html'
    model = models.Article
    context_object_name = 'article_list'
    form_class = forms.TagsForm
    form = None
    tags = None

    def add_to_query(self, value):
        return None if value in ('', None) else Q(tags__in=value)

    def _get_objects(self, query):
        return models.Article.objects.none()\
            if query is None\
            else models.Article.objects.filter(query).distinct()

    # def get_success_url(self):
    #     return reverse_lazy('main:tags')

    # def get(self, request, *args, **kwargs):
    #     self.tags_form = forms.TagsForm(self.request.GET or None,)
    #     return super().get(request, *args, **kwargs)

    def get_queryset(self):
        # print('get_queryset')
        # tags = None
        self.form = forms.TagsForm(self.request.GET or None)
        self.tags = self.request.GET.getlist('tags')
        # if self.request.GET.getlist('tags'):
        #     self.tags = self.request.GET.getlist('tags')
        query = self.add_to_query(self.tags)
        objects = self._get_objects(query)
        return objects.order_by('-created_at')

    def get_context_data(self, **kwargs):
        # print('get_context_data')
        # print(f'{self.tags=}')
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'Тэги',
            'navbar': navbar_active('tags'),
            'tags': self.tags,
            'form': self.form,
        })
        context.update(get_db_lists())
        return context


class ContactView(generic.TemplateView):
    template_name = 'main/contacts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'Контакты',
            'navbar': navbar_active('contacts'),
        })
        context.update(get_db_lists())
        return context


# , mixins.PermissionRequiredMixin
class ProfileView(mixins.LoginRequiredMixin, generic.TemplateView):
    template_name = 'main/profile.html'
    # model = models.Account
    # form_class = forms.ProfileForm
    # success_url = reverse_lazy('main:home')

    # def form_valid(self, form):
    #     form.instance.user = self.request.user
    #     print('form_valid')
    #     print(form.instance)
    #     # form.fill(self.request.user)
    #     return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.request.user.pk
        account = None
        user_object = User.objects.filter(pk=pk)
        if not user_object.exists():
            raise Http404
        user = user_object.get()
        # print(f'{user=}')
        account_object = models.Account.objects.filter(pk=pk)
        if account_object.exists():
            account = account_object.get()
            # print(acc.get_gender_display())
            # account = account_object.values('nickname', 'birthday', 'gender', 'avatar').first()
            # print(f'{account=}')
        # article_list = models.Article.objects.filter(created_by=pk).order_by('-created_at').values(
        #     'pk', 'title', 'annotation', 'banner',
        #     'created_by', 'created_by__username', 'created_by__first_name', 'created_by__last_name', 'created_at',
        #     'category__pk', 'category__title', 'views__count')
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'Профиль пользователя',
            'navbar': navbar_active('profile'),
            'user': user,
            'account': account,
            # 'article_list': article_list,
        })
        context.update(get_db_lists())
        return context


class ProfileArticlesView(generic.ListView):
    template_name = 'main/profile_articles.html'
    model = models.Article
    context_object_name = 'article_list'

    # def add_to_query(self, value):
    #     return None if value in ('', None) else Q(title__icontains=value)

    # def _get_objects(self, query):
    #     return models.Article.objects.all() if query is None else models.Article.objects.filter(query)

    def get_queryset(self):
        user = self.request.user
        # print(user)
        return models.Article.objects.filter(created_by=user).order_by('-created_at').values(
            'pk', 'title', 'annotation', 'content', 'banner', 'created_at',
            'category__pk', 'category__title', 'views__count')
        # filter_value = self.request.GET.get('filter')
        # print(f'{filter_value=}')
        # query = self.add_to_query(filter_value)
        # return self._get_objects(query).order_by('-created_at').values(
        #     'pk', 'title', 'annotation', 'content', 'banner', 'created_at',
        #     'category__pk', 'category__title', 'views__count')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'Мои статьи',
            'navbar': navbar_active('profile'),
            # 'category_title': 'Категории',
            # 'category_list': get_category_list_db(),
            # 'tag_list': get_tag_list_db(),
            # 'news': get_news(context.get('pk')),
            'comment_list': get_comments_list(context.get('pk')),
        })
        context.update(get_db_lists())
        return context


class UserView(generic.TemplateView):
    template_name = 'main/user.html'
    # model = User
    # context_object_name = 'account'
    # form_class = forms.ProfileForm
    # success_url = reverse_lazy('main:home')

    # def form_valid(self, form):
    #     form.fill(self.request.user)
    #     return super().form_valid(form)

    def get_context_data(self, **kwargs):
        pk = self.kwargs.get('pk')
        # user = None
        account = None
        user_object = User.objects.filter(pk=pk)
        if not user_object.exists():
            raise Http404
        user = user_object.get()
        # print(f'{user=}')
        account_object = models.Account.objects.filter(pk=pk)
        if account_object.exists():
            account = account_object.get()
            # print(acc.get_gender_display())
            # account = account_object.values('nickname', 'birthday', 'gender', 'avatar').first()
            # print(f'{account=}')
        article_list = models.Article.objects.filter(created_by=pk).order_by('-created_at').values(
            'pk', 'title', 'annotation', 'banner',
            'created_by', 'created_by__username', 'created_by__first_name', 'created_by__last_name', 'created_at',
            'category__pk', 'category__title', 'views__count')
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'Профиль автора',
            'navbar': navbar_active('user'),
            'user': user,
            'account': account,
            'article_list': article_list,
        })
        context.update(get_db_lists())
        return context


"""
class ProfileUpdateView(generic.FormView):
    template_name = 'main/profile_update.html'
    form_class = forms.ProfileUpdateForm
    success_url = reverse_lazy('main:home')

    def form_valid(self, form, **kwargs):
        print('form.valid')
        form.update(self.request.user)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        pk = self.request.user.pk
        account = None
        user_object = User.objects.filter(pk=pk)
        if not user_object.exists():
            raise Http404
        user = user_object.get()
        # print(f'{user=}')
        account_object = models.Account.objects.filter(pk=pk)
        if account_object.exists():
            account = account_object.get()
            # print(acc.get_gender_display())
            # account = account_object.values('nickname', 'birthday', 'gender', 'avatar').first()
            # print(f'{account=}')
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'Профиль пользователя',
            'navbar': navbar_active('user'),
            'user': user,
            'account': account,
        })
        context.update(get_db_lists())
        return context
"""


class ProfileUpdateMultiView(generic.FormView):
    template_name = 'main/profile_update.html'
    form_class = forms.ProfileUpdateMultiForm
    success_url = reverse_lazy('main:profile')

    def get_form_kwargs(self):
        # print('get_form_kwargs')
        kwargs = super(ProfileUpdateMultiView, self).get_form_kwargs()
        kwargs.update(instance={
            'user': self.request.user,
            'account': models.Account.objects.filter(pk=self.request.user.pk).get(),
        })
        return kwargs

    def form_valid(self, form, **kwargs):
        # print('form_valid')
        # form.update(self.request.user)
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        pk = self.request.user.pk
        account = None
        user_object = User.objects.filter(pk=pk)
        if not user_object.exists():
            raise Http404
        user = user_object.get()
        # print(f'{user=}')
        account_object = models.Account.objects.filter(pk=pk)
        if account_object.exists():
            account = account_object.get()
            # print(acc.get_gender_display())
            # account = account_object.values('nickname', 'birthday', 'gender', 'avatar').first()
            # print(f'{account=}')
        else:
            account_object = models.Account.objects.create(user=user)
            account = account_object
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'Профиль пользователя',
            'navbar': navbar_active('profile'),
        })
        context.update(get_db_lists())
        return context


"""
class ArchiveView(generic.ListView):
    template_name = 'main/archive.html'
    model = models.Article
    context_object_name = 'article_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'Архив статей',
            'navbar': navbar_active('archive'),
        })
        context.update(get_db_lists())
        return context
"""


class ArchiveArticleView(generic.dates.ArchiveIndexView):
    template_name = 'main/archive_article.html'
    model = models.Article
    context_object_name = 'article_list'
    date_field = 'created_at'
    allow_future = False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'Архив статей',
            'navbar': navbar_active('archive'),
        })
        context.update(get_db_lists())
        return context


class ArchiveArticleYearView(generic.dates.YearArchiveView):
    template_name = 'main/archive_article_year.html'
    queryset = models.Article.objects.all()
    context_object_name = 'article_list'
    date_field = 'created_at'
    make_object_list = True
    allow_future = False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'Архив статей',
            'navbar': navbar_active('archive'),
        })
        context.update(get_db_lists())
        return context


class ArchiveArticleMonthView(generic.dates.MonthArchiveView):
    template_name = 'main/archive_article_month.html'
    queryset = models.Article.objects.all()
    context_object_name = 'article_list'
    month_format = '%m'
    date_field = 'created_at'
    allow_future = False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'Архив статей',
            'navbar': navbar_active('archive'),
        })
        context.update(get_db_lists())
        return context


class ArchiveArticleDayView(generic.dates.DayArchiveView):
    template_name = 'main/archive_article_day.html'
    queryset = models.Article.objects.all()
    context_object_name = 'article_list'
    month_format = '%m'
    day_format = '%d'
    date_field = 'created_at'
    allow_future = False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'Архив статей',
            'navbar': navbar_active('archive'),
        })
        context.update(get_db_lists())
        return context
