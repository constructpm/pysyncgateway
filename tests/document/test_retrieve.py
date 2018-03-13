from __future__ import absolute_import, print_function, unicode_literals

import pytest

from pysyncgateway.exceptions import DoesNotExist


@pytest.fixture
def recipe_document(database):
    """
    Returns:
        Document: Contains a recipe and written to sync gateway.
    """
    data = {
        'ingredients': ['chicken', 'butter'],
        'recipe': 'Mix the chicken and the butter. Voila!',
    }
    document = database.get_document('butter_chicken')
    document.data = data
    document.create_update()
    return document


def test_recipe_document(recipe_document, database):
    result = recipe_document

    assert result in database.all_docs()


@pytest.fixture
def permissions_document(database):
    """
    Returns:
        Document: Written to SG with empty data, just channels set.
    """
    document = database.get_document('permission-list')
    document.set_channels('acc.1234', 'acc.7882')
    document.create_update()
    return document


def test_permissions_document(permissions_document, database):
    result = permissions_document

    assert result in database.all_docs()


# --- TESTS ---


def test(recipe_document, database):
    reload_document = database.get_document('butter_chicken')

    result = reload_document.retrieve()

    assert result is True
    for key in reload_document.data.keys():
        assert isinstance(key, unicode)
    assert sorted(list(reload_document.data)) == ['ingredients', 'recipe']
    assert reload_document.data['ingredients'] == ['chicken', 'butter']
    assert reload_document.data['recipe'] == 'Mix the chicken and the butter. Voila!'
    assert isinstance(reload_document.data['recipe'], unicode)
    assert reload_document.rev == recipe_document.rev
    assert reload_document.channels == ()


def test_channels(permissions_document, database):
    """
    Document with no data can be retrieved, channels are updated
    """
    reload_document = database.get_document('permission-list')

    result = reload_document.retrieve()

    assert result is True
    assert reload_document.data == {}
    assert reload_document.rev == permissions_document.rev
    assert reload_document.channels == ('acc.1234', 'acc.7882')


# --- FAILURES ---


def test_missing(empty_document):
    with pytest.raises(DoesNotExist):
        empty_document.retrieve()
