import numpy as np
import scipy
import torch
from torchvision import ops
from sklearn.cluster import DBSCAN

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

# Return intersection-over-union (Jaccard index) between two sets of boxes.
def box_iou(boxes1, boxes2):
    inter, union = _box_inter_union(boxes1, boxes2)
    iou = inter / union
    return iou

def iou_to_distance(matrix):
    return 1 - matrix

def clustering(distance_matrix):
    dbscan = DBSCAN(eps=0.75, min_samples=2, metric='precomputed')
    labels = dbscan.fit_predict(distance_matrix)
    return labels

# Calculate the median of each component within a cluster
def median_component(component_list):
    # Sort the numbers in ascending order
    sorted_list = sorted(component_list)  
    # Get the length of the sorted list
    length_list = len(sorted_list)  
    # If the length is even
    if length_list % 2 == 0:  
        median = (sorted_list[length_list // 2 - 1] + sorted_list[length_list // 2]) / 2
    # If the length is odd
    else:  
        median = sorted_list[length_list // 2]
    return median

# Group the components of the images within a cluster to calculate the median
def median_cluster_xywh(cluster_xywh):
    coordinate_x = []
    coordinate_y = []
    width = []
    height = []
    for image in cluster_xywh:
        coordinate_x.append(float(image[0]))
        coordinate_y.append(float(image[1]))
        width.append(float(image[2]))
        height.append(float(image[3]))
    return [str(median_component(coordinate_x)), str(median_component(coordinate_y)), str(median_component(width)), str(median_component(height))]

# Get the all the clusters in the image and assign them a final label
def get_clusters_per_image(identifications_image):
    # Define the arrays to work with coordinates and labels
    box_coordinates_string = []
    bbox_labels = []
    # Dictionary containing the final cluster's labels
    final_labels = {}
    # Array containing the final xywh format and label of the final clusters of an image
    final_clusters_image = []
    
    # Let's work from the original coordinates in x, y, w, h format and with string type
    for identification in identifications_image:
        box_coordinates_string.append([identification['coordinateX'], identification['coordinateY'], identification['width'], identification['height']])
        bbox_labels.append(identification['parasite'])
    # Convert to float
    box_coordinates_xywh = [np.array(image).astype(np.float64) for image in box_coordinates_string]
    # now transform the xywh format to xyxy
    box_coordinates_xyxy = [xywh_to_xyxy(image) for image in box_coordinates_xywh]
    # Create the numpy array
    box_coordinates_xyxy = np.stack(box_coordinates_xyxy)
    ious = box_iou(box_coordinates_xyxy, box_coordinates_xyxy)
    distance = iou_to_distance(ious)
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
    # end of label information. From now on, as before
    cluster_labels = clustering(combined_distance)
    # Get the number of clusters that have been detected
    number_clusters = max(cluster_labels) + 1
    # Create an array with as many positions as clusters (not including noise cluster)
    images_to_final_image = []
    for index in range(number_clusters):
        images_to_final_image.append([])
    # Loop through the clusters
    for index, cluster in enumerate(cluster_labels):
        # Real cluster
        if cluster >= 0:
            images_to_final_image[cluster].append(box_coordinates_string[index])
            # Check if the current label is not in the dictionary to add it
            if not bbox_labels[index] in final_labels:
                final_labels[str(cluster)] = bbox_labels[index]
    # Calculate the median for each cluster
    for index, cluster in enumerate(images_to_final_image):
        final_median_cluster = median_cluster_xywh(cluster)
        final_clusters_image.append(final_median_cluster + [final_labels[str(index)]])
    return final_clusters_image