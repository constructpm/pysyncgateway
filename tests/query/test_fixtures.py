from __future__ import absolute_import, print_function, unicode_literals


import datetime


def test_slow_view_calling_time(slow_view):
    start = datetime.datetime.now()

    slow_view.query_view('all')

    end = datetime.datetime.now()
    assert (end - start).total_seconds() > 2
