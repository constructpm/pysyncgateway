

from pysyncgateway import Query


def test(database):
    query = Query(database, '__DESIGN_DOC_ID__')

    result = query.build_view_url('__VIEW_NAME__')

    assert result == 'http://localhost:4985/db/_design/__DESIGN_DOC_ID__/_view/__VIEW_NAME__'
