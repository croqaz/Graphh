
import os, sys
sys.path.insert(1, os.getcwd())

from json import load
from graphh import Neuro

COUNTRIES = load(open('test/data/countries.json'))


def iter_countries():
    for item in COUNTRIES:
        id = item['cca2']
        data = {
          b'common_name': item['name']['common'],
          b'official_name': item['name']['official'],
          b'capital': item['capital'],
          b'region': item['region'],
          b'sub_region': item['subregion'],
          b'cca2': item['cca2'],
          b'cca3': item['cca3'],
          b'ccn3': item['ccn3'],
          b'cioc': item['cioc'],
          b'area_size': item['area'],
        #   b'currencies': item['currency'],
        #   b'languages': item['languages'],
        #   b'borders': item['borders'],
        }
        yield id, data


def test_countries():
    """
    Countries and borders
    https://github.com/mledoze/countries
    """
    g = Neuro()

    for id, c in iter_countries():
        for predicate, thing in c.items():
            g.add_triple(id, predicate, thing)

    regions = sorted(n for n in g.query_thing('region') if n)
    # print('What are the regions ::', regions)
    assert regions == ['Africa', 'Americas', 'Asia', 'Europe', 'Oceania']

    subregs = set(n for n in g.query_thing('sub_region'))
    # print('What are the sub-regions ::', subregs)
    assert subregs == set(n['subregion'] for n in COUNTRIES)

    countries = sorted(g.query_thing('official_name'))
    # print('How many countries ::', len(countries))
    assert len(countries) == len(COUNTRIES)

    capitals = set(g.query_thing('capital'))
    # print('How many capitals ::', len(capitals))
    assert capitals == set(n['capital'] for n in COUNTRIES)

    info = {k: v for _, k, v in g.query_triple('RO', '?', '?')}
    # print('What info about Romania ::', info)
    assert info[b'common_name'] == 'Romania'
    assert info[b'capital'] == 'Bucharest'
