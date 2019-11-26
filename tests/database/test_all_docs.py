import pytest
from pysyncgateway.exceptions import DoesNotExist

# See also: Tests on Document.create_update: where `all_docs` is used to assert
# that new docs appear in the output.


def test_happy_empty(database):
    database.create()

    result = database.all_docs()

    assert result == []


def test_missing_database(database):
    with pytest.raises(DoesNotExist):
        database.all_docs()
