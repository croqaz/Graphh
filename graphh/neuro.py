
#- rev: v1 -
#- hash: 277WHB -

from .graph import Graph
from .util import hash
from stones import MemoryStore


def create_matcher(part, where):
    """
    Create a matcher function
    """
    # Starts with
    if where == '<':
        return lambda t: t.startswith(part)
    # Ends with
    if where == '>':
        return lambda t: t.endswith(part)
    # Contains
    return lambda t: part in t


class Neuro(Graph):
    """
    Neuro[n] engine.
    """

    __slots__ = ('_triples', )

    def __init__(self):
        super().__init__()
        self._triples = MemoryStore(encoder='noop')


    def to_dict(self) -> dict:
        """
        Represent instance as Python dictionary.
        """
        out = super().to_dict()
        out.update({'t': dict(self._triples)})
        return out


    def from_dict(self, data: dict):
        """
        Load instance from Python dictionary.
        This will OVERWRITE all existing triples and all existing quads!
        """
        super().from_dict(data)
        self._triples.update(data['t'])


    def add_triple(self, subject: str, predicate: str, thing: str):
        """
        Create a (Subject -> Predicate -> Thing) relation.
        Examples:
        * RO -> official_name -> Romania
        * RO -> capital -> Bucharest
        * RO -> area_size -> 238391
        """
        k1 = self.add_node(subject)
        k2 = self.add_node(predicate)
        k3 = self.add_node(thing)
        # print(f'Triple :: {subject} -> {predicate} -> {thing}')
        self.add_edge(k1, k2)
        self.add_edge(k2, k3)
        key = hash(k1, k2, k3)
        self._triples[key] = (k1, k2, k3)
        return key


    def query_subject(self, predicate: str, match='', where=''):
        """
        Find subjects connected to a predicate.
        Returns a generator.
        """
        pkey = hash(predicate)
        edges = self.inc_edges(pkey)
        if not edges:
            return False
        if not match:
            # Just return all subjects
            for e in edges:
                yield self.get_node_id(self.edge_head(e))
        else:
            # Match some subjects
            matches = create_matcher(match, where)
            for e in edges:
                t = self.get_node_id(self.edge_head(e))
                if matches(t):
                    yield t

    def query_thing(self, predicate: str, match='', where=''):
        """
        Find things connected to a predicate.
        Returns a generator.
        """
        pkey = hash(predicate)
        edges = self.out_edges(pkey)
        if not edges:
            return False
        if not match:
            # Just return all things
            for e in edges:
                yield self.get_node_id(self.edge_tail(e))
        else:
            # Match some things
            matches = create_matcher(match, where)
            for e in edges:
                t = self.get_node_id(self.edge_tail(e))
                if matches(t):
                    yield t


    def query_triple(self, subject: str, predicate: str, thing: str):
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
