from django.contrib import admin
from . import models


class CategoriesAdmin(admin.ModelAdmin):
    fields = ['name', ('banner',)]
    list_display = 'id', 'name', 'banner',
    list_display_links = 'name',
    search_fields = 'name',


admin.site.register(models.Categories, CategoriesAdmin)


class NewsAdmin(admin.ModelAdmin):
    fields = ['category', ('headline', 'content'), 'banner', 'created_by', 'pub_date']
    list_display = 'id', 'category', 'headline', 'created_by', 'pub_date'
    list_display_links = 'headline',
    search_fields = 'category', 'headline', 'created_by', 'pub_date',


admin.site.register(models.News, NewsAdmin)


class CommentsAdmin(admin.ModelAdmin):
    fields = ['news', 'created_by', 'message', 'pub_date']
    list_display = 'id', 'news', 'created_by', 'pub_date',
    list_display_links = 'id',
    search_fields = 'news', 'created_by', 'pub_date',


admin.site.register(models.Comments, CommentsAdmin)
