from functions import merge_all
from functions import filter_labels

def test_merge_all():
    _in = {
        'a.x': 1,
        'a.y': 2,
        'a.c.x': 3,
        'a.d.x': 4,
        'a.d.y': 5,
        'a.z': 6,
        'a.c.e.y': 7,
        'a.c.e.z': 8
    }
    _out = {
        'a': {'x': 1, 'y': 2, 'z': 6},
        'a.c': {'x': 3, 'y': 2, 'z': 6},
        'a.d': {'x': 4, 'y': 5, 'z': 6},
        'a.c.e': {'y': 7, 'z': 8, 'x': 3}
    }
    assert merge_all(_in) == _out

def test_filter_labels():
    _in = {
        'cloudflare-dns.moo': 1,
        'a.y': 2,
    }
    _out = {
        'cloudflare-dns.moo': 1,
    }
    assert filter_labels(_in) == _out