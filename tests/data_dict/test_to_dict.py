from __future__ import absolute_import, print_function, unicode_literals

from pysyncgateway.data_dict import DataDict


def test_empty():
    """
    Resulting dict is completely different to the wrapped DataDict. A protected
    key can be assigned in the returned value.
    """
    dd = DataDict()

    result = dd.to_dict()

    assert result == {}
    assert isinstance(result, dict)
    assert id(result) != id(dd)
    result['_rev'] = 3
