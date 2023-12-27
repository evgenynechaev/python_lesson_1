from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User, Group

from . import models


def set_writer(model, request, queryset):
    group = Group.objects.get(name='Писатели')
    for user in queryset:
        user.groups.set([group])


set_writer.short_description = "Разрешить пользователю написание статей"


def set_reader(model, request, queryset):
    group = Group.objects.get(name='Читатели')
    for user in queryset:
        user.groups.set([group])


set_reader.short_description = "Перевести пользователя в Читатели"


class CustomUserAdmin(UserAdmin):
    actions = set_writer, set_reader,
    list_display = 'username', 'first_name', 'last_name', 'email', '_groups', 'is_staff',
    list_filter = 'username', 'email',

    def _groups(self, row):
        return ', '.join(row.groups.all().values_list('name', flat='True'))

    _groups.short_description = 'Группы'


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


# admin.site.unregister(User)
# admin.site.register(User, CustomUserAdmin)


class AccountAdmin(admin.ModelAdmin):
    list_display = ['user', 'nickname', 'birthday', 'gender']
    list_filter = ['user', 'nickname', 'birthday', 'gender']


admin.site.register(models.Account, AccountAdmin)


class CategoryAdmin(admin.ModelAdmin):
    fields = ['title', ('banner',)]
    list_display = 'id', 'title', 'banner', 'banner_tag',
    list_display_links = 'title',
    search_fields = 'title',


admin.site.register(models.Category, CategoryAdmin)


class TagAdmin(admin.ModelAdmin):
    list_display = 'id', 'title', 'status'
    list_filter = 'title', 'status',


admin.site.register(models.Tag, TagAdmin)


class ArticleAdmin(admin.ModelAdmin):
    fields = 'category', 'title', 'annotation', 'content', 'banner', 'tags', 'views',
    list_display = 'id', 'category', 'title', 'created_by', 'created_at', 'views', '_tags', 'banner_tag'
    list_display_links = 'id', 'title',
    search_fields = 'category', 'title', 'created_at',
    ordering = '-created_at', 'title', 'created_by',
    filter_horizontal = 'tags',

    def _tags(self, row):
        return ', '.join(row.tags.all().values_list('title', flat='True'))

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user  # the object is being created, so set the user
            views = models.Views.objects.create(count=0)
            obj.views = views
        obj.save()


admin.site.register(models.Article, ArticleAdmin)


class ViewsAdmin(admin.ModelAdmin):
    list_display = 'count',
    # list_filter = 'article',


admin.site.register(models.Views, ViewsAdmin)


class FavoriteArticleAdmin(admin.ModelAdmin):
    list_display = 'article', 'created_by', 'created_at',
    list_filter = 'article', 'created_by', 'created_at',


admin.site.register(models.FavoriteArticle, FavoriteArticleAdmin)


class CommentAdmin(admin.ModelAdmin):
    fields = 'article', 'message', 'created_by',
    list_display = 'id', 'article', 'message', 'created_by',
    list_display_links = 'id',
    search_fields = 'article', 'created_by', 'created_at',


admin.site.register(models.Comment, CommentAdmin)
