from pysyncgateway import Session


def test(database):
    result = database.get_session()

    assert isinstance(result, Session)
    assert result.database == database
