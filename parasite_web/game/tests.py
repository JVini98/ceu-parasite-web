from django.test import TestCase
from clustering import get_clusters_per_image

import unittest

# Create your tests here.
class TestClustering(unittest.TestCase):
    # Test to apply median (average of the two central values)
    def test_one_cluster_two_identifications(self):
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

    def test_no_cluster_diff_coordy(self):
        identifications = []
        identifications.append({'coordinateX': 1000, 'coordinateY': 3000, 'width': 200, 'height':100, 'parasite': "A"})
        identifications.append({'coordinateX': 1050, 'coordinateY': 1650, 'width': 150, 'height':110, 'parasite': "A"})
        
        expected_clusters = []
        calculated_cluster = get_clusters_per_image(identifications)
        
        self.assertEqual(expected_clusters, calculated_cluster)
    
    def test_no_cluster_diff_width(self):
        identifications = []
        identifications.append({'coordinateX': 1000, 'coordinateY': 1700, 'width': 500, 'height':100, 'parasite': "A"})
        identifications.append({'coordinateX': 1050, 'coordinateY': 1650, 'width': 150, 'height':110, 'parasite': "A"})
        
        expected_clusters = []
        calculated_cluster = get_clusters_per_image(identifications)
        
        self.assertEqual(expected_clusters, calculated_cluster)
    
    def test_no_cluster_diff_height(self):
        identifications = []
        identifications.append({'coordinateX': 1000, 'coordinateY': 1700, 'width': 200, 'height':800, 'parasite': "A"})
        identifications.append({'coordinateX': 1050, 'coordinateY': 1650, 'width': 150, 'height':110, 'parasite': "A"})
        
        expected_clusters = []
        calculated_cluster = get_clusters_per_image(identifications)
        
        self.assertEqual(expected_clusters, calculated_cluster)
    
    # Test to apply median (central value)
    def test_one_cluster_three_identifications(self):
        identifications = []
        identifications.append({'coordinateX': 1000, 'coordinateY': 1700, 'width': 200, 'height':100, 'parasite': "A"})
        identifications.append({'coordinateX': 1050, 'coordinateY': 1650, 'width': 150, 'height':110, 'parasite': "A"})
        identifications.append({'coordinateX': 1100, 'coordinateY': 1650, 'width': 225, 'height':95, 'parasite': "A"})
        
        expected_clusters = [["1050.0", "1650.0", "200.0", "100.0", "A"]]
        calculated_cluster = get_clusters_per_image(identifications)
        
        self.assertEqual(expected_clusters, calculated_cluster)
    
    def test_cluster_with_noise(self):
        identifications = []
        identifications.append({'coordinateX': 1000, 'coordinateY': 1700, 'width': 200, 'height':100, 'parasite': "A"})
        identifications.append({'coordinateX': 1050, 'coordinateY': 1650, 'width': 150, 'height':110, 'parasite': "A"})
        identifications.append({'coordinateX': 1100, 'coordinateY': 1650, 'width': 225, 'height':95, 'parasite': "B"})
        
        expected_clusters = [["1025.0", "1675.0", "175.0", "105.0", "A"]]
        calculated_cluster = get_clusters_per_image(identifications)
        
        self.assertEqual(expected_clusters, calculated_cluster)

if __name__ == "__main__":
    unittest.main()

