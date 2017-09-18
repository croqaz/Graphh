
from ..graph import Graph


def generate_line_gr(size):
    """
    Generate a long line graph.
    The size represents the number of points.
    There is no size limit.
    """
    if size < 2:
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


def generate_polygon_gr(size):
    """
    Generate a polygon shaped graph.
    Size = 3 -> triangle
    Size = 4 -> square
    Size = 5 -> pentagon
    Etc..
    """
    if size <= 2:
        raise Exception('The size must be a number larger than 3')
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


# The end
