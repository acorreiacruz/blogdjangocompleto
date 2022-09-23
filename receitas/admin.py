from django.contrib import admin
from .models import Category, Receitas

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')


@admin.register(Receitas)
class ReceitasAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_at', 'author', 'is_published')
    list_display_links = ('id', 'title')
    search_fields = 'id', 'title' , 'slug', 'description', 'author'
    list_per_page = 10
    list_filter = ('is_published', 'category', 'author')
    list_editable = 'is_published',
    prepopulated_fields = {
        'slug': ('title',)
    }

