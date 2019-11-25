

import pytest

from pysyncgateway.data_dict import DataDict


def test_empty():
    """
    DataDict.from_dict creates an empty instance with an empty dict
    """
    result = DataDict.from_dict({})

    assert result == {}
    assert isinstance(result, DataDict)


def test_good_keys():
    """
    DataDict.from_dict loads all keys not in the filter list
    """
    input_data = {
        'results': {
            'temp',
            2,
            'num',
            3,
        },
    }

    result = DataDict.from_dict(input_data)

    assert result == input_data


def test_keys_filtered():
    """
    DataDict.from_dict removes keys that are in filtered keys list
    """
    input_data = {
        '_id': 1,
        '_rev': 2,
        'channels': ['tests'],
    }

    result = DataDict.from_dict(input_data)

    assert result == {}


# --- FAILURES ---


def test_non_dict():
    with pytest.raises(ValueError):
        DataDict.from_dict(1)
