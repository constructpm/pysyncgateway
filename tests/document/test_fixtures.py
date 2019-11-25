


def test_database(database, admin_client):
    result = database

    assert result in admin_client.all_databases()


def test_empty_document(empty_document):
    result = empty_document

    assert result.data == {}
    assert result.rev == ''


def test_recipe_document(recipe_document, database):
    result = recipe_document

    assert result in database.all_docs()


def test_permissions_document(permissions_document, database):
    result = permissions_document

    assert result in database.all_docs()


def test_conflicted_document(conflicted_document, database):
    result = conflicted_document

    assert database.all_docs() == [result]
    assert result.rev == '1-123'
    assert result.retrieve()
    assert result.rev == '1-789'
