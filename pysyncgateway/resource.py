from __future__ import absolute_import, print_function, unicode_literals

from .data_dict import DataDict
from .helpers import ComparableMixin


class Resource(ComparableMixin, object):
    """
    A Couchbase object stored within a Database, identified by a URL and
    accessible through REST verbs. Data is stored in a DataDict manager.

    Attributes:
        _data (DataDict)
        database (Database)
    """

    def __init__(self, database):
        """
        Initialise a Resource with a database.

        Args:
            database (Database)
        """
        if not getattr(database, 'url', None):
            raise ValueError(
                '{class_name} needs a `database` that provides a populated '
                '`url` (usually a `Database` instance), not {found}'.format(
                    class_name=self.__class__.__name__,
                    found=type(database).__name__,
                ),
            )
        self.database = database
        self.data = {}

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data):
        self._data = DataDict.from_dict(data)

    def __lt__(self, other):
        return self.url < other.url

    def __hash__(self):
        return hash(self.url)

    def __repr__(self):
        """
        Provides 'nice' output if object has defined `url` attribute. Else
        falls back to default.
        """
        try:
            nice_output = unicode(self)
            return nice_output.encode('UTF8')
        except (AttributeError, UnicodeEncodeError):
            return super(Resource, self).__repr__()

    def __unicode__(self):
        return '<{class_name} "{url}">'.format(
            class_name=self.__class__.__name__,
            url=self.url,
        )
