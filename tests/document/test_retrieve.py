import pytest
from pysyncgateway.exceptions import DoesNotExist


def test(recipe_document, database):
    reload_document = database.get_document('butter_chicken')

    result = reload_document.retrieve()

    assert result is True
    for key in list(reload_document.data.keys()):
        assert isinstance(key, str)
    assert sorted(list(reload_document.data)) == ['ingredients', 'recipe']
    assert reload_document.data['ingredients'] == ['chicken', 'butter']
    assert reload_document.data['recipe'] == 'Mix the chicken and the butter. Voila!'
    assert isinstance(reload_document.data['recipe'], str)
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
