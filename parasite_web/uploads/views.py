import base64
from io import BytesIO

import numpy as np
from django.core.checks import messages
from django.http import HttpResponse
from django.shortcuts import redirect, render
from PIL import Image, ImageDraw

from .forms import ParasiteImageForm
from .models import ParasiteImage


# TODO: raises ValueError("not enough image data") with small images
def upload_file(request):
    if request.method == "POST":
        form = ParasiteImageForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            parasite_img_model: ParasiteImage = form.save()
            parasite_img = Image.open(parasite_img_model.path)
            annotated_img = annotate_parasites(parasite_img)
            return render(request=request, template_name="uploads/show.html", context={"img_uri": to_data_uri(annotated_img)})
    else:
        form = ParasiteImageForm()
        return render(request=request, template_name="uploads/form.html", context={'form': form})


def to_data_uri(numpy_img):
    pil_img = Image.fromarray(numpy_img, 'RGB')
    data = BytesIO()
    pil_img.save(data, "png")
    data64 = base64.b64encode(data.getvalue())
    return u'data:img/jpeg;base64,' + data64.decode('utf-8')


def annotate_parasites(parasite_img):
    # TODO: to be modified to talk with the AI
    annotated_img = parasite_img.copy()
    img_drawer = ImageDraw.Draw(annotated_img)
    img_drawer.line((0, 0) + annotated_img.size, fill=128)
    img_drawer.line(
        (0, annotated_img.size[1], annotated_img.size[0], 0), fill=128
    )
    # Should return an array to imitate AI's behaviour
    return np.asarray(annotated_img)
