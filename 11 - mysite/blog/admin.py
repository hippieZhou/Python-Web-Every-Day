from django.contrib import admin
from .models import BlogArticles
# Register your models here.


@admin.register(BlogArticles)
class BlogArticlesAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publish')
    list_filter = ('publish', 'author')
    search_fields = ('title', 'body')
    raw_id_fidles = ('author',)
    date_hierarchy = 'publish'
    ordering = ['-publish', 'author']

# 个人喜欢采用装饰器方式进行注册，如上
# admin.site.register(BlogArticles, BlogArticlesAdmin)
