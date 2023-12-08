from django.contrib import admin
from . import models


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
    list_display = 'title', 'status'
    list_filter = 'title', 'status',


admin.site.register(models.Tag, TagAdmin)


class ArticlesAdmin(admin.ModelAdmin):
    fields = 'category', 'title', 'annotation', 'content', 'banner', 'tags', 'views',
    list_display = 'id', 'category', 'title', 'created_by', 'created_at', 'views', '_tags',
    list_display_links = 'id', 'title',
    search_fields = 'category', 'title', 'created_at',

    def	_tags(self, row):
        return ', '.join(row.tags.all().values_list('title', flat='True'))

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user  # the object is being created, so set the user
            views = models.Views.objects.create(count=0)
            obj.views = views
        obj.save()


admin.site.register(models.Article, ArticlesAdmin)


class ViewsAdmin(admin.ModelAdmin):
    list_display = 'count',
    # list_filter = 'article',


admin.site.register(models.Views, ViewsAdmin)


# class ArticleViewsAdmin(admin.ModelAdmin):
#     list_display = 'article', 'count_views'
#     list_filter = 'article',


# admin.site.register(models.ArticleViews, ArticleViewsAdmin)


class CommentsAdmin(admin.ModelAdmin):
    fields = 'article', 'message', 'created_by',
    list_display = 'id', 'article', 'message', 'created_by',
    list_display_links = 'id',
    search_fields = 'article', 'created_by', 'created_at',


admin.site.register(models.Comments, CommentsAdmin)
