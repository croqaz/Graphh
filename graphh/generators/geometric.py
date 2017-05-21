
from ..graph import Graph

def generate_polygon(size):
    """
    Generate a polygon shaped graph.
    Size = 3 -> triangle
    Size = 4 -> square
    Size = 5 -> pentagon
    Etc..
    """
    if size <= 2:
        raise Error('The size must a number be larger than 3')
    if size > 26:
        raise Error('The size must a number be larger than 3')

    g = Graph()
    nodes = []

    # Adding nodes
    for i in range(1, 1 + size):
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
