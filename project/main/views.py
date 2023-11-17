from django.shortcuts import render
from django.http import HttpResponse

from . import models
from . import forms


def navbar_active(page: str):
    navbar: dict = {
        'home': '',
        'category': '',
        'news': '',
        'contacts': '',
    }
    navbar.update({page: 'active'})
    # print(navbar)
    return navbar


def get_category_list(category_id=''):
    all_category_list = [
        {'id': 'business', 'name': 'Бизнес', 'banner': 'img/cat-500x80-1.jpg'},
        {'id': 'technology', 'name': 'Технологии', 'banner': 'img/cat-500x80-2.jpg'},
        {'id': 'entertainment', 'name': 'Развлечения', 'banner': 'img/cat-500x80-3.jpg'},
        {'id': 'sports', 'name': 'Спорт', 'banner': 'img/cat-500x80-4.jpg'},
        {'id': 'politics', 'name': 'Политика', 'banner': 'img/cat-500x80-1.jpg'},
        {'id': 'corporate', 'name': 'Корпорации', 'banner': 'img/cat-500x80-2.jpg'},
        {'id': 'health', 'name': 'Здоровье', 'banner': 'img/cat-500x80-3.jpg'},
        {'id': 'education', 'name': 'Образование', 'banner': 'img/cat-500x80-4.jpg'},
        {'id': 'science', 'name': 'Наука', 'banner': 'img/cat-500x80-1.jpg'},
        {'id': 'foods', 'name': 'Еда', 'banner': 'img/cat-500x80-2.jpg'},
        {'id': 'travel', 'name': 'Путешествия', 'banner': 'img/cat-500x80-3.jpg'},
        {'id': 'lifestyle', 'name': 'Стиль жизни', 'banner': 'img/cat-500x80-4.jpg'},
    ]
    # if category_id == '':
    #     return all_category_list
    # category_list = [item for item in all_category_list if item.get('id') == category_id]
    # return category_list
    return all_category_list


def get_category_name(category_id):
    for item in get_category_list():
        if item.get('id') == category_id:
            return item.get('name')
    return ''


def get_news_list(category_name: str = ''):
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
    if category_name == '':
        return all_news_list
    news_list = [item for item in all_news_list if item.get('category') == category_name]
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


def category(request, name):
    # print(name)
    context = {'title': 'Категория',
               'navbar': navbar_active('category'),
               'category_title': 'Категории',
               'category_list': get_category_list(),
               'category_name': get_category_name(name),
               'news_list': get_news_list(name),
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
               'navbar': navbar_active('home'),
               'category_title': 'Категории',
               'category_list': get_category_list(),
               # 'news': get_news(pk),
               # 'comment_list': get_comments_list(pk),
               'profile': 'profile',
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
