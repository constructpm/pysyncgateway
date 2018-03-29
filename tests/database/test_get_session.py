from __future__ import absolute_import, print_function, unicode_literals

from pysyncgateway import Session


def test(database):
    result = database.get_session()

    assert isinstance(result, Session)
    assert result.database == database
