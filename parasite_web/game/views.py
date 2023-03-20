from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
from uploads.models import Photograph, Parasite, User
from .models import Identification
import json

# Create your views here.
def retrieveIdParasite(nameSelected):
    return Parasite.objects.get(name=nameSelected)

def manipulateImage(request):
    if request.method == "POST":
        jsonReceived = request.POST.get('json')

        if (jsonReceived != ""):
            json2 = json.loads(jsonReceived)
            for dict in json2:
                identification = Identification(coordinateX=dict["coordinateX"], 
                                                coordinateY=dict["coordinateY"], 
                                                width=dict["width"], 
                                                height=dict["height"], 
                                                user=User.objects.get(pk=1),
                                                photograph=Photograph.objects.get(pk=4),
                                                parasite=retrieveIdParasite(dict["annotation"])
                                                )
                identification.save()
            return JsonResponse({'message': "Successfully sent to the server"})
    else:
        image = Photograph.objects.get(pk=4)
        parasites = Parasite.objects.values_list('name', flat=True)
        return render(request=request, template_name="game.html", context={'image': image, 'parasites': parasites})