from __future__ import absolute_import, print_function, unicode_literals

import pytest

from pysyncgateway import Database, Query


@pytest.fixture
def database(admin_client):
    """
    Returns:
        Database: 'db' database written to Sync Gateway.
    """
    database = Database(admin_client, 'db')
    database.create()
    return database


@pytest.fixture
def query(database):
    """
    Returns:
        Query: Not written to Sync Gateway.
    """
    return Query(database, 'all_lists')


@pytest.fixture
def slow_view(database):
    """
    A view that returns all documents, but slowly. This uses a horrible
    sleep-like function that locks up Walrus for 1s.

    Fixture populates the database with enough documents to ensure that calling
    the view takes at least 2 seconds total.

    Returns:
        Query: Called 'slow_lists', written to Sync Gateway, with a single view
            called 'all' that takes 1 second per document in the database.
    """
    database.get_document('a').create_update()
    database.get_document('b').create_update()
    query = Query(database, 'slow_lists')
    query.data = {
        'views': {
            'all': {
                'map':
                """
function (doc, meta){
    function pausecomp(millis){
        var date = new Date();
        var curDate = null;
        do { curDate = new Date(); }
        while(curDate-date < millis);
    }
    pausecomp(1000);
    emit(meta.id,doc);
}
        """,
            },
        },
    }
    query.create_update()
    return query
