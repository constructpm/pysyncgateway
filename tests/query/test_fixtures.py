

import datetime


def test_slow_view_calling_time(slow_view):
    start = datetime.datetime.now()

    slow_view.query_view('all')  # act

    end = datetime.datetime.now()
    assert (end - start).total_seconds() > 1.5


def test_food_query(food_query):
    result = food_query.query_view('all')

    assert result['total_rows'] == 5
