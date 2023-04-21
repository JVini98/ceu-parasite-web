import numpy as np
import scipy
import torch
from torchvision import ops
from sklearn.cluster import DBSCAN

# image = [top-leftx, top-lefty, width, height]
image1 = ["1149.7215179505479", "725.0646330096754", "516.6119994320322", "290.59424968051815"]
image2 = ["1200", "780", "520", "295"]
image3 = ["1617.8857662906719", "218.1067835582991", "299.92178394329227", "168.7060034681019"]
image4 = ["1700", "225.1067835582991", "300", "168.7060034681019"]
image5 = ["495.6243064641784", "408.49842165746287", "531.329735484363", "298.8729762099542"]
image6 = ["1000", "1700", "200", "100"]
image7 = ["1050", "1650", "150", "110"]
bbox_labels = ["A", "B", "C", "C", "A", "C", "C"]

# Define a function to transform bbox format
def xywh_to_xyxy(bbox):
    x, y, w, h = bbox
    return [x, y, x + w, y + h]

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
    # I think that a reasonable value for eps is 0.75. Let's experiment with that
    dbscan = DBSCAN(eps=0.75, min_samples=2, metric='precomputed')
    labels = dbscan.fit_predict(distance_matrix)
    return labels

if __name__ == "__main__":
    # Let's work from the original coordinates in x, y, w, h format and with string type
    box_coordinates_string = [image1, image2, image3, image4, image5, image6, image7]
    # We first convert to float
    box_coordinates_xywh = [np.array(image).astype(np.float64) for image in box_coordinates_string]
    # now transform the xywh format to xyxy
    box_coordinates_xyxy = [xywh_to_xyxy(image) for image in box_coordinates_xywh]
    # Create the numpy array
    box_coordinates_xyxy = np.stack(box_coordinates_xyxy)
    ious = box_iou(box_coordinates_xyxy, box_coordinates_xyxy)
    print("The IoU matrix is: " + str(ious.shape))
    print(ious)
    distance = iou_to_distance(ious)
    print("The distance matrix is: " + str(distance.shape))
    print(distance)
    # Use label information: The label information is used to penalize the distance between boxes with different labels
    # 1) from list to a np.array of shape (n, 1), being n the number of boxes
    bbox_labels_np = np.array(bbox_labels).reshape(-1, 1)
    # 2) compute the distance between labels (0 if equal, 1 if different). This returns a condensed matrix ...
    condensed_dist = scipy.spatial.distance.pdist(bbox_labels_np, lambda x, y: 0 if x == y else 1)
    # ... which is converted to a standard square matrix
    labels_dist = scipy.spatial.distance.squareform(condensed_dist)
    # 3) add the label distance to the original distance. We use a large number (10, which is large compared to 1)
    # to make sure that the label distance separates close boxes with similar labels
    combined_distance = distance + 10 * labels_dist
    print("The combined distance matrix is: " + str(combined_distance.shape))
    print(combined_distance)
    # end of label information. From now on, as before
    cluster_labels = clustering(combined_distance)
    print("The labels are: ")
    print(cluster_labels)

    # Plot the boxes with the labels. Each color represents a different cluster. Red is the noise cluster.
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches
    fig, ax = plt.subplots(1)
    colors = ['r', 'g', 'b', 'c', 'm', 'y', 'k', 'w']
    X = np.ones((2500, 2500))
    fig, ax = plt.subplots(1)
    ax.imshow(X)
    for i in range(len(box_coordinates_xywh)):
        box = box_coordinates_xywh[i]
        label = bbox_labels[i]
        x, y, w, h = box
        color = colors[cluster_labels[i] + 1]
        rect = patches.Rectangle((x, y), w, h, linewidth=2, edgecolor=color, facecolor='none')
        ax.text(x, y, label, fontsize=20, color=color)
        ax.add_patch(rect)
    plt.show()
