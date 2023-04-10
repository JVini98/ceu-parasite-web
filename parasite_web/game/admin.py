from django.contrib import admin

# Register your models here.
from .models import Identification

class IdentificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'coordinateX', 'coordinateY', 'width', 'height', 'timestamp', 'user', 'photograph', 'parasite')

admin.site.register(Identification, IdentificationAdmin)
