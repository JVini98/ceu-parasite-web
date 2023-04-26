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
                                                photograph=Photograph.objects.first(),
                                                parasite=retrieveIdParasite(dict["annotation"])
                                                )
                identification.save()
            return JsonResponse({'message': "Successfully sent to the server"})
    else:
        # If the user is logged in
        if ('user' in request.session):
            image = Photograph.objects.get(pk=4)
            imageDisplay, executed = deleteEXIF(image)
            # Image with metadata (JPEG)
            if executed:
                buffer = BytesIO()
                imageDisplay.save(buffer, format="JPEG")
                buffer.seek(0)
                mime_type = "image/jpeg"
                contents = buffer.getvalue().hex()
                contents_bytes = binascii.a2b_hex(contents)
                contents_base64 = base64.b64encode(contents_bytes).decode()
                parasites = Parasite.objects.values_list('name', flat=True)
                form = ReportPhotographForm()
                return render(request=request, template_name="game.html", context={"image": f"data:{mime_type};base64,{contents}", 'parasites': parasites, 'form': form})
            # Image with no EXIF Metadata does not change
            else: 
                parasites = Parasite.objects.values_list('name', flat=True)
                form = ReportPhotographForm()
                return render(request=request, template_name="game.html", context={"image": imageDisplay, 'parasites': parasites, 'form': form})
        # Display error message
        else: 
            error = 'To access the game section, you need to login'
            return redirect(f'/?error={error}')

# Delete EXIF metadata to display the image with no position
def deleteEXIF(imageDB):
    imageRecovered = imageDB.path
    imageBytes = imageRecovered.read()
    imageToChange = Image.open(BytesIO(imageBytes))
    if "exif" in imageToChange.info:
        exifDict = piexif.load(imageToChange.info["exif"])
        exifBytes = piexif.dump(exifDict)
        del imageToChange.info["exif"]
        output = BytesIO()
        imageToChange.save(output, format="JPEG", exif=exifBytes)
        return imageToChange, True
    return imageDB, False

