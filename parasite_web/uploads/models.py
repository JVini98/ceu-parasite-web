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

class User(models.Model):
    name = models.CharField(max_length=50)
    surname1 = models.CharField(max_length=50)
    surname2 = models.CharField(max_length=50, blank=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)

if (not User.objects.exists()):
    User(name="Patricia", surname1="Herrera", surname2="", email="patricia@gmail.com", password="patricia1234").save()