

import pytest


def test(empty_document):
    result = empty_document.set_rev('1-hnfwinfwehfs')

    assert result is None
    assert empty_document.rev == '1-hnfwinfwehfs'


def test_empty(empty_document):
    with pytest.raises(ValueError):
        empty_document.set_rev('')
