from django.contrib import admin

from .models import ArticleColumn
# Register your models here.


@admin.register(ArticleColumn)
class ArticleColumnAdmiin(admin.ModelAdmin):
    list_display = ('column', 'created', 'user')
    list_filer = ('column',)
