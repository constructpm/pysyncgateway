from __future__ import absolute_import, print_function, unicode_literals

import pytest

from pysyncgateway.exceptions import NotLoaded


def test_loaded(session):
    session.retrieve()

    result = session.get_name()

    assert result == '__USERNAME__'


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
