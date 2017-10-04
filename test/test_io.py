
import os, sys
sys.path.insert(1, os.getcwd())

from graphh import Graph
from graphh.io import cbor, msgpack, csv
from graphh.generators import generate_polygon_gr


def test_io_cbor():
    """
    Import-Export CBOR files
    """
    g = generate_polygon_gr(3)

    pth = 'test/g.cb'
    cbor.export_cbor(g, pth)
    assert os.path.isfile(pth)

    x = Graph()
    cbor.import_cbor(x, pth)

    assert g.number_of_nodes() == x.number_of_nodes()

    assert g.node_list() == x.node_list()
    assert g.edge_list() == x.edge_list()

    os.remove(pth)


def test_io_mpack():
    """
    Import-Export MsgPack files
    """
    g = generate_polygon_gr(4)

    pth = 'test/g.mp'
    msgpack.export_msgpack(g, pth)
    assert os.path.isfile(pth)

    x = Graph()
    msgpack.import_msgpack(x, pth)

    assert g.number_of_nodes() == x.number_of_nodes()

    assert g.node_list() == x.node_list()
    assert g.edge_list() == x.edge_list()

    os.remove(pth)


def test_io_csv():
    """
    Import-Export CSV files
    """
    g = generate_polygon_gr(4)

    n_pth = 'test/nodes.csv'
    e_pth = 'test/edges.csv'
    csv.export_csv(g, n_pth, e_pth)
    assert os.path.isfile(n_pth)
    assert os.path.isfile(e_pth)

    x = Graph()
    csv.import_csv(x, n_pth, e_pth)

    assert g.number_of_nodes() == x.number_of_nodes()

    assert g.node_list() == x.node_list()
    assert g.edge_list() == x.edge_list()

    os.remove(n_pth)
    os.remove(e_pth)


# The end
