from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.template import loader
from uploads.models import Photograph, Parasite
from users.models import User
from .models import Identification
from .forms import ReportPhotographForm
from PIL import Image
from io import BytesIO
import json, piexif, binascii, base64

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
                                                photograph=Photograph.objects.get(pk=5),
                                                parasite=retrieveIdParasite(dict["annotation"])
                                                )
                identification.save()
            return JsonResponse({'message': "Successfully sent to the server"})
    else:
        # If the user is logged in
        if ('user' in request.session):
            image = Photograph.objects.get(pk=5)
            executed, imageDisplay = deleteEXIF(image)
            # Image with EXIF metadata (JPEG)
            if executed:
                buffer = BytesIO()
                imageDisplay.save(buffer, format="JPEG")
                buffer.seek(0)
                mime_type = "image/jpeg"
                contents = buffer.getvalue()
                contents_base64 = base64.b64encode(contents).decode()
                imageRender = f"data:{mime_type};base64,{contents_base64}"
            # Image with no EXIF metadata
            else: 
                imageRender = imageDisplay.path.url
            parasites = Parasite.objects.values_list('name', flat=True)
            form = ReportPhotographForm()
            return render(request=request, template_name="game.html", context={"image": imageRender, 'parasites': parasites, 'form': form})
        # Display error message
        else: 
            error = 'To access the game section, you need to login'
            return redirect(f'/?error={error}')

# Delete EXIF metadata from a JPEG file to display the image with no unwanted rotation
def deleteEXIF(imageDB):
    imagePath = imageDB.path
    imageBytes = imagePath.read()
    imageToChange = Image.open(BytesIO(imageBytes))
    # Check if the image has EXIF metadata to delete it
    if "exif" in imageToChange.info:
        exifDict = piexif.load(imageToChange.info["exif"])
        exifBytes = piexif.dump(exifDict)
        del imageToChange.info["exif"]
        buffer = BytesIO()
        imageToChange.save(buffer, format="JPEG", exif=exifBytes)
        return True, imageToChange
    return False, imageDB 

