import pytest

from pysyncgateway.exceptions import NotLoaded


def test_loaded(session):
    session.retrieve()

    result = session.get_channels()

    assert result == ['!', 'a', 'b', 'c']


def test_not_loaded(session):
    with pytest.raises(NotLoaded):
        session.get_name()


def test_not_provided(session):
    """
    Sync Gateway may change its response (this endpoint is not documented).
    """
    session.data['userCtx'] = {'other_stuff': True}

    with pytest.raises(KeyError):
        session.get_name()
