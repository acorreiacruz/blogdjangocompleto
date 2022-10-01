from random import SystemRandom
import string
from django.utils.text import slugify
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class Tag(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(unique=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveBigIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    def save(self, *args, **kwargs):
        if not self.slug:
            letras_randomicas = "".join(
                SystemRandom().choices(string.ascii_letters + string.digits, k=5)
            )
            self.slug = slugify(letras_randomicas)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name
