from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import CroppedImage
import json

# Create your views here.
def manipulateImage(request):
    if request.method == "POST":
        jsonReceived = request.POST.get('json')
        json2 = json.loads(jsonReceived)
        message = "Successfully sent to the server"
        return HttpResponse(json2)
    else:
        image = CroppedImage.objects.get(pk=2)
        return render(request=request, template_name="game.html", context={'image': image})


