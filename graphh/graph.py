
from .util import hash


class Graph:
    """
    Directed graph engine.

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
        # Key -> Value
        self._nodes = {}
        # Indexed (incoming-adjacency-list, outgoing-adjacency-list)
        self._adjacency = {}
        # The edges are stored as:
        # Key -> (node_id, node_id)
        self._edges = {}


    def to_dict(self):
        """
        Represent instance as Python dictionary.
        """
        return {'n': self._nodes, 'e': self._edges}

    def from_dict(self, data):
        """
        Load instance from Python dictionary.
        This will OVERWRITE all existing nodes and all existing edges!
        """
        self._edges.update(data['e'])
        self._nodes.update(data['n'])
        # Restore the adjancency list
        # for node in self._nodes:


    def add_node(self, node_data, safe=True):
        """
        Adds a new node to the graph.
        The node must be a hashable value.
        Adding the same node data twice will be silently ignored.
        """
        key = hash(node_data)
        if key in self._nodes:
            if safe:
                return key
            else:
                return False
        # index 0 -> incoming edges
        # index 1 -> outgoing edges
        self._nodes[key] = node_data
        self._adjacency[key] = (set(), set())
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
            self._edges[key] = (head_id, tail_id)
            self._adjacency[tail_id][0].add(key)
            self._adjacency[head_id][1].add(key)
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

    def __contains__(self, node_id):
        """
        Test whether a node is in the graph
        """
        return node_id in self._nodes

    def __len__(self):
        """
        Returns the number of nodes in the graph
        """
        return len(self._nodes)

    def get_node_id(self, node_id):
        """
        Returns the node data from the graph
        """
        return self._nodes.get(node_id, False)

    def get_node(self, node_data):
        """
        Returns the node ID from the graph
        """
        key = hash(node_data)
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

    def edge_head(self, edge_id):
        """
        Returns the node of the head of the edge ID
        """
        return self._edges[edge_id][0]

    def edge_tail(self, edge_id):
        """
        Returns node of the tail of the edge ID
        """
        return self._edges[edge_id][1]

    def out_edges(self, node_id):
        """
        Returns a list of the outgoing edges
        """
        return list(self._adjacency[node_id][1])

    def inc_edges(self, node_id):
        """
        Returns a list of the incoming edges
        """
        return list(self._adjacency[node_id][0])

    def all_edges(self, node_id):
        """
        Returns a list of incoming and outging edges from a node
        """
        return set(self.inc_edges(node_id) + self.out_edges(node_id))

    def out_degree(self, node_id):
        """
        Returns the number of outgoing edges
        """
        out_edges = self._adjacency[node_id][1]
        return len(out_edges)

    def inc_degree(self, node_id):
        """
        Returns the number of incoming edges
        """
        inc_edges = self._adjacency[node_id][0]
        return len(inc_edges)

    def all_degree(self, node_id):
        """
        Returns the total degree of a node
        """
        return self.inc_degree(node_id) + self.out_degree(node_id)


# Eof()
