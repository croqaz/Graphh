
import os, sys # noqa: E401
sys.path.insert(1, os.getcwd())

from json import load
from graphh import Neuro


def test_triple():
    """
    Yes / No words
    """
    words = load(open('tests/data/yes_no.json'))

    g = Neuro()

    for word, means in words.items():
        # subject -> predicate -> thing
        g.add_triple(word, b'means', means)

    assert set(g.query_subject('means')) == set(words)
    assert set(g.query_thing('means')) == {'yes', 'no'}


def test_family():

    g = Neuro()

    g.add_node('mom')
    g.add_node('dad')
    g.add_node('girl')
    g.add_node('boy')
    g.add_node('lazy cat')

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

    # Who needs mom
    assert sorted(g.query_pt_s('needs', 'mom')) ==  ['boy', 'girl', 'lazy cat']
    # Who needs dad
    assert sorted(g.query_pt_s('needs', 'dad')) == ['boy', 'girl']

    # Girl needs what == Boy needs what
    assert sorted(g.query_sp_t('girl', 'needs')) == sorted(g.query_sp_t('boy', 'needs'))

    assert sorted(g.query_triple('?', 'loves', 'mom')) == ['dad']
    assert sorted(g.query_triple('?', 'needs', 'mom')) == ['boy', 'girl', 'lazy cat']

    assert sorted(g.query_triple('mom', 'loves', '?')) == ['dad', 'girl', 'lazy cat']
    assert sorted(g.query_triple('dad', 'loves', '?')) == ['boy', 'mom']
