# Generated by Django 4.2.7 on 2023-11-29 18:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_rename_tags_tag_alter_article_options_article_tags'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Categories',
            new_name='Category',
        ),
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['id'], 'verbose_name': 'Category (Категория)', 'verbose_name_plural': 'Categories (Категории)'},
        ),
    ]