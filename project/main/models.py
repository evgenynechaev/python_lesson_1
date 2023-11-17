from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse_lazy


class Categories(models.Model):
    name = models.CharField(
        max_length=20,
        db_index=True,
        null=False,
        blank=False,
        unique=True,
        verbose_name='name (Категория)',
        help_text='Название категории')
    banner = models.FileField(
        upload_to='media/',
        null=True,
        blank=True,
        verbose_name='banner (Баннер)')
    image = models.ImageField(
        upload_to='images/',
        null=True,
        blank=True,
        verbose_name='image (Баннер)')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Categories (Категории)'
        verbose_name_plural = 'Categories (Категории)'
        ordering = ['id']


class News(models.Model):
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    headline = models.CharField(
        max_length=200,
        db_index=False,
        null=False,
        blank=False,
        unique=False,
        verbose_name='headline (Заголовок)',
        help_text='Заголовок новости')
    content = models.TextField(
        db_index=False,
        null=False,
        blank=False,
        unique=False,
        verbose_name='content (Новость)',
        help_text='Содержание новости')
    banner = models.FileField(
        upload_to='media/',
        null=True,
        blank=True,
        verbose_name='banner (Баннер)')
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE)
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='created_at (Дата создания)')

    def __str__(self):
        return self.headline

    class Meta:
        verbose_name = 'News (Новость)'
        verbose_name_plural = 'News (Новость)'


class Comments(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE)
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
