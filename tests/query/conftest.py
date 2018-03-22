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
    sleep-like function that locks up Walrus for 1s per document. Fixture
    populates the database with enough documents to ensure that calling the
    view takes at least 2 seconds total.

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
function(doc, meta) {
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


@pytest.fixture
def food_query(database):
    """
    Populates the database with some foods and builds a query, all written to
    Sync Gateway. View does not need hotting up because docs are in place when
    it is created.

    Returns:
        Query: With 'all' view populated where key will search for the foods
            where the first letter of the name of the food matches.
    """
    for name, data in [
        ('lightbulb', {
            'type': 'fixture',
            'name': 'Lightbulb',
        }),
        ('apple', {
            'type': 'food',
            'name': 'apple',
        }),
        ('banana', {
            'type': 'food',
            'name': 'banana',
        }),
        ('apricot', {
            'type': 'food',
            'name': 'apricot',
        }),
        ('walrus', {
            'type': 'animal',
            'name': 'I AM THE WALRUS',
        }),
        ('almond', {
            'type': 'food',
            'name': 'almond',
        }),
        ('pumpkin', {
            'type': 'food',
            'name': 'pumpkin',
        }),
    ]:
        doc = database.get_document(name)
        doc.data = data
        doc.create_update()
    query = Query(database, 'food_index')
    query.data = {
        'views': {
            'all': {
                'map':
                """
function(doc, meta) {
    if(doc.type == "food" && doc.name) {
        emit(doc.name[0], doc)
    }
}
""",
            },
        },
    }
    query.create_update()
    return query
