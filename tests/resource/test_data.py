from __future__ import absolute_import, print_function, unicode_literals

import pytest

from pysyncgateway import Database
from pysyncgateway.resource import Resource


@pytest.fixture
def resource(admin_client):
    """
    Returns:
        Resource: Containing basic data.
    """
    database = Database(admin_client, 'db')
    resource = Resource(database)
    resource.data = {
        'result': {
            'new': True,
        },
    }
    return resource


def test_getter(resource):
    """
    resource.data provides _data, but strips channels and _rev
    """
    result = resource.data

    assert result == {
        'result': {
            'new': True,
        },
    }


def test_happy(resource):
    """
    resource sets its data, stored in `_data`
    """
    data = {
        '__INFO__': '__STUFF__',
        'recipe': ['channels', 'ridges', 'hills', 'valleys'],
    }

    resource.data = data

    assert resource._data == data


def test_clean_protected(resource):
    mixed_data = {
        '__INFO__': '__STUFF__',
        'channels': ['acc.1234'],
        '_rev': '1-asdfvanndkeifyufyannba',
        '_id': 1234,
    }

    resource.data = mixed_data

    assert resource.data == {'__INFO__': '__STUFF__'}


def test_end_to_end(resource):
    """
    resource.data can do `self.data = self.data`

    This is a good test because it ensures that cleansing of the data on
    getting matches the requirements of the clean data enforced when
    setting.
    """
    resource.data = resource.data

    assert resource.data == {
        'result': {
            'new': True,
        },
    }


def test_set_key(resource):
    """
    resource.data can be set with a key
    """
    resource.data['info'] = {
        'person': {
            'name': 'Fry',
            'species': 'human',
        },
    }

    assert resource.data == {
        'info': {
            'person': {
                'name': 'Fry',
                'species': 'human',
            },
        },
        'result': {
            'new': True,
        },
    }


# --- FAILURES ---


def test_data_not_dict(resource):
    """
    resource.data raises when a non-`dict` is passed
    """
    with pytest.raises(ValueError):
        resource.data = '__STUFF__'
