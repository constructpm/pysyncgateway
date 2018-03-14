# encoding: utf-8
from __future__ import absolute_import, print_function, unicode_literals


def test(empty_document):
    """
    Assert that type in repr is Document because this function is provided by
    Resource.
    """
    result = unicode(empty_document)

    assert result.startswith('<Document ')
