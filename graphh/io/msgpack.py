"""
Import and export Graph to MsgPack.
"""

import time
import msgpack

def export_msgpack(graph, file_name='graphh.pack'):
    t1 = time.time()
    with open(file_name, 'wb') as fd:
        fd.write(msgpack.packb(graph.to_dict(), use_bin_type=True))
    t2 = time.time()
    print('Exported MsgPack in `{:.4f}` seconds.'.format(t2 - t1))

def import_msgpack(graph, file_name):
    t1 = time.time()
    with open(file_name, 'rb') as fd:
        data = msgpack.unpackb(fd.read())
        # Fix binary keys
        data['n'] = data[b'n']
        data['e'] = data[b'e']
        del data[b'n'], data[b'e']
        graph.from_dict(data)
    t2 = time.time()
    print('Imported MsgPack in `{:.4f}` seconds.'.format(t2 - t1))
    return graph
