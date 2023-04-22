from django.db import models
from users.models import User

# Create your models here.
class Photograph(models.Model):
    path = models.ImageField(upload_to="images/")
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return str(self.pk)

class Parasite(models.Model):
    name = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return str(self.pk)

if (not Parasite.objects.exists()):
    Parasite(name="Entamoeba").save()
    Parasite(name="Ascaris lumbricoides").save()
    Parasite(name="Balantidium coli").save()
    Parasite(name="Diphyllobothrium latum").save()
    Parasite(name="Entamoeba coli").save()
    Parasite(name="Enterobius vermicularis").save()
    Parasite(name="Giardia").save()
    Parasite(name="Hymenolepis nana").save()
    Parasite(name="Taenia").save()
    Parasite(name="Trichuris trichura").save()
    Parasite(name="Hookworm").save()

class Region(models.Model):
    coordinateX = models.CharField(max_length=20)
    coordinateY = models.CharField(max_length=20)
    width = models.CharField(max_length=20)
    height = models.CharField(max_length=20)
    timestamp = models.DateTimeField(auto_now_add=True)
    photograph = models.ForeignKey(Photograph, on_delete=models.CASCADE)
    parasite = models.ForeignKey(Parasite, on_delete=models.CASCADE)
