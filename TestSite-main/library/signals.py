# Official_LMS/library/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, created, **kwargs):
    if created:
        # Perform actions that should only occur on the creation of a new CustomUser
        # For example, initialize related profiles or send a welcome email
        pass
