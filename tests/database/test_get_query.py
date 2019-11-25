

from pysyncgateway import Query


def test(database):
    result = database.get_query('test')

    assert result == Query(database, 'test')
