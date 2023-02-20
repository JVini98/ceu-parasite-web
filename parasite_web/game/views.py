from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import CroppedImage

# Create your views here.
def manipulateImage(request):
    image = CroppedImage.objects.get(pk=2)
    return render(request=request, template_name="game.html", context={'image': image})
