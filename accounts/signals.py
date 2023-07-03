from django.core import signals
from django.dispatch import receiver
from django.db.models.signals import post_save
from accounts.models import User, Profile

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=Profile)
def save_profile(sender, instance, created, **kwargs):
    instance.profile.save()