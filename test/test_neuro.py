
import os, sys
import unittest
sys.path.insert(1, os.getcwd())
from json import load
from graphh import *

words = load(open('test/data/yes_no.json'))


class TestLocal(unittest.TestCase):

    def test_triple(self):

        g = Neuro()

        for word, means in words.items():
            # subject -> predicate -> thing
            g.add_triple(word, b'means', means)

        # print(f'\nAdded {len(words):,} words.')

        self.assertEqual(
            len(g.query_subject('means')), len(words))
        self.assertEqual(
            set(g.query_thing('means')), {'yes', 'no'})


    def test_family(self):

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
        self.assertListEqual(
            sorted(g.query_subject('needs')), ['boy', 'girl', 'lazy cat'])
        # Who is needed
        self.assertListEqual(
            sorted(g.query_thing('needs')), ['dad', 'mom'])

        # Who loves someone
        self.assertListEqual(
            sorted(g.query_subject('loves')), ['dad', 'mom'])
        # Who is loved by someone
        self.assertListEqual(
            sorted(g.query_thing('loves')), ['boy', 'dad', 'girl', 'lazy cat', 'mom'])

        # Relations between mom & dad
        self.assertListEqual(
            g.query_triple('mom', '?', 'dad'), [('mom', 'loves', 'dad')])
        self.assertListEqual(
            g.query_triple('dad', '?', 'mom'), [('dad', 'loves', 'mom')])

        # Who loves mom
        self.assertListEqual(
            g.query_triple('?', 'loves', 'mom'), [('dad', 'loves', 'mom')])
        # Who needs mom
        self.assertListEqual(
            g.query_triple('?', 'needs', 'mom'),
            [('girl', 'needs', 'mom'), ('boy', 'needs', 'mom'), ('lazy cat', 'needs', 'mom')]
        )
