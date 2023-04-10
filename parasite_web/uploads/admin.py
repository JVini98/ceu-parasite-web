from django.contrib import admin

from .models import Photograph, Parasite

class PhotographAdmin(admin.ModelAdmin):
    list_display = ('id', 'path')

class ParasiteAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

admin.site.register(Photograph, PhotographAdmin)
admin.site.register(Parasite, ParasiteAdmin)