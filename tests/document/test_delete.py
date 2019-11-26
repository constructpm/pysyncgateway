import pytest
from pysyncgateway import Database, Document
from pysyncgateway.exceptions import DoesNotExist, RevisionMismatch


@pytest.fixture
def document(database):
    """
    Returns:
        Document: written to sync gateway.
    """
    document = Document(database, 'a_document')
    document.data = {'testing': True}
    document.create_update()
    return document


@pytest.fixture
def other_document(database, document):
    """
    Returns:
        Document: Copy of 'document' fixture, but with an additional revision.
    """
    other_document = Document(database, document.doc_id)
    other_document.retrieve()
    other_document.data['more'] = 'stuff'
    other_document.create_update()
    return other_document


def test_other_document(other_document, document):
    """
    Two instances of the same Document have different revisions: document.rev
    is older (smaller) than other_document.rev.
    """
    result = other_document

    assert result == document
    assert result.rev > document.rev


# --- TESTS ---


def test_happy(document, database):
    result = document.delete()

    assert result is True
    assert document not in database.all_docs()


# --- FAILURES ---


def test_missing_database(admin_client):
    database = Database(admin_client, 'missingdb')
    document = database.get_document('documentid')
    document.set_rev('1-1234')

    with pytest.raises(DoesNotExist):
        document.delete()


def test_missing(empty_document):
    with pytest.raises(DoesNotExist):
        empty_document.delete()


def test_already_deleted(document, database):
    Document(database, 'a_document').delete()

    with pytest.raises(RevisionMismatch):
        document.delete()


def test_bad_revision(document, other_document):
    with pytest.raises(RevisionMismatch):
        document.delete()
