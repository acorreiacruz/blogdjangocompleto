from receitas.models import Receitas
from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver
import os


def delete_cover(instance):
    try:
        os.remove(instance.cover.path)
    except (ValueError, FileNotFoundError):
        ...


@receiver(pre_delete, sender=Receitas)
def receita_cover_delete(sender, instance, *args, **kwargs):
    old_instance = Receitas.objects.filter(pk=instance.pk).first()
    delete_cover(old_instance)


@receiver(pre_save, sender=Receitas)
def receita_cover_update(sender , instance, *args, **kwargs):
    old_instance = Receitas.objects.filter(pk=instance.pk).first()
    is_new_cover = old_instance.cover != instance.cover

    if is_new_cover:
        delete_cover(old_instance)
