from django.contrib import admin

from .models import Photograph, Parasite, Region

class PhotographAdmin(admin.ModelAdmin):
    list_display = ('id', 'path', 'timestamp', 'user', 'reported')

class ParasiteAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

class RegionAdmin(admin.ModelAdmin):
    list_display = ('id', 'coordinateX', 'coordinateY', 'width', 'height', 'timestamp', 'photograph', 'parasite')

admin.site.register(Photograph, PhotographAdmin)
admin.site.register(Parasite, ParasiteAdmin)
admin.site.register(Region, RegionAdmin)