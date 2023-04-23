from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.template import loader
from uploads.models import Photograph, Parasite
from users.models import User
from .models import Identification
from .forms import ReportPhotographForm
import json

# Create your views here.
def retrieveIdParasite(nameSelected):
    return Parasite.objects.get(name=nameSelected)

# A user has reported a photograph
def reportedPhotograph(request):
    if request.method == "POST":
        form = ReportPhotographForm(request.POST or None)
        if form.is_valid():
            pkImage = form.cleaned_data['image_reported']
            image = Photograph.objects.get(id=pkImage)
            image.reported = True
            image.save()
            return redirect('/game')

# Receive the identifications send by the user
def manipulateImage(request):
    if request.method == "POST":
        jsonReceived = request.POST.get('json')
        user = User.objects.get(email=request.session["user"])

        if (jsonReceived != ""):
            json2 = json.loads(jsonReceived)
            for dict in json2:
                identification = Identification(coordinateX=dict["coordinateX"], 
                                                coordinateY=dict["coordinateY"], 
                                                width=dict["width"], 
                                                height=dict["height"], 
                                                user=user,
                                                photograph=Photograph.objects.first(),
                                                parasite=retrieveIdParasite(dict["annotation"])
                                                )
                identification.save()
            return JsonResponse({'message': "Successfully sent to the server"})
    else:
        # If the user is logged in
        if ('user' in request.session):
            image = Photograph.objects.first()
            parasites = Parasite.objects.values_list('name', flat=True)
            form = ReportPhotographForm()
            return render(request=request, template_name="game.html", context={'image': image, 'parasites': parasites, 'form': form})
        # Display error message
        else: 
            error = 'To access the game section, you need to login'
            return redirect(f'/?error={error}')