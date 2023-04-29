import base64
from io import BytesIO

import numpy as np
from django.core.checks import messages
from django.http import HttpResponse
from django.shortcuts import redirect, render

from PIL import Image
from PIL import ImageColor
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageOps

from .forms import PhotographForm
from .models import Photograph
from users.models import User

# model_integration

import matplotlib
import matplotlib.pyplot as plt

import grpc
import tensorflow as tf
from tensorflow_serving.apis import prediction_service_pb2_grpc
from tensorflow_serving.apis.predict_pb2 import PredictRequest


# TODO: raises ValueError("not enough image data") with small images
def upload_file(request):
    if request.method == "POST":
        form = PhotographForm(data=request.POST, files=request.FILES)
        user = User.objects.get(email=request.session["user"])
        if form.is_valid():
            photograph = form.save(commit=False)
            photograph.user = user
            photograph.save()
            parasite_img_model: Photograph = photograph
            parasite_img = Image.open(parasite_img_model.path)
            annotated_img = annotate_parasites(parasite_img)
            return render(request=request, template_name="uploads/show.html", context={"img_uri": to_data_uri(annotated_img)})
    else:
        # If the user is logged in
        if ('user' in request.session):
            form = PhotographForm()
            return render(request=request, template_name="uploads/form.html", context={'form': form})
        # Display error message
        else:
            error = 'To access the uploads section, you need to login'
            return redirect(f'/?error={error}')


def to_data_uri(numpy_img):
    pil_img = Image.fromarray(numpy_img, 'RGB')
    data = BytesIO()
    pil_img.save(data, "png")
    data64 = base64.b64encode(data.getvalue())
    return u'data:img/jpeg;base64,' + data64.decode('utf-8')


def draw_bounding_box_on_image(image,
                               ymin,
                               xmin,
                               ymax,
                               xmax,
                               color,
                               font,
                               thickness=4,
                               display_str_list=()):
    """Adds a bounding box to an image."""
    draw = ImageDraw.Draw(image)
    im_width, im_height = image.size
    (left, right, top, bottom) = (xmin * im_width, xmax * im_width,
                                  ymin * im_height, ymax * im_height)
    draw.line([(left, top), (left, bottom), (right, bottom), (right, top),
               (left, top)],
              width=thickness,
              fill=color)

    # If the total height of the display strings added to the top of the bounding
    # box exceeds the top of the image, stack the strings below the bounding box
    # instead of above.
    display_str_heights = [font.getsize(ds)[1] for ds in display_str_list]
    # Each display_str has a top and bottom margin of 0.05x.
    total_display_str_height = (1 + 2 * 0.05) * sum(display_str_heights)

    if top > total_display_str_height:
        text_bottom = top
    else:
        text_bottom = top + total_display_str_height
    # Reverse list and print from bottom to top.
    for display_str in display_str_list[::-1]:
        text_width, text_height = font.getsize(display_str)
        margin = np.ceil(0.05 * text_height)
        draw.rectangle([(left, text_bottom - text_height - 2 * margin),
                        (left + text_width, text_bottom)],
                       fill=color)
        draw.text((left + margin, text_bottom - text_height - margin),
                  display_str,
                  fill="black",
                  font=font)
        text_bottom -= text_height - 2 * margin


def draw_boxes(image, boxes, class_names, scores, max_boxes=10, min_score=0.1):
    """Overlay labeled boxes on an image with formatted scores and label names."""
    colors = list(ImageColor.colormap.values())

    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSansNarrow-Regular.ttf",
                                  25)
    except IOError:
        print("Font not found, using default font.")
        font = ImageFont.load_default()

    for i in range(min(boxes.shape[0], max_boxes)):
        print(scores[i], min_score)
        if scores[i] >= min_score:
            ymin, xmin, ymax, xmax = tuple(boxes[i])
            display_str = "{}: {}%".format(class_names[i], 100 * scores[i])
            color = colors[hash(class_names[i]) % len(colors)]
            image_pil = Image.fromarray(np.uint8(image)).convert("RGB")
            draw_bounding_box_on_image(
                image_pil,
                ymin,
                xmin,
                ymax,
                xmax,
                color,
                font,
                display_str_list=[display_str])
            np.copyto(image, np.array(image_pil))
    return image


def map_classes(classes):

    conversion_table = {
        1: "Trichuris trichura",
        2: "Ascaris lumbricoides",
        3: "Uncinarias",
        4: "Diphyllobotrium latum",
        5: "Taenia",
        6: "Balantidium coli",
        7: "Hymenolepis nana",
        8: "Enterobius vermicularis",
        9: "Amebas",
        10: "Giardia",
        11: "Sin clasificar"
    }

    string_arr = np.vectorize(conversion_table.get)(classes)
    return string_arr


def annotate_parasites(parasite_img):
    # TODO: to be modified to talk with the AI

    # matplotlib.use('TkAgg')

    SERVER = '13.48.86.83:8500'

    parasite_img_np = np.asarray(parasite_img)

    request = PredictRequest()
    request.model_spec.name = "saved_model"
    request.model_spec.signature_name = "serving_default"
    request.inputs['input_tensor'].CopyFrom(
        tf.make_tensor_proto(parasite_img_np[np.newaxis, :, :, :]))

    channel = grpc.insecure_channel(
        SERVER,
        options=[('grpc.max_send_message_length', -1),
                 ('grpc.max_receive_message_length', -1)]
    )
    predict_service = prediction_service_pb2_grpc.PredictionServiceStub(
        channel)
    response = predict_service.Predict(request, timeout=60)

    num_detections = int(tf.make_ndarray(
        response.outputs["num_detections"])[0])
    output_dict = {
        'detection_boxes': tf.make_ndarray(response.outputs["detection_boxes"]),
        'detection_classes': tf.make_ndarray(response.outputs["detection_classes"]).astype('int64'),
        'detection_scores': tf.make_ndarray(response.outputs["detection_scores"])
    }
    output_dict = {key: value[0, :num_detections]
                   for key, value in output_dict.items()}
    output_dict['num_detections'] = num_detections

    annotated_img = draw_boxes(parasite_img_np, output_dict['detection_boxes'], map_classes(
        output_dict['detection_classes']), output_dict['detection_scores'])

    img_drawer = ImageDraw.Draw(annotated_img)
    img_drawer.line((0, 0) + annotated_img.size, fill=128)
    img_drawer.line(
        (0, annotated_img.size[1], annotated_img.size[0], 0), fill=128
    )
    # Should return an array to imitate AI's behaviour
    return np.asarray(annotated_img)
