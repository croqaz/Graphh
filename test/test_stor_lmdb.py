
import os, sys
import shutil
import unittest
sys.path.insert(1, os.getcwd())
from graphh.stor import lmdb

DB = 'a'

class TestDb(unittest.TestCase):

    def setUp(self):
        shutil.rmtree(DB + '.lmdb', True)

    def tearDown(self):
        shutil.rmtree(DB + '.lmdb', True)


    def test_empty_db(self):
        d = lmdb.LmdbStore(DB)

        self.assertEqual(len(d), 0)

        self.assertIsNone(d.get(b'x'))


    def test_put_get(self):
        d = lmdb.LmdbStore(DB)

        d.put(b'a', b'a')

        self.assertEqual(len(d), 1)

        self.assertEqual(d.get(b'a'), b'a')

        d.put(b'x', b'xxx')

        self.assertEqual(len(d), 2)

        self.assertEqual(d.get(b'x'), b'xxx')


    def test_delete(self):
        d = lmdb.LmdbStore(DB)

        d.put(b'a', b'123')
        self.assertEqual(len(d), 1)

        d.delete(b'a')
        self.assertEqual(len(d), 0)

        self.assertIsNone(d.get(b'a'))
