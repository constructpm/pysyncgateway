# encoding: utf-8
import pytest
from pysyncgateway import Document
from pysyncgateway.exceptions import RevisionMismatch


def test(database):
    """
    After doc creation, asserts that the document revision in the document
    instance matches the document revision provided by `all_docs`
    """
    document = Document(database, 'test.1234|create_update')
    data = {
        'likes': 'tests',
        'dislikes': 'errors',
    }
    document.data = data
    document.set_channels('testchannel')

    result = document.create_update()

    assert result == database.client.CREATED
    all_docs = database.all_docs()
    assert all_docs == [document]
    assert all_docs[0].doc_id == 'test.1234|create_update'
    assert all_docs[0].rev == document.rev


def test_happy_empty(empty_document, database):
    result = empty_document.create_update()

    assert result == database.client.CREATED
    assert database.all_docs() == [empty_document]


@pytest.mark.parametrize('doc_id', [
    'more money £',
    'space * everything',
    '$stuff!channel',
    'café culture',
])
def test_all_valid_doc_keys(doc_id, database):
    """
    Documents can be created with many different types of ID

    There are document ids which should work, but don't because URL encoding is
    not properly completed:
        'Questions? yeah man!',
        'hashes### like a boss',
    """
    document = Document(database, doc_id)

    result = document.create_update()

    assert result == database.client.CREATED
    assert document in database.all_docs()


# --- FAILURES ---


def test_recreate_existing_document(database):
    """
    Second request attempts to create a document that already exists.
    """
    doc_id = 'double.dribble'
    document = Document(database, doc_id)
    document.create_update()
    document = Document(database, doc_id)

    with pytest.raises(RevisionMismatch) as exc_info:
        document.create_update()

    assert exc_info.value.args == (document.url, '')


def test_update_bumped_document(database):
    doc_id = 'double.dribble'
    document = Document(database, doc_id)
    document.create_update()
    initial_rev = document.rev
    document.create_update()
    document = Document(database, doc_id)
    document.set_rev(initial_rev)

    with pytest.raises(RevisionMismatch) as exc_info:
        document.create_update()

    assert exc_info.value.args == (document.url, initial_rev)
