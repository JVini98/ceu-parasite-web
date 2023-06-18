from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Identification
from django.db.models import Count

identifications = []

# Decorator that registers a signal receiver function to be called, when an instance of the Identification model is saved
@receiver(post_save, sender=Identification)
def log_identification(sender, instance, created, **kwargs):
    if created:
        print(f'New identification created: {instance.id}')
        # # Define the number of identifications per image to launch the cluster algorithm
        # number_indentifications_per_image = 2
        # # Get the photographs that match the number of identifications per image 
        # photographs_valid = Identification.objects.values('photograph')\
        #     .annotate(num_photos=Count('photograph'))\
        #     .filter(num_photos__gte=number_indentifications_per_image)
        # # print(photographs_valid)
        # # Get Querysets with the all the identifications per image
        # for photograph_valid in photographs_valid:
        #     identifications_per_image = Identification.objects.filter(photograph=photograph_valid['photograph']).values('coordinateX', 'coordinateY', 'width', 'height', 'parasite')
        #     identifications.append(identifications_per_image)
        # # print(identifications)
    else:
        print('Identification updated, so nothing is done')