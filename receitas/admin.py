from django.contrib import admin
from .models import Category, Receitas

class CategoryAdmin(admin.ModelAdmin):
    ...

admin.site.register(Category,CategoryAdmin)


@admin.register(Receitas)
class ReceitasAdmin(admin.ModelAdmin):
    ...

