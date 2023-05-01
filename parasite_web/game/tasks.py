from parasite_web.celery import app as celery_app
from .models import Identification
from uploads.models import Region, Photograph, Parasite
from django.db.models import Count
from .clustering import get_clusters_per_image

identifications_grouped = []

# Retrieve the parasite instance
def retrieveParasite(idReceived):
    return Parasite.objects.get(id=idReceived)

# Retrieve the photograph instance
def retrievePhotograph(idReceived):
    return Photograph.objects.get(id=idReceived)

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
    for index, identification_grouped in enumerate(identifications_grouped):
        photograph_id = photographs_valid[index]['photograph']
        print("El ID de la imagen procesada es " + str(photograph_id))
        print("Lo que se le pasa es " + str(identification_grouped))
        regions_of_interest_image = get_clusters_per_image(identification_grouped)
        print("Lo que recibe es"  + str(regions_of_interest_image))
        for region_of_interest_image in regions_of_interest_image:
            print(region_of_interest_image[4])
            region = Region(coordinateX=region_of_interest_image[0],
                            coordinateY=region_of_interest_image[1],
                            width=region_of_interest_image[2],
                            height=region_of_interest_image[3],
                            photograph=retrievePhotograph(photograph_id),
                            parasite=retrieveParasite(region_of_interest_image[4])
                            )
            region.save()