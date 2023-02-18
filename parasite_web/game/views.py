from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import CroppedImage

# Create your views here.
def manipulateImage(request):
    image = CroppedImage.objects.get(pk=2)
    template = loader.get_template('game.html')
    context = {
        'image': image,
    }
    return HttpResponse(template.render(context, request))
