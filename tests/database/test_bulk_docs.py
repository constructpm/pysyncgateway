import pytest
from pysyncgateway.exceptions import DoesNotExist


@pytest.fixture
def doc_123(database):
    d_123 = database.get_document("foo")
    d_123.data = {
        "type": "user",
        "updated_at": "2016-06-24T17:37:49.715Z",
        "status": "online",
    }
    d_123.set_rev("1-123")
    return d_123


@pytest.fixture
def doc_456(database):
    d_456 = database.get_document("foo")
    d_456.data = {
        "type": "user",
        "updated_at": "2016-06-26T17:37:49.715Z",
        "status": "offline",
    }
    d_456.set_rev("1-456")
    return d_456


@pytest.fixture
def doc_789(database):
    d_789 = database.get_document("foo")
    d_789.data = {
        "type": "user",
        "updated_at": "2016-06-25T17:37:49.715Z",
        "status": "offline",
    }
    d_789.set_rev("1-789")
    return d_789


# --- TESTS ---


def test_no_docs(database):
    database.create()

    result = database.bulk_docs([])

    assert result is True
    assert database.all_docs() == []


def test_new_docs(database):
    """
    Example taken from https://docs.couchbase.com/sync-gateway/1.5/resolving-conflicts.html
    """
    database.create()
    doc = database.get_document("foo")
    doc.data = {
        "type": "user",
        "updated_at": "2016-06-24T17:37:49.715Z",
        "status": "online",
    }
    doc.set_rev("1-123")

    result = database.bulk_docs([doc])

    assert result is True
    assert database.all_docs() == [doc]


def test_new_docs_conflicted(database, doc_123, doc_456, doc_789):
    """
    Example taken from https://docs.couchbase.com/sync-gateway/1.5/resolving-conflicts.html
    """
    database.create()

    result = database.bulk_docs([doc_123, doc_456, doc_789])

    assert result is True
    assert database.all_docs() == [doc_123]
    assert doc_123.get_open_revisions() == 3
    assert doc_123.delete()
    assert doc_123.retrieve()
    assert doc_123.rev == "1-456"


def test_delete_conflicts(database, doc_123, doc_456, doc_789):
    """
    After deleting other revisions, they still come through with
    get_open_revisions(), but deleting the last revision clears out the
    document.
    """
    database.create()
    database.bulk_docs([doc_123, doc_456, doc_789])
    doc_123.to_delete = True
    doc_456.to_delete = True

    result = database.bulk_docs([doc_123, doc_456], new_edits=None)

    assert result is True
    assert database.all_docs() == [doc_123]
    assert doc_123.get_open_revisions() == 1
    assert doc_123.open_revisions == []
    assert doc_123.rev == "1-789"
    assert doc_123.delete()
    with pytest.raises(DoesNotExist):
        doc_123.retrieve()


# --- FAILURES ---


def test_missing_database(database):
    with pytest.raises(DoesNotExist):
        database.bulk_docs([])
