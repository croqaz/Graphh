
import os, sys
import unittest
sys.path.insert(1, os.getcwd())
from graphh import *
from graphh.generators import *


class TestLocal(unittest.TestCase):

    def test_triangle(self):
        g = generate_polygon_gr(3)

        # Points
        a = g.add_node('a')
        b = g.add_node('b')
        c = g.add_node('c')

        points = {a: 'a', b: 'b', c: 'c'}

        for k, v in points.items():
            self.assertEqual(g.get_node_id(k), v)
            self.assertEqual(g.out_degree(k), 1)
            self.assertEqual(g.inc_degree(k), 1)
            self.assertEqual(g.all_degree(k), 2)

        self.assertTrue(g.has_edge(a, b))
        self.assertTrue(g.has_edge(c, a))

        self.assertListEqual(g.out_edges(a), [g.get_edge(a, b)])
        self.assertListEqual(g.inc_edges(a), [g.get_edge(c, a)])

        self.assertEqual(len(g), 3)
        self.assertEqual(g.number_of_nodes(), 3)
        self.assertEqual(g.number_of_edges(), 3)

        self.assertEqual(g.node_list(), set([a, b, c]))


    def test_square(self):
        g = generate_polygon_gr(4)

        # Points
        a = g.add_node('a')
        b = g.add_node('b')
        c = g.add_node('c')
        d = g.add_node('d')

        points = {a: 'a', b: 'b', c: 'c', d: 'd'}

        for k, v in points.items():
            self.assertEqual(g.get_node_id(k), v)
            self.assertEqual(g.out_degree(k), 1)
            self.assertEqual(g.inc_degree(k), 1)
            self.assertEqual(g.all_degree(k), 2)

        self.assertTrue(g.has_edge(a, b))
        self.assertTrue(g.has_edge(b, c))

        self.assertEqual(len(g), 4)
        self.assertEqual(g.number_of_nodes(), 4)
        self.assertEqual(g.number_of_edges(), 4)

        self.assertEqual(g.node_list(), set([a, b, c, d]))


    def test_pentagon(self):
        g = generate_polygon_gr(5)

        # Points
        a = g.add_node('a')
        b = g.add_node('b')
        c = g.add_node('c')
        d = g.add_node('d')
        e = g.add_node('e')

        points = set([a, b, c, d, e])

        self.assertEqual(len(g), len(points))
        self.assertEqual(g.number_of_nodes(), len(points))
        self.assertEqual(g.number_of_edges(), len(points))

        self.assertEqual(g.node_list(), points)


    def test_line(self):
        g = generate_line_gr(100)
        self.assertEqual(len(g), 100)
        self.assertEqual(g.number_of_nodes(), 100)
        self.assertEqual(g.number_of_edges(), 99)


# The end
