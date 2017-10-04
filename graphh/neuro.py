
from .graph import Graph
from .util import hash


class Neuro(Graph):
    """
    Neuro[n] engine.
    """

    __slots__ = ('_triples', )

    def __init__(self):
        super().__init__()
        self._triples = {}


    def to_dict(self):
        """
        Represent instance as Python dictionary.
        """
        out = super().to_dict()
        out.update({'t': self._triples})
        return out

    def from_dict(self, data):
        """
        Load instance from Python dictionary.
        This will OVERWRITE all existing triples and all existing quads!
        """
        super().from_dict(data)
        self._triples.update(data['t'])


    def add_triple(self, subject, predicate, thing):
        k1 = self.add_node(subject)
        k2 = self.add_node(predicate)
        k3 = self.add_node(thing)
        # print(f'Triple :: {subject} -> {predicate} -> {thing}')
        self.add_edge(k1, k2)
        self.add_edge(k2, k3)
        key = hash(k1, k2, k3)
        self._triples[key] = (k1, k2, k3)
        return key


    def query_subject(self, predicate):
        """
        Find all subjects from a predicate.
        Returns a generator.
        """
        pkey = hash(predicate)
        edges = self.inc_edges(pkey)
        if not edges:
            return False
        return (self.get_node_id(self.edge_head(e)) for e in edges)

    def query_thing(self, predicate):
        """
        Find all things from a predicate.
        Returns a generator.
        """
        pkey = hash(predicate)
        edges = self.out_edges(pkey)
        if not edges:
            return False
        return (self.get_node_id(self.edge_tail(e)) for e in edges)


    def query_triple(self, subject, predicate, thing):
        """
        Query for subject, predicate, or thing.
        And for any variation.
        This performs exact matches.
        """
        # Must specify something useful for the query
        if (subject, predicate, thing) == ('?', '?', '?'):
            return False
        skey = hash(subject)
        pkey = hash(predicate)
        tkey = hash(thing)
        result = []
        for (sk0y, pk0y, tk0y) in self._triples.values():
            if predicate != '?' and pkey != pk0y:
                continue
            if subject != '?' and skey != sk0y:
                continue
            if thing != '?' and tkey != tk0y:
                continue
            result.append((
                self.get_node_id(sk0y), self.get_node_id(pk0y), self.get_node_id(tk0y)
            ))
        return result


# Eof()
