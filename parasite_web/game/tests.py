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

    def test_cluster_with_noise_2(self):
        identifications = []
        identifications.append({'coordinateX': 1000, 'coordinateY': 1700, 'width': 200, 'height':100, 'parasite': "A"})
        identifications.append({'coordinateX': 1050, 'coordinateY': 1650, 'width': 150, 'height':110, 'parasite': "A"})
        identifications.append({'coordinateX': 1100, 'coordinateY': 1650, 'width': 225, 'height':95, 'parasite': "B"})
        identifications.append({'coordinateX': 1100, 'coordinateY': 1650, 'width': 225, 'height':95, 'parasite': "C"})

        expected_clusters = [["1025.0", "1675.0", "175.0", "105.0", "A"]]
        calculated_cluster = get_clusters_per_image(identifications)
        
        self.assertEqual(expected_clusters, calculated_cluster)
    
    def test_two_clusters(self):
        identifications = []
        identifications.append({'coordinateX': 1000, 'coordinateY': 1700, 'width': 200, 'height':100, 'parasite': "A"})
        identifications.append({'coordinateX': 1050, 'coordinateY': 1650, 'width': 150, 'height':110, 'parasite': "A"})
        identifications.append({'coordinateX': 1500, 'coordinateY': 1700, 'width': 300, 'height':150, 'parasite': "B"})
        identifications.append({'coordinateX': 1530, 'coordinateY': 1760, 'width': 200, 'height':75, 'parasite': "B"})

        expected_clusters = [["1025.0", "1675.0", "175.0", "105.0", "A"], ["1515.0", "1730.0", "250.0", "112.5", "B"]]
        calculated_cluster = get_clusters_per_image(identifications)
        
        self.assertEqual(expected_clusters, calculated_cluster)

    def test_real_values(self):
        identifications = []
        identifications.append({'coordinateX': 867.8490849909888, 'coordinateY': 568.3798980744398, 'width': 832.0087912052827, 'height':468.0049450529716, 'parasite': "A"})
        identifications.append({'coordinateX': 679.3439511375462, 'coordinateY': 469.190797093177, 'width': 1107.403701094231, 'height':622.914581865505, 'parasite': "A"})

        expected_clusters = [["773.5965180642675", "518.7853475838084", "969.7062461497569", "545.4597634592383", "A"]]
        calculated_cluster = get_clusters_per_image(identifications)
        
        self.assertEqual(expected_clusters, calculated_cluster)

if __name__ == "__main__":
    unittest.main()

