from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Artist

User = get_user_model()

@receiver(post_save, sender=User)
def create_artist_profile(sender, instance, created, **kwargs):
    if created and instance.is_artist:
        Artist.objects.create(user=instance)