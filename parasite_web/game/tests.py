from django.test import TestCase
from clustering import get_clusters_per_image

import unittest

# Create your tests here.
class TestClustering(unittest.TestCase):
    def test_one_cluster(self):
        identifications = []
        identifications.append({'coordinateX': 1000, 'coordinateY': 1700, 'width': 200, 'height':100, 'parasite': "A"})
        identifications.append({'coordinateX': 1050, 'coordinateY': 1650, 'width': 150, 'height':110, 'parasite': "A"})
        
        expected_clusters = [["1025.0", "1675.0", "175.0", "105.0", "A"]]
        calculated_cluster = get_clusters_per_image(identifications)
        
        self.assertEqual(expected_clusters, calculated_cluster)
    
    def test_no_cluster_diff_parasite(self):
        identifications = []
        identifications.append({'coordinateX': 1000, 'coordinateY': 1700, 'width': 200, 'height':100, 'parasite': "A"})
        identifications.append({'coordinateX': 1050, 'coordinateY': 1650, 'width': 150, 'height':110, 'parasite': "B"})
        
        expected_clusters = []
        calculated_cluster = get_clusters_per_image(identifications)
        
        self.assertEqual(expected_clusters, calculated_cluster)
    
    def test_no_cluster_diff_coordx(self):
        identifications = []
        identifications.append({'coordinateX': 5000, 'coordinateY': 1700, 'width': 200, 'height':100, 'parasite': "A"})
        identifications.append({'coordinateX': 1000, 'coordinateY': 1650, 'width': 150, 'height':110, 'parasite': "A"})
        
        expected_clusters = []
        calculated_cluster = get_clusters_per_image(identifications)
        
        self.assertEqual(expected_clusters, calculated_cluster)

if __name__ == "__main__":
    unittest.main()

