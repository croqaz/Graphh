
import os, sys # noqa: E401
sys.path.insert(1, os.getcwd())

from graphh.generators import generate_line_gr
from graphh.generators import generate_star_gr
from graphh.generators import generate_polygon_gr


def test_triangle():
    g = generate_polygon_gr(3)

    # Points
    a = g.add_node('a')
    b = g.add_node('b')
    c = g.add_node('c')

    points = {a: 'a', b: 'b', c: 'c'}

    for k, v in points.items():
        assert g.get_node_id(k) == v
        assert g.out_degree(k) == 1
        assert g.inc_degree(k) == 1
        assert g.all_degree(k) == 2

    assert g.has_edge(a, b)
    assert g.has_edge(c, a)

    assert g.out_edges(a) == set([g.get_edge(a, b)])
    assert g.inc_edges(a) == set([g.get_edge(c, a)])

    assert len(g) == 3
    assert g.number_of_nodes() == 3
    assert g.number_of_edges() == 3

    assert g.node_list() == [a, b, c]


def test_square():
    g = generate_polygon_gr(4)

    # Points
    a = g.add_node('a')
    b = g.add_node('b')
    c = g.add_node('c')
    d = g.add_node('d')

    points = {a: 'a', b: 'b', c: 'c', d: 'd'}

    for k, v in points.items():
        assert g.get_node_id(k) == v
        assert g.out_degree(k) == 1
        assert g.inc_degree(k) == 1
        assert g.all_degree(k) == 2

    assert g.has_edge(a, b)
    assert g.has_edge(b, c)

    assert len(g) == 4
    assert g.number_of_nodes() == 4
    assert g.number_of_edges() == 4

    assert g.node_list() == [a, b, c, d]


def test_star():
    g = generate_star_gr(5)

    # Points
    z = g.add_node(0)
    a = g.add_node('a')
    b = g.add_node('b')
    c = g.add_node('c')
    d = g.add_node('d')
    e = g.add_node('e')

    points = [a, b, c, d, e]

    assert len(g) == len(points) + 1
    assert g.number_of_nodes() == len(points) + 1
    assert g.number_of_edges() == len(points)

    assert g.node_list() == [z, a, b, c, d, e]


def test_line():
    g = generate_line_gr(100)
    assert len(g) == 100
    assert g.number_of_nodes() == 100
    assert g.number_of_edges() == 99


# The end
