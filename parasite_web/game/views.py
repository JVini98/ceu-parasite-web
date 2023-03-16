from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
from uploads.models import ParasiteImage
import json

# Create your views here.
def manipulateImage(request):
    if request.method == "POST":
        jsonReceived = request.POST.get('json')

        if (jsonReceived != ""):
            json2 = json.loads(jsonReceived)
            #for dict in json2:
                #insert(dict["url"], dict["annotation"]...)
            return JsonResponse({'message': "Successfully sent to the server"})
            #return JsonResponse({'message': json2[0]["url"]})
    else:
        image = ParasiteImage.objects.get(pk=4)
        return render(request=request, template_name="game.html", context={'image': image})


