
from .util import hash


class Events:

    def before_node_add(self, node_id):
        pass

    def after_node_add(self, node_id):
        pass

    def before_edge_add(self, edge_id):
        pass

    def after_edge_add(self, edge_id):
        pass


class Graph(Events):
    """
    Simple directed graph.

    Possible props:
      * nodes
      * edges
      * triples
      * chains
      * meta
      * indexes
    """

    __slots__ = ('_nodes', '_edges', '_adjacency')

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
        Represent instance as Python dictionaries, ready for serialization.
        """
        return {'n': dict(self._nodes), 'e': dict(self._edges)}

    def from_dict(self, data):
        """
        Load instance from Python dictionary.
        This will OVERWRITE all existing nodes and all existing edges!
        """
        self._edges.update(data['e'])
        self._nodes.update(data['n'])
        # Create the adjancency sets
        for key in self._nodes:
            self._adjacency[key] = (set(), set())
        # Restore the adjancency list
        for key, (head_id, tail_id) in self._edges.items():
            self._adjacency[tail_id][0].add(key)
            self._adjacency[head_id][1].add(key)


    def add_node(self, node_data, safe=True):
        """
        Adds a new node to the graph.
        The node must be a hashable value (number, string, binary).
        Adding the same node data twice will be silently ignored.
        """
        key = hash(node_data)
        if key in self._nodes:
            if safe:
                return key
            else:
                return False

        # Execute `before hook`
        self.before_node_add(key)
        self._nodes[key] = node_data
        # Execute `after hook`
        self.after_node_add(key)
        # index 0 -> incoming edges; index 1 -> outgoing edges;
        self._adjacency[key] = (set(), set())
        return key


    def add_edge(self, head_id, tail_id, safe=True):
        """
        Adds a directed edge going from head_id to tail_id
        """
        if head_id not in self._nodes or tail_id not in self._nodes:
            return False

        # Hashing the node ids
        key = hash(head_id, tail_id)
        if key in self._edges:
            if safe:
                return key
            else:
                return False

        # Execute `before hook`
        self.before_edge_add(key)
        self._edges[key] = (head_id, tail_id)
        # Execute `after hook`
        self.after_edge_add(key)
        # index 0 -> incoming edges; index 1 -> outgoing edges;
        self._adjacency[tail_id][0].add(key)
        self._adjacency[head_id][1].add(key)
        return key


    def add_bi_edge(self, head_id, tail_id):
        """
        Adds 2 directed edges between head_id and tail_id
        """
        self.add_edge(head_id, tail_id)
        self.add_edge(tail_id, head_id)


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


    def iter_nodes(self, values=True):
        """
        Iterates over all nodes in the graph
        """
        if values:
            return self._nodes.items()
        return iter(self._nodes)

    def iter_edges(self, values=True):
        """
        Iterates over all edges in the graph
        """
        if values:
            return self._edges.items()
        return iter(self._edges)


    def node_list(self) -> list:
        """
        Return a list with all node ids in the graph
        """
        return list(self._nodes.keys())

    def edge_list(self) -> list:
        """
        Return a list with all edge ids in the graph
        """
        return list(self._edges.keys())


    def edge_head(self, edge_id: bytes) -> bytes:
        """
        Returns the node of the head of the edge ID
        """
        return self._edges[edge_id][0]

    def edge_tail(self, edge_id: bytes) -> bytes:
        """
        Returns node of the tail of the edge ID
        """
        return self._edges[edge_id][1]


    def out_edges(self, node_id: bytes) -> set:
        """
        Returns a set with the outgoing edges
        """
        return set(self._adjacency[node_id][1])

    def inc_edges(self, node_id: bytes) -> set:
        """
        Returns a set with the incoming edges
        """
        return set(self._adjacency[node_id][0])

    def all_edges(self, node_id: bytes) -> set:
        """
        Returns a set with incoming and outging edges from a node
        """
        return set(self.inc_edges(node_id) + self.out_edges(node_id))


    def out_degree(self, node_id: bytes) -> int:
        """
        Returns the number of outgoing edges
        """
        out_edges = self._adjacency.get(node_id, (set(), set()))[1]
        return len(out_edges)

    def inc_degree(self, node_id: bytes) -> int:
        """
        Returns the number of incoming edges
        """
        inc_edges = self._adjacency.get(node_id, (set(), set()))[0]
        return len(inc_edges)

    def all_degree(self, node_id: bytes) -> int:
        """
        Returns the total degree of a node
        """
        return self.inc_degree(node_id) + self.out_degree(node_id)


# Eof()
