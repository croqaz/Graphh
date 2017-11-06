
import os, sys # noqa: E401
sys.path.insert(1, os.getcwd())

from json import load
from graphh import Neuro

data = load(open('tests/data/les_miserables.json'))


def test_miserables():
    """
    Les Miserables relation graph
    https://bl.ocks.org/mbostock/4062045
    """

    g = Neuro()

    for node in data['nodes']:
        g.add_node(node['id'])

    # Before triples
    assert g.number_of_nodes() == len(data['nodes'])

    # Counting the relations
    relations = set()

    for link in data['links']:
        g.add_triple(link['source'], 'knows', link['target'])
        # Counting the triples
        relations.add(f'{link["source"]}knows')
        relations.add(f'knows{link["target"]}')

    # After triples it should be just 1 more node
    assert g.number_of_nodes() == len(data['nodes']) + 1
    assert g.number_of_edges() == len(relations)

    # Who is known by someone
    is_known = set(l['target'] for l in data['links'])
    assert set(g.query_thing('knows')) == is_known

    # Who knows someone
    knows_who = set(l['source'] for l in data['links'])
    assert set(g.query_subject('knows')) == knows_who

    # Want I need to find ::
    # Who knows the most people (top 3)
    # Who is known by the most people (top 3)
