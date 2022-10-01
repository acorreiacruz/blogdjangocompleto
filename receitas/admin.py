from django.contrib import admin
from .models import Category, Receitas
from django.contrib.auth.models import User
from tag.models import Tag
from django.contrib.contenttypes.admin import GenericStackedInline


class TagInline(GenericStackedInline):
    model = Tag
    fields = 'name',
    extra = 1



admin.site.unregister(User)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'username', 'email')
    list_display_links = ('id', 'username')
    search_fields = 'username',


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')


@admin.register(Receitas)
class ReceitasAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_at', 'author', 'is_published')
    list_display_links = ('id', 'title')
    search_fields = 'title' , 'slug', 'description', 'author'
    list_per_page = 10
    list_filter = ('is_published', 'category', 'author')
    list_editable = 'is_published',
    prepopulated_fields = {
        'slug': ('title',)
    }
    inlines = [
        TagInline
    ]
