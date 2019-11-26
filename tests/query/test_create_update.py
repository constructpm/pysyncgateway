import pytest
from pysyncgateway import Query


@pytest.fixture
def existing_query(query):
    """
    Returns:
        Query: With a single "True" view (maps all rows) called "one".
    """
    query.data = {
        'views': {
            'one': {
                'map': 'function(doc, meta){emit(1, doc);}',
            },
        },
    }
    query.create_update()
    return query


def test_existing_query(existing_query):
    result = existing_query

    assert result.retrieve()
    assert 'function(doc, meta){emit(1, doc);}' in result.data['views']['one']['map']


# --- TESTS ---


def test(query, database):
    view_func = """
        function (doc, meta){
            if(meta.id.indexOf("projects")>-1) {
                emit(meta.id.substring(meta.id.indexOf("|") + 1), doc);
            }
        }
    """
    data = {
        'views': {
            'all_lists': {
                'map': view_func,
            },
        },
    }
    query.data = data

    result = query.create_update()

    assert result is True
    clean_query = Query(database, 'all_lists')
    clean_query.retrieve()
    assert list(clean_query.data) == ['views']
    assert list(clean_query.data['views']) == ['all_lists']
    assert list(clean_query.data['views']['all_lists']) == ['map']
    assert view_func in clean_query.data['views']['all_lists']['map']


def test_update(existing_query, database):
    existing_query.data = {
        'views': {
            'one': {
                'map': 'function(doc, meta){1==1;}',
            },
        },
    }

    result = existing_query.create_update()

    assert result is True
    clean_query = Query(database, 'all_lists')
    clean_query.retrieve()
    assert list(clean_query.data) == ['views']
    assert list(clean_query.data['views']) == ['one']
    assert list(clean_query.data['views']['one']) == ['map']
    assert 'function(doc, meta){1==1;}' in clean_query.data['views']['one']['map']
