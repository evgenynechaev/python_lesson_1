import datetime
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse_lazy
from django.core import validators
from django.utils.safestring import mark_safe


class BaseModel(models.Model):
    created_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_created",
        related_query_name="%(app_label)s_%(class)ss_created",
        verbose_name='Кто создал')
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания')

    class Meta:
        abstract = True


class Account(models.Model):
    gender_choices = (('M', 'Мужчина'),
                      ('F', 'Женщина'),
                      ('U', 'Не выбрано'))
    phoneNumberRegexValidator = validators.RegexValidator(regex=r"^\+?1?\d{8,15}$")
    user = models.OneToOneField(
        User,
        null=False,
        on_delete=models.CASCADE,
        primary_key=True,
        verbose_name='User',
        help_text='User')
    nickname = models.CharField(
        null=True,
        max_length=20,
        verbose_name='Nickname',
        help_text='Nickname')
    birthday = models.DateField(
        null=True,
        blank=True,
        verbose_name='День рождения',
        help_text='День рождения')
    gender = models.CharField(
        null=True,
        default='U',
        choices=gender_choices,
        max_length=1,
        verbose_name='Пол',
        help_text='Пол')
    phone = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        validators=[phoneNumberRegexValidator],
        verbose_name='Телефон',
        help_text='Номер телефона')
    avatar = models.ImageField(
        # default='default.jpg',
        null=True,
        blank=True,
        upload_to='account_images/',
        verbose_name='Аватар',
        help_text='Аватар')

    def __str__(self):
        return f"{self.user.username}'s account"

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


class Category(models.Model):
    title = models.CharField(
        max_length=20,
        db_index=True,
        null=False,
        blank=False,
        unique=True,
        verbose_name='Категория',
        help_text='Название категории')
    banner = models.ImageField(
        upload_to='category_images/',
        null=True,
        blank=True,
        verbose_name='Баннер')

    def __str__(self):
        return self.title

    def banner_tag(self):
        if self.banner:
            return mark_safe(f'<img src="{self.banner.url}" width="auto" height="50"/>')

    # def get_absolute_url(self):
    #     return reverse_lazy('main:guide_test_detail', args=[str(self.id)])

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['id']


class Tag(models.Model):
    title = models.CharField(
        max_length=80,
        verbose_name='Название',
        help_text='Название тэга')
    status = models.BooleanField(
        default=True,
        verbose_name='Статус',
        help_text='Статус тэга')

    def __str__(self):
        return self.title

    class Meta:
        ordering = 'title', 'status',
        verbose_name = 'Тэг (Tag)'
        verbose_name_plural = 'Тэги'


class Views(models.Model):
    count = models.PositiveIntegerField(
        default=0,
        verbose_name='Количество просмотров',
        help_text='Количество просмотров новости')

    def __str__(self):
        return str(self.count)

    class Meta:
        verbose_name = 'Количество просмотров'
        verbose_name_plural = 'Количество просмотров'


class Article(BaseModel):
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        on_delete=models.CASCADE)
    title = models.CharField(
        max_length=200,
        db_index=False,
        null=False,
        blank=False,
        unique=False,
        verbose_name='Заголовок',
        help_text='Заголовок статьи')
    annotation = models.TextField(
        db_index=False,
        null=False,
        blank=False,
        unique=False,
        verbose_name='Аннотация',
        help_text='Аннотация статьи')
    content = models.TextField(
        db_index=False,
        null=False,
        blank=False,
        unique=False,
        verbose_name='Содержание',
        help_text='Содержание статьи')
    banner = models.FileField(
        upload_to='article_images/',
        null=True,
        blank=True,
        verbose_name='Баннер')
    tags = models.ManyToManyField(
        to=Tag,
        blank=True)
    views = models.OneToOneField(
        Views,
        on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse_lazy('main:article_detail', kwargs={'pk': self.pk})

    def banner_tag(self):
        if self.banner:
            return mark_safe(f'<img src="{self.banner.url}" width="auto" height="50"/>')

    def tag_list(self):
        tags = ' '.join(self.tags.all())
        return tags

    def tag_list_str(self):
        tags = ', '.join(self.tags.all().values_list('title', flat=True))
        # print('tags')
        # print(tags)
        return tags

    class Meta:
        ordering = ['title', 'created_at']
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'


class Comment(BaseModel):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    message = models.TextField(
        db_index=False,
        null=False,
        blank=False,
        unique=False,
        verbose_name='Комментарий',
        help_text='Комментарий к новости')

    def __str__(self):
        return self.message

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


class FavoriteArticle(BaseModel):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'


class PublishedToday(models.Manager):
    def get_queryset(self):
        return super(PublishedToday, self).get_queryset().filter(date__gte=datetime.date.today())
