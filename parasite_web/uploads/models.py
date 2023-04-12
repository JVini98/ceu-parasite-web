from django.db import models

# Create your models here.
class Photograph(models.Model):
    path = models.ImageField(upload_to="images/")
    #uploaded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.pk)

class Parasite(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
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
