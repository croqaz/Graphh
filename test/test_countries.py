
import os, sys
sys.path.insert(1, os.getcwd())

from json import load
from graphh import FsConvention

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
          b'cca3': item['cca3'],
          b'ccn3': item['ccn3'],
          b'cioc': item['cioc'],
          b'area_size': item['area'],
          b'borders': item['borders'],
          b'currencies': item['currency'],
          b'languages': sorted(item['languages'].values())
        }
        if item.get('latlng'):
            data['latitude'] = item['latlng'][0]
            data['longitude'] = item['latlng'][1]
        yield id, data


def test_countries():
    """
    Countries and borders
    https://github.com/mledoze/countries
    """
    g = FsConvention('Geography')
    g.create_table('countries')

    for id, data in iter_countries():
        g.create_doc('countries', id, data)

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

    countries = set(g.query_thing('official_name', 'U', '<'))
    # print('R countries:', countries)
    assert countries == set(n['name']['official'] for n in COUNTRIES \
        if n['name']['official'][0] == 'U')

    countries = set(g.query_thing('official_name', 'a', '>'))
    # print('A countries:', countries)
    assert countries == set(n['name']['official'] for n in COUNTRIES \
        if n['name']['official'][-1] == 'a')

    info = g.get_doc('countries', 'RO')
    # print('What info about Romania ::', info)
    assert info[b'common_name'] == 'Romania'
    assert info[b'capital'] == 'Bucharest'
