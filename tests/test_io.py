
import os, sys # noqa: E401
sys.path.insert(1, os.getcwd())

from graphh import Graph
from graphh.io import cbor, msgpack, csv
from graphh.generators import gen_complete_gr


def test_io_cbor():
    """
    Import-Export CBOR files
    """
    g = gen_complete_gr(9)

    pth = 'tests/g.cb'
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
    g = gen_complete_gr(8)

    pth = 'tests/g.mp'
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
    g = gen_complete_gr(7)

    n_pth = 'tests/nodes.csv'
    e_pth = 'tests/edges.csv'
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
