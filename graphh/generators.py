
import itertools
from .graph import Graph


def generate_line_gr(size):
    """
    Generate a long line graph.
    The size represents the number of points.
    There is no upper size limit.
    """
    if size <= 1:
        raise Exception('The size must be a number larger than 2')

    g = Graph()
    nodes = []

    # Adding nodes as numbers
    for i in range(1, size + 1):
        node = g.add_node(i)
        nodes.append(node)
    # Adding edges
    for i in range(len(nodes)):
        if i < len(nodes) - 1:
            g.add_edge(nodes[i], nodes[i + 1])

    # Basic validation
    assert g.number_of_nodes() == size
    assert g.number_of_edges() == size - 1
    return g


def generate_star_gr(size):
    """
    Generate a star graph.
    The size represents the number of edges.
    """
    if size <= 1:
        raise Exception('The size must be a number larger than 2')
    if size > 26:
        raise Exception('The size must be a number smaller than 26')

    g = Graph()
    nodes = []

    # Add central point
    root = g.add_node(0)

    # Adding nodes as numbers
    for i in range(1, size + 1):
        node = g.add_node(i)
        nodes.append(node)
    # Adding edges
    for n in nodes:
        g.add_edge(root, n)

    # Basic validation
    assert g.number_of_nodes() == size + 1
    assert g.number_of_edges() == size
    return g


def generate_polygon_gr(size):
    """
    Generate a polygon shaped graph (cycle graph).
    Size = 3 -> triangle
    Size = 4 -> square
    Size = 5 -> pentagon
    Size = 6 -> hexagon
    Etc...
    """
    if size <= 1:
        raise Exception('The size must be a number larger than 2')
    if size > 26:
        raise Exception('The size must be a number smaller than 26')

    g = Graph()
    nodes = []

    # Adding nodes as letters
    for i in range(1, size + 1):
        node = g.add_node(chr(i + 96))
        nodes.append(node)
    # Adding edges
    for i in range(len(nodes)):
        if i == len(nodes) - 1:
            g.add_edge(nodes[i], nodes[0])
        else:
            g.add_edge(nodes[i], nodes[i + 1])

    # Basic validation
    assert g.number_of_nodes() == size
    assert g.number_of_edges() == size
    return g


def gen_complete_gr(size):
    """
    Generate a the complete graph.
    The size represents the number of points.
    https://en.wikipedia.org/wiki/Complete_graph
    """
    if size <= 1:
        raise Exception('The size must be a number larger than 1')

    g = Graph()
    nodes = []

    # Adding nodes as letters
    for i in range(1, size + 1):
        node = g.add_node(chr(i + 96))
        nodes.append(node)
    # Adding edges
    for pair in itertools.permutations(nodes, 2):
        g.add_edge(*pair)

    # Basic validation
    assert g.number_of_nodes() == size
    assert g.number_of_edges() == size * (size - 1)
    return g


def gen_ladder_gr(height):
    """
    Generate a ladder graph.
    The height represents the height of the ladder.
    https://en.wikipedia.org/wiki/Ladder_graph
    """
    if height <= 0:
        raise Exception('The height must be a number larger than zero')

    g = Graph()
    nodes = []
    gr_height = height * 2

    # Adding nodes as letters
    for i in range(1, (gr_height + 1)):
        node = g.add_node(chr(i + 96))
        nodes.append(node)
    # Adding edges
    for i in range(gr_height):
        if i % 2:
            g.add_edge(nodes[i-1], nodes[i])
    for i in range(0, (gr_height - 2)):
        g.add_edge(nodes[i], nodes[i+2])

    # Basic validation
    assert g.number_of_nodes() == gr_height
    assert g.number_of_edges() == height + 2 * (height - 1)
    return g


# The end
