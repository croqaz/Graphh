
from .util import hash


class Graph:
    """
    Directed graph engine.
    All iterations are lazy.

    Possible props:
      * nodes
      * edges
      * triples
      * chains
      * meta
      * indexes
    """

    def __init__(self):
        # The nodes are stored as:
        # Key -> (incoming-adjacency-list, outgoing-adjacency-list, value)
        self._nodes = {}
        # The edges are stored as:
        # Key -> (node_id, node_id)
        self._edges = {}

    def to_dict(self):
        """
        Represent instance as Python dictionary.
        """
        out = {'n': {}, 'e': self._edges}
        for k, ion in self._nodes.items():
            i, o, n = ion
            out['n'][k] = [list(i), list(o), n]
        return out

    def from_dict(self, data):
        """
        Load instance from Python dictionary.
        This will OVERWRITE all existing nodes and all existing edges!
        """
        self._edges.update(data['e'])
        for k, ion in data['n'].items():
            i, o, n = ion
            self._nodes[k] = [set(i), set(o), n]

    def add_node(self, node_data, safe=True):
        """
        Adds a new node to the graph.
        The node must be a hashable value.
        Adding the same node data twice will be silently ignored.
        """
        key = hash(node_data)
        # index 0 -> incoming edges
        # index 1 -> outgoing edges
        if key in self._nodes:
            if safe:
                return key
            else:
                return False
        self._nodes[key] = (set(), set(), node_data)
        return key

    def add_edge(self, head_id, tail_id, safe=True):
        """
        Adds a directed edge going from head_id to tail_id
        """
        if head_id in self._nodes and tail_id in self._nodes:
            # Hashing the node ids
            key = hash(head_id, tail_id)
            if key in self._edges:
                if safe:
                    return key
                else:
                    return False
            # index 0 -> incoming edges
            # index 1 -> outgoing edges
            self._nodes[tail_id][0].add(key)
            self._nodes[head_id][1].add(key)
            self._edges[key] = (head_id, tail_id)
            return key
        return False

    def add_bi_edge(self, head_id, tail_id):
        """
        Adds 2 directed edges between head_id and tail_id
        """
        self.add_edge(head_id, tail_id)
        self.add_edge(tail_id, head_id)


    def __iter__(self):
        """
        Iterates over all nodes in the graph
        """
        return iter(self._nodes)

    def __contains__(self, node):
        """
        Test whether a node is in the graph
        """
        return node in self._nodes

    def __len__(self):
        """
        Returns the number of nodes in the graph
        """
        return len(self._nodes)

    def get_node_id(self, node_id):
        """
        Returns the node data from the graph
        """
        return self._nodes.get(node_id, [False, False, False])[-1]

    def get_node(self, data):
        """
        Returns the node ID from the graph
        """
        key = hash(data)
        if key in self._nodes:
            return key
        return False

    def has_edge_id(self, edge_id):
        """
        Returns True if the edge ID is in the graph
        """
        return edge_id in self._edges

    def get_edge_id(self, edge_id):
        """
        Returns the edge ID from the graph
        """
        return self._edges.get(edge_id, False)

    def has_edge(self, head_id, tail_id):
        """
        Returns True if the edge (head_id, tail_id) is in the graph
        """
        key = hash(head_id, tail_id)
        return key in self._edges

    def get_edge(self, head_id, tail_id):
        """
        Returns the edge (head_id, tail_id) from the graph
        """
        key = hash(head_id, tail_id)
        if key in self._edges:
            return key
        return False

    def number_of_nodes(self):
        """
        Returns the number of nodes
        """
        return len(self._nodes)

    def number_of_edges(self):
        """
        Returns the number of edges
        """
        return len(self._edges)

    def node_list(self):
        """
        Return a set with all node ids in the graph
        """
        return set(self._nodes.keys())

    def edge_list(self):
        """
        Return a set with all edge ids in the graph
        """
        return set(self._edges.keys())

    def head(self, edge_id):
        """
        Returns the node of the head of the edge ID
        """
        return self._edges[edge_id][0]

    def tail(self, edge_id):
        """
        Returns node of the tail of the edge ID
        """
        return self._edges[edge_id][1]

    def out_edges(self, node_id):
        """
        Returns a list of the outgoing edges
        """
        return list(self._nodes[node_id][1])

    def inc_edges(self, node_id):
        """
        Returns a list of the incoming edges
        """
        return list(self._nodes[node_id][0])

    def all_edges(self, node_id):
        """
        Returns a list of incoming and outging edges from a node
        """
        return set(self.inc_edges(node_id) + self.out_edges(node_id))

    def out_degree(self, node_id):
        """
        Returns the number of outgoing edges
        """
        return len(self.out_edges(node_id))

    def inc_degree(self, node_id):
        """
        Returns the number of incoming edges
        """
        return len(self.inc_edges(node_id))

    def all_degree(self, node_id):
        """
        Returns the total degree of a node
        """
        return self.inc_degree(node_id) + self.out_degree(node_id)


# Eof()
