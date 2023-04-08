from django.db import models

# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=22)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    def __str__(self):
        return str(self.pk)