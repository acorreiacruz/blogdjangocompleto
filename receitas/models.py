from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.contenttypes.fields import GenericRelation
from tag.models import Tag


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Receitas(models.Model):

    title = models.CharField(max_length= 70)
    description = models.CharField(max_length= 180)
    slug = models.SlugField(unique=True)
    preparation_time = models.IntegerField()
    preparation_time_unit = models.CharField(max_length=15)
    servings = models.IntegerField()
    servings_unit = models.CharField(max_length=30)
    preparation_step = models.TextField()
    preparation_step_is_html = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    cover = models.ImageField(upload_to='receitas/covers/%Y/%m/%d/')
    category = models.ForeignKey(Category,on_delete=models.SET_NULL,null=True,blank=True,default=None)
    author = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    tags = GenericRelation(Tag, related_query_name='receitas')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("receitas:receita", kwargs={"pk":self.id})

    def save(self, *args, **kwargs):

        if not self.slug:
            self.slug = slugify(self.title)

        return super().save(*args, **kwargs)