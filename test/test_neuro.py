
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
