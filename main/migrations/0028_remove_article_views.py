# Generated by Django 4.2.8 on 2023-12-07 06:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0027_alter_article_views'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='views',
        ),
    ]
