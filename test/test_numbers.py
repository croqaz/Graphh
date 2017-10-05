
import os, sys
sys.path.insert(1, os.getcwd())
from graphh import Neuro

MIN_NR = 10_000
MAX_NR = 30_000


is_odd = lambda x: x % 2

def is_prime(a):
    return not (a < 2 or any(a % x == 0 for x in range(2, int(a**0.5) + 1)))

def is_palindrome(a):
    return str(a) == str(a)[::-1]


def test_numbers():
    """
    Stress test
    """
    g = Neuro()

    for i in range(MIN_NR, MAX_NR):
        nr = str(i).encode()
        g.add_triple(nr, b'=', b'number')
        if is_odd(i):
            g.add_triple(nr, b'o', b'odd')
        else:
            g.add_triple(nr, b'o', b'even')
        if is_prime(i):
            g.add_triple(nr, b'p', b'prime')
        if is_palindrome(i):
            g.add_triple(nr, b'p', b'palindrome')

    nrs = set(g.query_subject('='))
    assert len(nrs) == MAX_NR - MIN_NR
    del nrs

    assert set(g.query_thing('o')) == {b'odd', b'even'}
    assert set(g.query_thing('p')) == {b'prime', b'palindrome'}

    # p = set(g.query_triple('?', 'p', 'palindrome'))
    # print('Palindromes ::', p)
