# Generated by Django 4.2.7 on 2023-11-16 21:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, help_text='Название категории', max_length=20, unique=True, verbose_name='name (Категория)')),
                ('banner', models.FileField(blank=True, null=True, upload_to='media/', verbose_name='banner (Баннер)')),
            ],
            options={
                'verbose_name': 'Categories (Категории)',
                'verbose_name_plural': 'Categories (Категории)',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('headline', models.CharField(help_text='Заголовок новости', max_length=200, verbose_name='headline (Заголовок)')),
                ('content', models.TextField(help_text='Содержание новости', verbose_name='content (Новость)')),
                ('banner', models.FileField(blank=True, null=True, upload_to='media/', verbose_name='banner (Баннер)')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='created_at (Дата создания)')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.categories')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'News (Новость)',
                'verbose_name_plural': 'News (Новость)',
            },
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(help_text='Комментарий к новости', verbose_name='message (Комментарий)')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('news', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.news')),
            ],
            options={
                'verbose_name': 'Comments (Комментарии)',
                'verbose_name_plural': 'Comments (Комментарии)',
            },
        ),
    ]