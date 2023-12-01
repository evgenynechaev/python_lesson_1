import datetime
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe


class BaseModel(models.Model):
    created_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_created",
        related_query_name="%(app_label)s_%(class)ss_created",
        verbose_name='created_by (Кто создал)')
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='created_at (Дата создания)')

    class Meta:
        abstract = True


class Account(models.Model):
    gender_choices = (('M', 'Мужчина'),
                      ('F', 'Женщина'),
                      ('U', 'Не выбрано'))
    user = models.OneToOneField(
        User,
        null=False,
        on_delete=models.CASCADE,
        primary_key=True)
    nickname = models.CharField(
        null=True,
        max_length=20)
    birthday = models.DateField(
        null=True,
        blank=True)
    gender = models.CharField(
        null=True,
        default='U',
        choices=gender_choices,
        max_length=1)
    avatar = models.ImageField(
        # default='default.jpg',
        null=True,
        blank=True,
        upload_to='account_images')

    def __str__(self):
        return f"{self.user.username}'s account"


class Category(models.Model):
    title = models.CharField(
        max_length=20,
        db_index=True,
        null=False,
        blank=False,
        unique=True,
        verbose_name='title (Категория)',
        help_text='Название категории')
    banner = models.ImageField(
        upload_to='images/',
        null=True,
        blank=True,
        verbose_name='banner (Баннер)')

    def __str__(self):
        return self.title

    def banner_tag(self):
        if self.banner:
            return mark_safe(f'<img src="{self.banner.url}" width="auto" height="50"/>')

    # def get_absolute_url(self):
    #     return reverse_lazy('main:guide_test_detail', args=[str(self.id)])

    class Meta:
        verbose_name = 'Category (Категория)'
        verbose_name_plural = 'Categories (Категории)'
        ordering = ['id']


class Tag(models.Model):
    title = models.CharField(max_length=80)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title', 'status']
        verbose_name = 'Tag (Тэг)'
        verbose_name_plural = 'Tags (Тэги)'


class Article(BaseModel):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    # author = models.ForeignKey(
    #     User,
    #     on_delete=models.CASCADE)
    title = models.CharField(
        max_length=200,
        db_index=False,
        null=False,
        blank=False,
        unique=False,
        verbose_name='title (Заголовок)',
        help_text='Заголовок статьи')
    content = models.TextField(
        db_index=False,
        null=False,
        blank=False,
        unique=False,
        verbose_name='content (Содержание)',
        help_text='Содержание статьи')
    banner = models.FileField(
        upload_to='media/',
        null=True,
        blank=True,
        verbose_name='banner (Баннер)')
    pub_date = models.DateTimeField(
        # auto_now_add=True,
        null=True,
        blank=True,
        verbose_name='pub_date (Дата публикации)',
        help_text='Дата публикации')
    tags = models.ManyToManyField(to=Tag, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse_lazy('main:article_detail', kwargs={'pk': self.id})

    def tag_list(self):
        tags = ' '.join(self.tags.all())
        print('tags')
        print(tags)
        return tags
        # s = ''
        # for t in self.tags.all():
        #     s+=t.title+' '
        # return s

    class Meta:
        ordering = ['title', 'pub_date']
        verbose_name = 'Article (Статья)'
        verbose_name_plural = 'Articles (Статьи)'


class ArticleViews(models.Model):
    article = models.OneToOneField(
        Article,
        on_delete=models.CASCADE,
        primary_key=True)
    count_views = models.PositiveIntegerField(
        default=0,
        verbose_name='count_views (Количество просмотров)',
        help_text='Количество просмотров новости')

    class Meta:
        verbose_name = 'ArticleViews (Количество просмотров)'
        verbose_name_plural = 'ArticleViews (Количество просмотров)'


class Comments(BaseModel):
    news = models.ForeignKey(Article, on_delete=models.CASCADE)
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE)
    message = models.TextField(
        db_index=False,
        null=False,
        blank=False,
        unique=False,
        verbose_name='message (Комментарий)',
        help_text='Комментарий к новости')
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='created_at (Дата создания)')

    def __str__(self):
        return self.message

    class Meta:
        verbose_name = 'Comments (Комментарии)'
        verbose_name_plural = 'Comments (Комментарии)'


class PublishedToday(models.Manager):
    def get_queryset(self):
        return super(PublishedToday, self).get_queryset().filter(date__gte=datetime.date.today())
