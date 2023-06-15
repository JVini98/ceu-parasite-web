import matplotlib.pyplot as plt
import numpy as np
import json
import matplotlib.patches as patches
from PIL import Image
from PIL import ImageOps

with open('pruebas.json', 'r') as f:
  data = json.load(f)

img = Image.open("Original.jpg")
img = ImageOps.exif_transpose(img)
for idx in range(5):
    x = float(data[idx]["fields"]["coordinateX"])
    y = float(data[idx]["fields"]["coordinateY"])
    h = float(data[idx]["fields"]["height"])
    w = float(data[idx]["fields"]["width"])

    fig, ax = plt.subplots(2)
    ax[0].imshow(img)
    print((x, y))
    print(w)
    print(h)
    rect = patches.Rectangle((x, y), w, h, linewidth=1, edgecolor='r', facecolor='none')
    ax[0].add_patch(rect)
    ax[1].imshow(Image.open(f"Example{idx + 1}.jpg"))
    plt.show()
