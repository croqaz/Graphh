"""
Import and export Graph to CSV.
"""

import time
from binascii import hexlify, unhexlify


def export_csv(graph, nodes_file='g_nodes.csv', edges_file='g_edges.csv'):
    t1 = time.time()
    with open(nodes_file, 'w') as nfile:
        nfile.write('id,label\n')
        for k, val in graph.iter_nodes():
            hex = hexlify(k).decode('utf')
            nfile.write(f'{hex},{val}\n')

    with open(edges_file, 'w') as efile:
        efile.write('Source,Target\n')
        for _, (head, tail) in graph.iter_edges():
            head = hexlify(head).decode('utf')
            tail = hexlify(tail).decode('utf')
            efile.write(f'{head},{tail}\n')
    t2 = time.time()
    print('Exported CSV in `{:.4f}` seconds.'.format(t2 - t1))


def import_csv(graph, nodes_file='g_nodes.csv', edges_file='g_edges.csv'):
    t1 = time.time()
    with open(nodes_file, 'r') as nfile:
        nfile.readline() # Ignore header
        for line in nfile.readlines():
            key, val = line[:-1].split(',')
            graph.add_node(val) == unhexlify(key), 'The CSV nodes file is corrupted'

    with open(edges_file, 'r') as efile:
        efile.readline() # Ignore header
        for line in efile.readlines():
            head, tail = line[:-1].split(',')
            graph.add_edge(unhexlify(head), unhexlify(tail))
    t2 = time.time()
    print('Imported CSV in `{:.4f}` seconds.'.format(t2 - t1))
    return graph
