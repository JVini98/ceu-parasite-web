import numpy as np
import torch
from torchvision import ops
from sklearn.cluster import DBSCAN

# image = [top-leftx, top-lefty, width, height]
image1 = ["1149.7215179505479", "725.0646330096754", "516.6119994320322", "290.59424968051815"]
image2 = ["828.3441890112942", "616.470370760941", "832.0087912052824", "468.0049450529714"]
image3 = ["1617.8857662906719", "218.1067835582991", "299.92178394329227", "168.7060034681019"]
image4 = ["1516.6611208894217", "151.54875974912346", "531.329735484363", "298.8729762099542"]
image5 = ["495.6243064641784", "408.49842165746287", "531.329735484363", "298.8729762099542"]

# imageCoord = [top-leftx, top-lefty, botton-rightx, botton-righty] for numpy
image1Coord = ["1149.7215179505479", "725.0646330096754", str(float(image1[0])+float(image1[2])), str(float(image1[1])+float(image1[3]))]
image2Coord = ["828.3441890112942", "616.470370760941", str(float(image2[0])+float(image2[2])), str(float(image1[1])+float(image1[3]))]
image3Coord = ["1617.8857662906719", "218.1067835582991", str(float(image3[0])+float(image3[2])), str(float(image1[1])+float(image1[3]))]
image4Coord = ["1516.6611208894217", "151.54875974912346", str(float(image4[0])+float(image4[2])), str(float(image1[1])+float(image1[3]))]
image5Coord = ["495.6243064641784", "408.49842165746287", str(float(image5[0])+float(image5[2])), str(float(image1[1])+float(image1[3]))]

def box_area(boxes):
    return (boxes[:, 2] - boxes[:, 0]) * (boxes[:, 3] - boxes[:, 1])

def _box_inter_union(boxes1, boxes2):
    boxes1 = boxes1.astype(np.float64)
    boxes2 = boxes2.astype(np.float64)

    area1 = box_area(boxes1)
    area2 = box_area(boxes2)

    lt = np.maximum(boxes1[:, None, :2], boxes2[:, :2])  # [N,M,2]
    rb = np.minimum(boxes1[:, None, 2:], boxes2[:, 2:])  # [N,M,2]

    wh = np.clip(rb - lt, 0, np.Inf)  # [N,M,2]
    inter = wh[:, :, 0] * wh[:, :, 1]  # [N,M]

    union = area1[:, None] + area2 - inter

    return inter, union


def box_iou(boxes1, boxes2):
    """
    Return intersection-over-union (Jaccard index) between two sets of boxes.

    Both sets of boxes are expected to be in ``(x1, y1, x2, y2)`` format with
    ``0 <= x1 < x2`` and ``0 <= y1 < y2``.

    Args:
        boxes1 (np.array[N, 4]): first set of boxes
        boxes2 (np.array[M, 4]): second set of boxes

    Returns:
        Tensor[N, M]: the NxM matrix containing the pairwise IoU values for every element in boxes1 and boxes2
    """
    inter, union = _box_inter_union(boxes1, boxes2)
    iou = inter / union
    return iou

def iou_to_distance(matrix):
    return 1 - matrix

def clustering(distance_matrix):
    dbscan = DBSCAN(eps=0.6, min_samples=2, metric='precomputed')
    labels = dbscan.fit_predict(distance_matrix)
    return labels

if __name__ == "__main__":
    boxes1= np.array([
        image1Coord,
        image2Coord,
        image3Coord,
        image4Coord,
        image5Coord
    ])
    boxes2 = np.array([
        image1Coord,
        image2Coord,
        image3Coord,
        image4Coord,
        image5Coord
    ])
    # Ious contiene todas las comparaciones de boxes1 con boxes2 en una matriz de tamaño 5 x 5
    ious = box_iou(boxes1, boxes2)
    print("The IoU matrix is: " + str(ious.shape))
    print(ious)
    distance = iou_to_distance(ious)
    print("The distance matrix is: " + str(distance.shape))
    print(distance)
    labels = clustering(distance)
    print("The labels are: ")
    print(labels)
