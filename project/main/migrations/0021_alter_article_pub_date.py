# Generated by Django 4.2.7 on 2023-12-01 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0020_alter_account_birthday_alter_account_gender_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='pub_date',
            field=models.DateTimeField(blank=True, help_text='Дата публикации', null=True, verbose_name='pub_date (Дата публикации)'),
        ),
    ]
