
import os, sys
import unittest
from path import Path
sys.path.insert(1, os.getcwd())
from graphh import *

class TestLocal(unittest.TestCase):

    def test_triangle(self):
        g = Graph()

        # Points
        a = g.add_node('a')
        b = g.add_node('b')
        c = g.add_node('c')
        # Connections
        g.add_edge(a, b)
        g.add_edge(b, c)
        g.add_edge(c, a)

        self.assertEqual(len(g), 3)
        self.assertEqual(g.number_of_nodes(), 3)
        self.assertEqual(g.number_of_edges(), 3)

        self.assertEqual(g.node_list(), set([a, b, c]))


    def test_square(self):
        g = Graph()

        # Points
        a = g.add_node('a')
        b = g.add_node('b')
        c = g.add_node('c')
        d = g.add_node('d')
        # Connections
        g.add_edge(a, b)
        g.add_edge(b, c)
        g.add_edge(c, d)
        g.add_edge(d, a)

        self.assertEqual(len(g), 4)
        self.assertEqual(g.number_of_nodes(), 4)
        self.assertEqual(g.number_of_edges(), 4)

        self.assertEqual(g.node_list(), set([a, b, c, d]))

# The end
