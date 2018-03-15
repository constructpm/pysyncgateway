from __future__ import absolute_import, print_function, unicode_literals

import pytest

from pysyncgateway.exceptions import InvalidChannelName


def test_admin_channels_happy(user):
    result = user.set_admin_channels('__CHANNEL1__', '__CHANNEL2__')

    assert result is None
    assert user.admin_channels == ('__CHANNEL1__', '__CHANNEL2__')


def test_none(user):
    user.set_admin_channels('__CHANNEL1__', '__CHANNEL2__')

    result = user.set_admin_channels()

    assert result is None
    assert user.admin_channels == ()


# --- FAILURES ---


def test_admin_channels_bad(user):
    with pytest.raises(InvalidChannelName):
        user.set_admin_channels('good@1', 'good@2', 'bad#1')
