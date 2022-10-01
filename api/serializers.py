from rest_framework import serializers
from receitas.models import Receitas, Category
from tag.models import Tag
from django.contrib.auth.models import User

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug']


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'email']


class ReceitasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Receitas
        fields = [
            'id', 'title', 'description', 'slug', 'preparation_time',
            'preparation_time_unit', 'servings', 'servings_unit', 'preparation_step',
            'preparation_step_is_html', 'is_published', 'category', 'author'
        ]
    category = CategoriaSerializer(read_only=True)
    author = UserSerializer(read_only=True)
    tags = TagSerializer(read_only=True)
