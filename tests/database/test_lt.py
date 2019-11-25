

import pytest

from pysyncgateway import AdminClient, Database


def test_equal():
    admin_client = AdminClient('__URL__')
    database_a = Database(admin_client, 'test')
    database_b = Database(admin_client, 'test')

    result = database_a == database_b

    assert result is True


def test_ne():
    """
    Databases with different client settings are not equal
    """
    a_admin_client = AdminClient('__URL_A__')
    a_database = Database(a_admin_client, 'db')
    b_admin_client = AdminClient('__URL_B__')
    b_database = Database(b_admin_client, 'db')

    result = a_database == b_database

    assert result is False


def test_ne_db():
    """
    Databases with different names are not equal
    """
    admin_client = AdminClient('__URL__')
    a_database = Database(admin_client, 'first')
    b_database = Database(admin_client, 'second')

    result = a_database == b_database

    assert result is False


def test_other_type():
    admin_client = AdminClient('__URL__')
    database = Database(admin_client, 'test')

    with pytest.raises(ValueError) as excinfo:
        database < 1

    assert 'int' in str(excinfo.value)
