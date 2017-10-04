
import os, sys
sys.path.insert(1, os.getcwd())

from json import load
from graphh import Neuro

words = load(open('test/data/yes_no.json'))


def test_triple():

    g = Neuro()

    for word, means in words.items():
        # subject -> predicate -> thing
        g.add_triple(word, b'means', means)

    assert set(g.query_subject('means')) == set(words)
    assert set(g.query_thing('means')) == {'yes', 'no'}


def test_family():

    g = Neuro()

    mom = g.add_node('mom')
    dad = g.add_node('dad')
    girl = g.add_node('girl')
    boy = g.add_node('boy')
    cat = g.add_node('lazy cat')

    # subject -> predicate -> thing
    g.add_triple('mom', 'loves', 'dad')
    g.add_triple('dad', 'loves', 'mom')
    g.add_triple('mom', 'loves', 'girl')
    g.add_triple('dad', 'loves', 'boy')
    g.add_triple('mom', 'loves', 'lazy cat')

    g.add_triple('girl', 'needs', 'mom')
    g.add_triple('girl', 'needs', 'dad')
    g.add_triple('boy', 'needs', 'mom')
    g.add_triple('boy', 'needs', 'dad')
    g.add_triple('lazy cat', 'needs', 'mom')

    # Who needs something
    assert sorted(g.query_subject('needs')) == ['boy', 'girl', 'lazy cat']
    # Who is needed
    assert sorted(g.query_thing('needs')) == ['dad', 'mom']

    # Who loves someone
    assert sorted(g.query_subject('loves')) == ['dad', 'mom']
    # Who is loved by someone
    assert sorted(g.query_thing('loves')) == ['boy', 'dad', 'girl', 'lazy cat', 'mom']

    # Relations between mom & dad
    assert g.query_triple('mom', '?', 'dad') == [('mom', 'loves', 'dad')]
    assert g.query_triple('dad', '?', 'mom') == [('dad', 'loves', 'mom')]

    # Who loves mom
    assert g.query_triple('?', 'loves', 'mom') == [('dad', 'loves', 'mom')]
    # Who needs mom
    assert g.query_triple('?', 'needs', 'mom') == \
        [('girl', 'needs', 'mom'), ('boy', 'needs', 'mom'), ('lazy cat', 'needs', 'mom')]
