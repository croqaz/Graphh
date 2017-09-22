
try:
    import plyvel
except ModuleNotFoundError:
    print('LevelDB store requires PyPi.python.org/pypi/plyvel')
    exit(1)


class LevelStore:

    __slots__ = 'db'

    def __init__(self, name):
        self.db = plyvel.DB(name + '.lvl', create_if_missing=True)

    def close(self):
        self.db.close()

    # def __getitem__(self, key):
    #     return self.db.get(key)

    def get(self, key, replacement=None):
        return self.db.get(key, replacement)

    # def __setitem__(self, key, data):
    #     self.db.put(key, data)

    def put(self, key, data, overwrite=False):
        if not overwrite and self.db.get(key):
            return
        self.db.put(key, data)

    def delete(self, key):
        self.db.delete(key)

    def __contains__(self, key):
        """
        Test whether a key is in the store
        """
        return bool(self.db.get(key))

    def __iter__(self):
        """
        Iterates over all key -> values
        """
        return iter(self.db)

    def __len__(self):
        """
        Returns the number of nodes in the graph
        """
        return len(set(self.db))
