
import os, sys
import unittest
from path import Path
sys.path.insert(1, os.getcwd())
from graphh import *
from graphh.generators.geometric import *

class TestLocal(unittest.TestCase):

    def test_triangle(self):
        g = generate_polygon(3)

        # Points
        a = g.add_node('a')
        b = g.add_node('b')
        c = g.add_node('c')

        self.assertEqual(len(g), 3)
        self.assertEqual(g.number_of_nodes(), 3)
        self.assertEqual(g.number_of_edges(), 3)

        self.assertEqual(g.node_list(), set([a, b, c]))


    def test_square(self):
        g = generate_polygon(4)

        # Points
        a = g.add_node('a')
        b = g.add_node('b')
        c = g.add_node('c')
        d = g.add_node('d')

        self.assertEqual(len(g), 4)
        self.assertEqual(g.number_of_nodes(), 4)
        self.assertEqual(g.number_of_edges(), 4)

        self.assertEqual(g.node_list(), set([a, b, c, d]))


    def test_pentagon(self):
        g = generate_polygon(5)

        # Points
        a = g.add_node('a')
        b = g.add_node('b')
        c = g.add_node('c')
        d = g.add_node('d')
        e = g.add_node('e')

        self.assertEqual(len(g), 5)
        self.assertEqual(g.number_of_nodes(), 5)
        self.assertEqual(g.number_of_edges(), 5)

        self.assertEqual(g.node_list(), set([a, b, c, d, e]))

# The end
