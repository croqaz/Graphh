
try:
    import lmdb
except ModuleNotFoundError:
    print('LevelDB store requires PyPi.python.org/pypi/lmdb')
    exit(1)


class LmdbStore:

    __slots__ = ('db', 'table')

    def __init__(self, name, table=b''):
        self.db = lmdb.open(name + '.lmdb', max_dbs=9, map_size=8e12)
        self.table = None
        if table:
            self.table = self.db.open_db(table)

    def close(self):
        self.db.close()

    def __getitem__(self, key):
        with self.db.begin(db=self.table) as txn:
            return txn.get(key)

    def get(self, key, replacement=None):
        with self.db.begin(db=self.table) as txn:
            return txn.get(key, replacement)

    def put(self, key, data, overwrite=False):
        with self.db.begin(write=True, db=self.table) as txn:
            txn.put(key, data, dupdata=False, overwrite=overwrite)

    def delete(self, key):
        with self.db.begin(write=True, db=self.table) as txn:
            txn.delete(key)

    def __contains__(self, key):
        """
        Test whether a key is in the store
        """
        with self.db.begin(db=self.table) as txn:
            return bool(txn.get(key))

    def __iter__(self):
        """
        Iterates over all key -> values
        """
        with self.db.begin(db=self.table) as txn:
            for key in txn.cursor().iternext(keys=True, values=False):
                yield key

    def __len__(self):
        """
        Returns the number of nodes in the graph
        """
        with self.db.begin(db=self.table) as txn:
            return txn.stat()['entries']
