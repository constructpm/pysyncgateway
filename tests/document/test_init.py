

import pytest

from pysyncgateway import Document
from pysyncgateway.exceptions import InvalidDocumentID


def test(database):
    result = Document(database, '__DOC_ID__')

    assert result.channels == ()
    assert result.doc_id == '__DOC_ID__'
    assert result.open_revisions == []
    assert result.rev == ''
    assert result.to_delete is False
    assert result.url.endswith('__DOC_ID__')


# --- FAILURES ---


def test_bad_name_raises(database):
    with pytest.raises(InvalidDocumentID):
        Document(database, 'colon:nope')
