from __future__ import absolute_import, print_function, unicode_literals

from pysyncgateway import Query


def test(database):
    result = database.get_query('test')

    assert result == Query(database, 'test')
