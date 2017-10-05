
from .neuro import Neuro
from .util import hash


class FsConvention(Neuro):
    """
    File-system-like convention graph.
    """

    def __init__(self, app: str):
        super().__init__()
        self._app = app
        self._chains = {}
        # Save app paths
        self._app_root_path = f'/{self._app}/'
        self._app_tables_path = f'/{self._app}/tables/'
        self._app_meta_path = f'/{self._app}/meta/'
        # Create root nodes
        self._app_root_id = self.add_node(self._app_root_path)
        self._app_tables_id = self.add_node(self._app_tables_path)
        self._app_meta_id = self.add_node(self._app_meta_path)
        # Create root edges
        self.add_edge(self._app_root_id, self._app_tables_id)
        self.add_edge(self._app_root_id, self._app_meta_id)


    def list_tables(self):
        tables = []
        for oe in self.out_edges(self._app_tables_id):
            n = self.get_node_id(self.tail(oe))
            tables.append(n)
        return tables

    def list_docs(self, table: str):
        doc_path = hash(f'{self._app_tables_path}{table}/docs/')
        docs = []
        for oe in self.out_edges(doc_path):
            n = self.get_node_id(self.tail(oe))
            docs.append(n)
        return docs


    def create_table(self, table: str):
        """
        Create a new table in the app.
        The name must be unique for the app, to avoid collision.
        """
        tb_path = f'{self._app_tables_path}{table}/'
        tb_key = self.add_node(tb_path, safe=False)
        if not tb_key:
            # print(f'Table "{tb_path}" exists already !')
            return False
        # print(f'Creating table "{tb_path}"')
        # Make edge between Tables and the New Table
        self.add_edge(self._app_tables_id, tb_key)
        tb_doc = self.add_node(f'{tb_path}docs/')
        # Make edge between New Tables and the New Table Docs
        self.add_edge(tb_key, tb_doc)
        tb_meta = self.add_node(f'{tb_path}meta/')
        # Make edge between New Tables and the New Table Meta
        self.add_edge(tb_key, tb_meta)


    def create_doc(self, table: str, uid: str, data: dict):
        """
        Insert a new document in a table.
        The UID must be unique in the table, to avoid collision.
        The data must be a dictionary.
        """
        doc_path = f'{self._app_tables_path}{table}/docs/'
        doc_uid = f'{doc_path}{uid}/'
        node_id = self.add_node(doc_uid, safe=False)
        if not node_id:
            # print(f'Document "{table}/{uid}" exists already !')
            return False
        # print(f'Creating doc "{doc_uid}"')
        tb_doc = hash(doc_path)
        self.add_edge(tb_doc, node_id)

        prop_keys = []
        for predicate, thing in data.items():
            if isinstance(thing, (tuple, list)):
                for t in thing:
                    k = self.add_triple(doc_uid, predicate, t)
                    prop_keys.append(k)
            else:
                k = self.add_triple(doc_uid, predicate, thing)
                prop_keys.append(k)

        key = hash(*prop_keys)
        self._chains[key] = tuple(prop_keys)
        return key


    def get_doc(self, table: str, uid: str):
        """
        Return a specific document UID from a table.
        """
        doc_uid = f'{self._app_tables_path}{table}/docs/{uid}/'
        doc = {}
        for subject, predicate, thing in self.query_triple(doc_uid, '?', '?'):
            doc[predicate] = thing
        return doc
