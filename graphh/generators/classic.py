
import itertools
from ..graph import Graph


def gen_complete_gr(size):
    """
    Generate a the complete graph.
    The size represents the number of points.
    https://en.wikipedia.org/wiki/Complete_graph
    """
    if size < 3:
        raise Exception('The size must be a number larger than 3')

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
