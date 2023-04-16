from django.db import models
from uploads.models import Photograph, Parasite
from users.models import User


# Create your models here.
class Identification(models.Model):
    coordinateX = models.CharField(max_length=20)
    coordinateY = models.CharField(max_length=20)
    width = models.CharField(max_length=20)
    height = models.CharField(max_length=20)
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    photograph = models.ForeignKey(Photograph, on_delete=models.CASCADE)
    parasite = models.ForeignKey(Parasite, on_delete=models.CASCADE)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 
                                            'photograph', 
                                            'parasite', 
                                            'coordinateX', 
                                            'coordinateY', 
                                            'width', 
                                            'height'
                                            ], name='unique_indetification')
        ]
