from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from autores.models import Profile
from django.dispatch import receiver


User = get_user_model()

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, *args, **kwargs):
    if created:
        profile = Profile.objects.create(
            author=instance
        )


