
#- rev: v2 -
#- hash: VPOTST -

from .graph import Graph
from .util import hash
from stones import MemoryStore


def create_matcher(part: str, where: str):
    """
    Create a matcher function
    """
    # Strictly equal
    if where == '=':
        return lambda t: t == part
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

    __slots__ = ('_sp', '_pt')

    def __init__(self):
        super().__init__()
        # subject + predicate -> things
        self._sp = MemoryStore(encoder='noop')
        # predicate + thing -> subjects
        self._pt = MemoryStore(encoder='noop')


    def to_dict(self) -> dict:
        """
        Represent instance as Python dictionary.
        """
        out = super().to_dict()
        out.update({
            'sp': dict(self._sp), 'pt': dict(self._pt)
        })
        return out


    def from_dict(self, data: dict):
        """
        Load instance from Python dictionary.
        This will OVERWRITE all existing triples and all existing quads!
        """
        super().from_dict(data)
        self._sp.update(data['sp'])
        self._pt.update(data['pt'])


    def add_triple(self, subject: str, predicate: str, thing: str):
        """
        Create a (Subject -> Predicate -> Thing) relation.
        Examples:
        * RO -> official_name -> Romania
        * RO -> capital -> Bucharest
        * RO -> area_size -> 238391
        """
        # print(f'T :: {subject} -> {predicate} -> {thing}')
        s_key = self.add_node(subject)
        p_key = self.add_node(predicate)
        t_key = self.add_node(thing)
        self.add_edge(s_key, p_key)
        self.add_edge(p_key, t_key)
        # Add subject + predicate -> things
        sp_key = hash(s_key, p_key)
        sp_set = self._sp.get(sp_key, set())
        sp_set.add(t_key)
        self._sp[sp_key] = sp_set
        # Add predicate + thing -> subjects
        pt_key = hash(p_key, t_key)
        pt_set = self._pt.get(pt_key, set())
        pt_set.add(s_key)
        self._pt[pt_key] = pt_set


    def query_subject(self, predicate: str, match='', where=''):
        """
        Find "subjects" that match, connected to a specific predicate.
        Returns a generator.

        Examples:
            g.add_triple('mom', 'loves', 'dad')
            g.add_triple('dad', 'loves', 'mom')
            g.add_triple('mom', 'loves', 'girl')
            g.add_triple('dad', 'loves', 'boy')
            g.query_subject('loves')) # Who is loving someone
            # ['dad', 'mom']
        """
        p_key = hash(predicate)
        if not match:
            # Just return all subjects
            for node in self.iter_prev_nodes(p_key):
                yield self.get_node_id(node)
        else:
            # Match some subjects
            matches = create_matcher(match, where)
            for node in self.iter_prev_nodes(p_key):
                t = self.get_node_id(node)
                if matches(t):
                    yield t


    def query_thing(self, predicate: str, match='', where=''):
        """
        Find "things" that match, connected to a specific predicate.
        Returns a generator.

        Examples:
            g.add_triple('mom', 'loves', 'dad')
            g.add_triple('dad', 'loves', 'mom')
            g.add_triple('mom', 'loves', 'girl')
            g.add_triple('dad', 'loves', 'boy')
            g.query_thing('loves')) # Who is loved by someone
            # ['boy', 'dad', 'girl', 'mom']
        """
        p_key = hash(predicate)
        if not match:
            # Just return all things
            for node in self.iter_next_nodes(p_key):
                yield self.get_node_id(node)
        else:
            # Match some things
            matches = create_matcher(match, where)
            for node in self.iter_next_nodes(p_key):
                t = self.get_node_id(node)
                if matches(t):
                    yield t


    def query_sp_t(self, subject: str, predicate: str):
        """
        Find all "things" that match with the specified subject and predicate.
        This performs exact matches.

        Examples:
            g.query_pt_s('UID123', 'continent')
            g.query_pt_s('UID456', 'currency')
        """
        sp_key = hash(hash(subject), hash(predicate))
        for n in self._sp.get(sp_key, set()):
            yield self.get_node_id(n)


    def query_pt_s(self, predicate: str, thing: str):
        """
        Find all "subjects" that match with the specified predicate and thing.
        This performs exact matches.

        Examples:
            g.query_pt_s('continent', 'Europe')
            g.query_pt_s('currency', 'Euro')
        """
        pt_key = hash(hash(predicate), hash(thing))
        for n in self._pt.get(pt_key, set()):
            yield self.get_node_id(n)


    def query_triple(self, subject: str, predicate: str, thing: str):
        """
        Query for "subject", or "thing".
        The predicate must be specified.
        This performs exact matches.
        """
        # Must specify something useful for the query
        if (subject, predicate, thing) == ('?', '?', '?'):
            return False
        # Predicates cannot be queried
        if predicate == '?':
            return False

        # S+P=T query
        if subject != '?' and thing == '?':
            return self.query_sp_t(subject, predicate)

        # P+T=S query
        if thing != '?' and subject == '?':
            return self.query_pt_s(predicate, thing)

        # ELSE ???

        # s_key = hash(subject)
        # p_key = hash(predicate)
        # t_key = hash(thing)

        # for (sk0y, pk0y, tk0y) in self._triples.values():
        #     if predicate != '?' and p_key != pk0y:
        #         continue
        #     if subject != '?' and s_key != sk0y:
        #         continue
        #     if thing != '?' and t_key != tk0y:
        #         continue
        #     yield (
        #         self.get_node_id(sk0y), self.get_node_id(pk0y), self.get_node_id(tk0y)
        #     )


# Eof()
