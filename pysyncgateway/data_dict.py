from __future__ import absolute_import, print_function, unicode_literals

import six

from .exceptions import InvalidDataKey


class DataDict(dict):
    """
    DataDict is the developer facing dictionary of data contained within a
    Couchbase Document. It prevents settings items with reserved Couchbase keys
    like "_rev" or "_id", but still acts like a dictionary to make manipulating
    Document data easy.

    NOTE: It is not design agnostic because it protects the "channels" key.
    Depending on your application and sync function, that might not be a list
    of channels in your data design.
    """

    filtered_keys = (
        '_id',
        '_rev',
        'channels',
    )

    @classmethod
    def from_dict(obj, data):
        """
        Given a dictionary `data`, create a new DataDict from a dictionary
        `data`, silently removing all filtered keys from that input.

        Args:
            data (dict): Input data.

        Returns:
            DataDict: New instance created with cleaned, copied `data`.

        Raises:
            ValueError: When passed a non-dict.
        """
        if not isinstance(data, dict):
            raise ValueError('data argument is not dict')
        new = obj()
        for key, value in six.iteritems(data):
            try:
                new[key] = value
            except InvalidDataKey:
                pass
        return new

    def __setitem__(self, key, value):
        """
        Assign value to key as usual, but only if `key` is not in
        `filtered_keys` list.

        Args:
            key (str)
            value

        Raises:
            InvalidDataKey: When data is passed that is not managed by
                DataDict.
        """
        if key in self.filtered_keys:
            raise InvalidDataKey('DataDict does not allow "{}" key'.format(key))
        return super(DataDict, self).__setitem__(key, value)

    def to_dict(self):
        """
        Returns:
            dict: A dictionary version of self
        """
        return dict(self)
