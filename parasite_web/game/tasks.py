from parasite_web.celery import app as celery_app
from .models import Identification
from django.db.models import Count
from .clustering import get_clusters_per_image

identifications_grouped = []

@celery_app.task
def launch_clustering():
    # Define the number of identifications per image to launch the cluster algorithm
    number_indentifications_per_image = 2
    # Get the photographs that match the number of identifications per image 
    photographs_valid = Identification.objects.values('photograph')\
        .annotate(num_photos=Count('photograph'))\
        .filter(num_photos__gte=number_indentifications_per_image)
    print(photographs_valid)
    # Get Querysets with the all the identifications per image
    for photograph_valid in photographs_valid:
        identifications_per_image = Identification.objects.filter(photograph=photograph_valid['photograph']).values('coordinateX', 'coordinateY', 'width', 'height', 'parasite')
        identifications_grouped.append(identifications_per_image)
    print(identifications_grouped)
    for identification_grouped in identifications_grouped:
        get_clusters_per_image(identification_grouped)
        print("Lo que se le pasa a cluster es " + str(identification_grouped))

