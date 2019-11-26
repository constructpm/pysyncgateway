# encoding: utf-8
def test(empty_document):
    """
    Assert that type in repr is Document because this function is provided by
    Resource.
    """
    result = str(empty_document)

    assert result.startswith("<Document ")
