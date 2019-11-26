import pytest
from pysyncgateway.exceptions import InvalidChannelName


def test_channels_happy(empty_document):
    result = empty_document.set_channels('__CHANNEL1__', '__CHANNEL2__')

    assert result is None
    assert empty_document.channels == ('__CHANNEL1__', '__CHANNEL2__')


# --- FAILURES ---


def test_channels_bad(empty_document):
    with pytest.raises(InvalidChannelName) as excinfo:
        empty_document.set_channels('good@1', 'good@2', 'bad#1')

    assert '#' in str(excinfo.value)
