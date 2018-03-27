from __future__ import absolute_import, print_function, unicode_literals

import pytest

from pysyncgateway.data_dict import DataDict
from pysyncgateway.exceptions import InvalidDataKey


def test():
    dd = DataDict()

    dd['stuff'] = 1

    assert dd == {'stuff': 1}


def test_blocked():
    dd = DataDict()

    with pytest.raises(InvalidDataKey):
        dd['_id'] = '1-aaaabbbcccdddeeeffff'

    assert dd == {}
