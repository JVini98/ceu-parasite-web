from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.template import loader
from uploads.models import Photograph, Parasite
from users.models import User
from .models import Identification
from .forms import ReportPhotographForm
from django.db.models import Count
from PIL import Image
from io import BytesIO
import json, piexif, base64

# Create your views here.
# Retrieve the parasite instance
def retrieveParasite(nameSelected):
    return Parasite.objects.get(name=nameSelected)

# Retrieve the photograph instance
def retrievePhotograph(idReceived):
    return Photograph.objects.get(id=idReceived)

# Show the photograph with the least number of annotations
def getPhotographLessAnnotations():
    # Retrieve photographs with and without annotations
    photographsWithAnnotations = Identification.objects.values('photograph').annotate(count=Count('photograph')).order_by('count')
    allPhotographs = Photograph.objects.all()
    
    # Find the photograph with the least number of annotations or the first with no annotations
    photographWithLeastAnnotations = None
    leastAnnotationsCount = float('inf')
    for photograph in allPhotographs:
        annotationsCount = 0
        for annotatedPhotograph in photographsWithAnnotations:
            if annotatedPhotograph['photograph'] == photograph.id:
                annotationsCount = annotatedPhotograph['count']
                break
        if annotationsCount < leastAnnotationsCount:
            leastAnnotationsCount = annotationsCount
            photographWithLeastAnnotations = photograph    
    return photographWithLeastAnnotations

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
                                                photograph=retrievePhotograph(dict["imageID"]),
                                                parasite=retrieveParasite(dict["annotation"])
                                                )
                identification.save()
            return JsonResponse({'message': "Successfully sent to the server"})
    else:
        # If the user is logged in
        if ('user' in request.session):
            # Try to get images from the DB
            try: 
                image = getPhotographLessAnnotations()
                executed, imageDisplay = deleteEXIF(image)
                # Image with EXIF metadata (JPEG)
                if executed:
                    buffer = BytesIO()
                    imageDisplay.save(buffer, format="JPEG")
                    buffer.seek(0)
                    mime_type = "image/jpeg"
                    contents = buffer.getvalue()
                    contents_base64 = base64.b64encode(contents).decode()
                    imageRender = {
                        'id': image.id,
                        'path': f"data:{mime_type};base64,{contents_base64}"
                    }
                # Image with no EXIF metadata
                else: 
                    imageRender = {
                        'id': image.id,
                        'path': imageDisplay.path.url
                    }
                parasites = Parasite.objects.values_list('name', flat=True)
                # If there are parasites in the DB
                if parasites: 
                    form = ReportPhotographForm()
                    return render(request=request, template_name="game.html", context={"image": imageRender, 'parasites': parasites, 'form': form})
                # If there are no parasites in the DB
                else: 
                    error = 'Currently there are no parasites to choose from, please contact the administrator to provide you the options'
                    return redirect(f'/?error={error}')
            # There are no images in the DB
            except: 
                error = 'Currently there are no images to identify, please provide one in the uploads section'
                return redirect(f'/?error={error}')
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

