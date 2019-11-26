from pysyncgateway import User


def test(database):
    result = User(database, 'test-user')

    assert result.database == database
    assert result.name == 'test-user'
    assert result.password is None
    assert result.retrieved is False
    assert result.url.startswith(database.url)
    assert result.url.endswith('/_user/test-user')
