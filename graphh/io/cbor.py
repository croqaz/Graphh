"""
Import and export Graph to CBOR.
"""

import time
import cbor2

def export_cbor(graph, file_name='graphh.cbor'):
    t1 = time.time()
    with open(file_name, 'wb') as fd:
        cbor2.dump(graph.to_dict(), fd)
    t2 = time.time()
    print('Exported CBOR in `{:.4f}` seconds.'.format(t2 - t1))

def import_cbor(graph, file_name):
    t1 = time.time()
    with open(file_name, 'rb') as fd:
        data = cbor2.load(fd)
        graph.from_dict(data)
    t2 = time.time()
    print('Imported CBOR in `{:.4f}` seconds.'.format(t2 - t1))
    return graph
