import unittest
from shapely.geometry import MultiPoint

class TestConvexHull(unittest.TestCase):

    def test_convex_hull_example(self):
        pts = MultiPoint([(16,3), (12,17), (0,6), (-4,-6), (16,6), (16,-7), (16,-3), (17,-4), (5,19), (19,-8), (3,16), (12,13), (3,-4), (17,5), (-3,15), (-3,-9), (0,11), (-9,-3), (-4,-2), (12,10)])
        expected_hull_points = [(-9, -3), (-3, -9), (19, -8), (17, 5), (12, 17), (5, 19), (-3, 15)]
        actual_hull = pts.convex_hull
        self.assertEqual(len(actual_hull.exterior.coords), len(expected_hull_points) + 1) # +1 because polygon is closed
        for point in expected_hull_points:
            self.assertIn(point, actual_hull.exterior.coords)


    def test_convex_hull_single_point(self):
        pts = MultiPoint([(0, 0)])
        hull = pts.convex_hull
        self.assertEqual(len(hull.exterior.coords), 1)  # Point
        self.assertEqual(hull.exterior.coords[0], (0.0, 0.0))

    def test_convex_hull_two_points(self):
        pts = MultiPoint([(0, 0), (1, 1)])
        hull = pts.convex_hull
        self.assertEqual(len(hull.exterior.coords), 3) # Linestring represented as closed polygon
        self.assertIn((0.0, 0.0), hull.exterior.coords)
        self.assertIn((1.0, 1.0), hull.exterior.coords)

    def test_convex_hull_collinear_points(self):
        pts = MultiPoint([(0, 0), (1, 1), (2, 2)])
        hull = pts.convex_hull
        self.assertEqual(len(hull.exterior.coords), 3) # Linestring
        self.assertIn((0.0, 0.0), hull.exterior.coords)
        self.assertIn((2.0, 2.0), hull.exterior.coords)

    def test_convex_hull_square(self):
        pts = MultiPoint([(0, 0), (1, 0), (1, 1), (0, 1)])
        hull = pts.convex_hull
        self.assertEqual(len(hull.exterior.coords), 5)  # Polygon
        self.assertIn((0.0, 0.0), hull.exterior.coords)
        self.assertIn((1.0, 0.0), hull.exterior.coords)
        self.assertIn((1.0, 1.0), hull.exterior.coords)
        self.assertIn((0.0, 1.0), hull.exterior.coords)

    def test_convex_hull_empty(self):
        pts = MultiPoint([])  # Empty MultiPoint
        hull = pts.convex_hull
        self.assertTrue(hull.is_empty)  # Check if the hull is empty


