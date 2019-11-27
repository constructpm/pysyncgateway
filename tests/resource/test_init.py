# encoding: utf-8
import pytest

from pysyncgateway import Database
from pysyncgateway.resource import Resource


def test(admin_client):
    database = Database(admin_client, 'db')

    result = Resource(database)

    assert result.database == database
    assert result._data.to_dict() == {}
    assert result.url == ''


class MockDatabase(object):
    pass


def test_happy_unicode():
    database = MockDatabase()
    database.url = 'http://localhost/caféculture'

    result = Resource(database)

    assert result.database == database


# --- FAILURES ---


def test_needs_database():
    with pytest.raises(TypeError):
        Resource()


def test_valid_database_required():
    with pytest.raises(ValueError) as excinfo:
        Resource(1)

    assert 'Resource' in excinfo.value.args[0]
