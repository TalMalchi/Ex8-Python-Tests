from math import ceil
from unittest import TestCase
from src.Point import Point
import networkx as nx


class test_Point(TestCase):

    def test_point(self):
        p1 = Point(1.0, 2.0, 3.5)
        self.assertEqual(p1.getY(), 2.0)
        p1.setX(2.4)
        self.assertEqual(p1.getX(), 2.4)
        self.assertEqual(p1.getZ(), 3.5)
        p1.setZ(4.7)
        self.assertEqual(p1.getZ(), 4.7)
        p2 = Point(1.5, 2.0, 4.5)
        self.assertEqual(p1.getY(), p2.getY())
        p2.setZ(4.7)
        self.assertEqual(p2.getZ(), p1.getZ())
        p3 = Point(1.0, 2.0, 4.0)
        p4 = Point(2.0, 3.0, 5.0)
        dist = p3.distance(p4)
        self.assertEqual(ceil(dist), 2)
        p4.setX(3.0)
        dist = p3.distance(p4)
        self.assertEqual(ceil(dist), 3)



if __name__ == '__main__':
    unittest.main()










