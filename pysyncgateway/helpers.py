from __future__ import absolute_import, print_function, unicode_literals


class ComparableMixin:
    """
    Alex Martelli's suggestion from https://stackoverflow.com/a/1061350/1286705
    """

    def __eq__(self, other):
        return not self < other and not other < self

    def __ne__(self, other):
        return self < other or other < self

    def __gt__(self, other):
        return other < self

    def __ge__(self, other):
        return not self < other

    def __le__(self, other):
        return not other < self
