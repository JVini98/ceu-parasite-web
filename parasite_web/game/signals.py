from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Identification

# Decorator that registers a signal receiver function to be called, when an instance of the Identification model is saved
@receiver(post_save, sender=Identification)
def log_identification(sender, instance, created, **kwargs):
    if created:
        print(f'New identification created: {instance.id}')
    else:
        print('Identification updated, so nothing is done')