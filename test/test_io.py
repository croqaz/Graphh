
import os, sys
import unittest
sys.path.insert(1, os.getcwd())
from graphh import *
from graphh.generators import *
from graphh.io import cbor, msgpack


class TestLocal(unittest.TestCase):

    def test_io_cbor(self):
        """
        Import-Export CBOR files
        """
        g = generate_polygon_gr(3)

        pth = 'test/g.cb'
        cbor.export_cbor(g, pth)
        assert os.path.isfile(pth)

        x = Graph()
        cbor.import_cbor(x, pth)

        self.assertEqual(g.node_list(), x.node_list())
        self.assertEqual(g.edge_list(), x.edge_list())

        os.remove(pth)


    def test_io_json(self):
        """
        Import-Export JSON files
        """
        g = generate_polygon_gr(4)

        pth = 'test/g.mp'
        msgpack.export_msgpack(g, pth)
        assert os.path.isfile(pth)

        x = Graph()
        msgpack.import_msgpack(x, pth)

        self.assertEqual(g.node_list(), x.node_list())
        self.assertEqual(g.edge_list(), x.edge_list())

        os.remove(pth)


# The end
