import sys
import django

from django.conf import settings
from django.contrib.auth import mixins
from django.contrib.auth.models import User, Group, AnonymousUser
from django.db import connection
from django.db.models import Q
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import generic
# from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

from . import models
from . import forms


def navbar_active(page: str):
    navbar: dict = {
        'home': '',
        'category': '',
        'categories': '',
        'user': '',
        'article': '',
        'article_create': '',
        'find': '',
        'tags': '',
        'archive': '',
        'contacts': '',
        'about': '',
        'profile': '',
        'profile_articles': '',
        'profile_favorites': '',
        'signup': '',
    }
    # navbar.update({'article': 'd-none'})
    navbar.update({'find': 'd-none'})
    # navbar.update({'tags': 'd-none'})
    # navbar.update({'archive': 'd-none'})
    # navbar.update({'contacts': 'd-none'})
    # navbar.update({'profile': 'd-none'})
    navbar.update({page: 'active'})
    return navbar


def get_db_lists():

    # user_list = User.objects.filter(groups__name='Писатели').all().values('id', 'username', 'first_name', 'last_name')
    # user_list = User.objects.annotate(
    #     no_of_pub = Count('id', filter=Q(author__status="PUBLISHED")),
    #     no_of_books_on_hold = Count('id', filter=Q(author__status="ON_HOLD")).
    #     filter(groups__name='Писатели').all().values('id', 'username', 'first_name', 'last_name')
    # authors = models.Article.objects.all().values('created_by').annotate(total=Count('created_by'), distinct=True).order_by('created_by__username')
    # authors = models.Article.objects.all().values('created_by').annotate(total=Count('created_by')).order_by('created_by__username')
    # authors = models.Article.objects.all().values('created_by__last_name').annotate(total=Count('created_by')).order_by('created_by__username')
    # authors = models.Article.objects.all().distinct('created_by')
    # q = ProductOrder.objects.values('Category').distinct()
    # authors = User.objects.annotate(
    #     no_of_pub=Count('id')
    # ).filter(no_of_pub__gt=0).order_by('-no_of_pub')
    user_list: list = []
    authors = User.objects.filter(groups__name='Писатели').order_by('username').all()
    for author in authors:
        articles_count = models.Article.objects.filter(created_by=author).count()
        if articles_count > 0:
            user_list.append(author)

    category_list = models.Category.objects.all()
    tag_list = models.Tag.objects.all()
    return {
        'user_list': user_list,
        'category_list': category_list,
        'tag_list': tag_list,
    }


def page_not_found(request, exception):
    return render(request, 'page_404.html')


class IndexView(generic.TemplateView):
    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        main_article_list: list = []
        for category in models.Category.objects.all().values('pk', 'title'):
            article = models.Article.objects.filter(category=category.get('pk')).order_by('-views__count'). \
                select_related('category', 'views').first()
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
        for category in models.Category.objects.all().values('pk', 'title'):
            article_list = models.Article.objects.filter(category=category.get('pk')).order_by('-created_at')[:4]
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
            'main_article_list': main_article_list,
            'category_article_list': category_article_list,
        })
        context.update(get_db_lists())
        return context


class CategoriesView(generic.TemplateView):
    template_name = 'main/categories.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_article_list: list = []
        for category in models.Category.objects.all().values('pk', 'title'):
            article_list = models.Article.objects.filter(category=category.get('pk'))[:2]
            if article_list.exists():
                category_article_list.append({
                    'category': category,
                    'article_list': article_list,
                })
        context.update({
            'title': 'Категории',
            'navbar': navbar_active('categories'),
            'category_article_list': category_article_list,
        })
        context.update(get_db_lists())
        return context


from django.db.models import Subquery, OuterRef, Count


class CategoryView(generic.ListView):
    template_name = 'main/category.html'
    model = models.Article
    context_object_name = 'article_list'
    paginate_by = 4

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        # subquery = models.FavoriteArticle.objects.filter(article=OuterRef('pk'), created_by=self.request.user).count()
        # .annotate(
        #     name=Subquery(
        #         Team.objects.filter(
        #             id=OuterRef('team_id')
        #         ).values('name')
        # return models.Article.objects.filter(category=pk).order_by('-created_at').annotate(
        #         favorites_count=Subquery(
        #             models.FavoriteArticle.objects.filter(
        #                 article=OuterRef('id'), created_by=self.request.user).annotate(
        #                     count=Count('id')).values('count')
        #         )
        # )
        return models.Article.objects.filter(
            category=pk).order_by('-created_at')  # .annotate(favorites_count=Subquery(subquery))

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
            'category': category_item,
        })
        context.update(get_db_lists())
        return context


class ArticleDetailView(generic.edit.FormMixin, generic.DetailView):
    template_name = 'main/article_detail.html'
    model = models.Article
    context_object_name = 'article'
    form_class = forms.CommentForm

    # form_class = forms.FavoriteArticleCommentMultiForm
    # success_url = reverse_lazy('main:article_detail' kwargs={'pk': self.object.id})

    def get_success_url(self):
        # print('get_success_url')
        return reverse_lazy('main:article_detail', kwargs={'pk': self.get_object().pk})

    """
    def get_form_kwargs(self):
        print('get_form_kwargs')
        kwargs = super().get_form_kwargs()
        kwargs.update(instance={
            'favorites': '',
            'comment': self.request.POST.get('message'),
        })
        return kwargs
    """

    def post(self, request, **kwargs):
        # print('post')
        # post = request.POST
        # print(post)
        user = request.user
        print(user)
        article = self.get_object()
        if 'favorites_add' in request.POST:
            # print('favorites_add')
            models.FavoriteArticle.objects.update_or_create(article=article, created_by=user)
        elif 'favorites_del' in request.POST:
            # print('favorites_del')
            models.FavoriteArticle.objects.filter(article=article, created_by=user).delete()
        elif 'comment_add' in request.POST:
            # print('comment_add')
            message = request.POST.get('message')
            # print(message)
            if len(message) > 0:
                models.Comment.objects.create(article=article, message=message, created_by=request.user)
        elif 'comment_del' in request.POST:
            # print('comment_del')
            comment_id = request.POST.get('comment_del')
            # print(comment_id)
            models.Comment.objects.filter(pk=comment_id, created_by=user).delete()

        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        # print('get_context_data')
        instance = self.get_object()
        # print(instance)
        instance.views.count += 1
        instance.views.save()
        # print(f'{self.request.user=}')

        comment_list = models.Comment.objects.filter(article=instance).order_by('-created_at')
        favorites_count = None
        if self.request.user.is_authenticated:
            favorites_count = models.FavoriteArticle.objects.filter(
                article=instance,
                created_by=self.request.user).count()
        # print(f'{favorites_count=}')

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
            'favorites_count': favorites_count
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
            'navbar': navbar_active('article_create'),
        })
        context.update(get_db_lists())
        return context


class ArticleUpdateView(generic.UpdateView):
    template_name = 'main/article_update.html'
    model = models.Article
    form_class = forms.ArticleForm
    success_url = reverse_lazy('main:home')

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
        return self._get_objects(query).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'Поиск',
            'navbar': navbar_active('find'),
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
        return models.Article.objects.none() \
            if query is None \
            else models.Article.objects.filter(query).distinct()

    # def get_success_url(self):
    #     return reverse_lazy('main:tags')

    def get(self, request, *args, **kwargs):
        self.form = forms.TagsForm(self.request.GET or None)
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        # print('get_queryset')
        # tags = None
        # self.form = forms.TagsForm(self.request.GET or None)
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


class AboutView(generic.TemplateView):
    template_name = 'main/about.html'

    def get_context_data(self, **kwargs):
        vendor = connection.vendor
        db_name = 'Unknown DB'
        db_version = 'Unknown'
        select_string = ''
        if vendor == 'sqlite':
            db_name = 'SQLite'
            select_string = 'select sqlite_version();'
        if vendor == 'mysql':
            db_name = 'MySQL'
            select_string = 'SELECT VERSION();'
        if vendor == 'postgresql':
            db_name = 'PostgreSQL'
            select_string = 'SELECT version();'
        if len(select_string) > 0:
            with connection.cursor() as cursor:
                cursor.execute(select_string)
                db_version, = cursor.fetchone()
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'О сайте',
            'navbar': navbar_active('about'),
            'python_version': sys.version,
            'django_version': django.get_version(),
            'db_name': db_name,
            'db_version': db_version,
            'base_dir': settings.BASE_DIR,
            'browser_user_agent': self.request.META['HTTP_USER_AGENT'],
        })
        context.update(get_db_lists())
        return context


# , mixins.PermissionRequiredMixin
# generic.edit.FormMixin,
class ProfileView(mixins.LoginRequiredMixin, generic.edit.FormMixin, generic.TemplateView):
    template_name = 'main/profile.html'
    form_class = forms.RequestWriterForm
    success_url = reverse_lazy('main:profile')

    def post(self, request, **kwargs):
        print('post')
        user = request.user
        group_readers = Group.objects.get(name='Читатели')
        group_request_writers = Group.objects.get(name='Запрос_На_Писатели')
        print(user.groups.all()[0])
        if user.groups.all()[0] == group_readers:
            print('group_readers')
            user.groups.set([group_request_writers])
        elif user.groups.all()[0] == group_request_writers:
            print('group_request_writers')
            user.groups.set([group_readers])
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

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
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'Профиль пользователя',
            'navbar': navbar_active('profile'),
            'user': user,
            'account': account,
        })
        context.update(get_db_lists())
        return context


class ProfileArticlesView(generic.ListView):
    template_name = 'main/profile_articles.html'
    model = models.Article
    context_object_name = 'article_list'

    def get_queryset(self):
        user = self.request.user
        return models.Article.objects.filter(created_by=user).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'Мои статьи',
            'navbar': navbar_active('profile_articles'),
            # 'comment_list': get_comments_list(context.get('pk')),
        })
        context.update(get_db_lists())
        return context


class ProfileFavoritesView(generic.ListView):
    template_name = 'main/profile_favorites.html'
    model = models.Article
    context_object_name = 'favorite_list'

    def get_queryset(self):
        # print('get_queryset')
        user = self.request.user
        return models.FavoriteArticle.objects.filter(created_by=user).order_by('-created_at').select_related('article')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'Избранное',
            'navbar': navbar_active('profile_favorites'),
        })
        context.update(get_db_lists())
        return context


class UserView(generic.TemplateView):
    template_name = 'main/user.html'

    def get_context_data(self, **kwargs):
        pk = self.kwargs.get('pk')
        writer_account = None
        user_object = User.objects.filter(pk=pk)
        if not user_object.exists():
            raise Http404
        writer = user_object.get()
        # print(f'{user=}')
        account_object = models.Account.objects.filter(pk=pk)
        if account_object.exists():
            writer_account = account_object.get()
        # article_list = models.Article.objects.filter(created_by=pk).order_by('-created_at')
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'Профиль автора',
            'navbar': navbar_active('user'),
            'writer': writer,
            'writer_account': writer_account,
            # 'article_list': article_list,
        })
        context.update(get_db_lists())
        return context


class UserArticlesView(generic.ListView):
    template_name = 'main/user_articles.html'
    model = models.Article
    context_object_name = 'article_list'
    paginate_by = 4

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        # subquery = models.FavoriteArticle.objects.filter(article=OuterRef('pk'), created_by=self.request.user).count()
        # .annotate(
        #     name=Subquery(
        #         Team.objects.filter(
        #             id=OuterRef('team_id')
        #         ).values('name')
        # return models.Article.objects.filter(category=pk).order_by('-created_at').annotate(
        #         favorites_count=Subquery(
        #             models.FavoriteArticle.objects.filter(
        #                 article=OuterRef('id'), created_by=self.request.user).annotate(
        #                     count=Count('id')).values('count')
        #         )
        # )
        return models.Article.objects.filter(
            created_by=pk).order_by('-created_at')  # .annotate(favorites_count=Subquery(subquery))

    def get_context_data(self, **kwargs):
        pk = self.kwargs.get('pk')
        writer = User.objects.get(pk=pk)
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'Статьи автора',
            'navbar': navbar_active('user'),
            'writer': writer,
        })
        context.update(get_db_lists())
        return context


class ProfileUpdateMultiView(generic.FormView):
    template_name = 'main/profile_update.html'
    form_class = forms.ProfileUpdateMultiForm
    success_url = reverse_lazy('main:profile')

    def get_form_kwargs(self):
        kwargs = super(ProfileUpdateMultiView, self).get_form_kwargs()
        kwargs.update(instance={
            'user': self.request.user,
            'account': models.Account.objects.filter(pk=self.request.user.pk).get(),
        })
        return kwargs

    def form_valid(self, form, **kwargs):
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


class ArchiveArticleView(generic.dates.ArchiveIndexView):
    template_name = 'main/archive_article.html'
    model = models.Article
    context_object_name = 'article_list'
    date_field = 'created_at'
    allow_future = False
    paginate_by = 4

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
    paginate_by = 4

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
    paginate_by = 4

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
    paginate_by = 4

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'Архив статей',
            'navbar': navbar_active('archive'),
        })
        context.update(get_db_lists())
        return context
