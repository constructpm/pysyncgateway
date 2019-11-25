Quickstart
==========

Install
-------

You can install ``pysyncgateway`` from `PyPi
<https://pypi.org/project/pysyncgateway/>`_::

    pip install pysyncgateway


Make an Admin Client
--------------------

Assuming that you have a Sync Gateway running with its admin port on
``http://localhost:4985/``, create an instance of :class:`AdminClient
<pysyncgateway.admin_client.AdminClient>` to connect:

.. testsetup::

    from __future__ import absolute_import, print_function, unicode_literals

.. doctest::

    >>> from pysyncgateway import AdminClient
    >>> admin_client = AdminClient('http://localhost:4985/')

Check that your ``admin_client`` instance is connected to the admin port by
loading the server info from Sync Gateway:

.. doctest::

    >>> server_info = admin_client.get_server()
    >>> sorted(list(server_info))
    ['ADMIN', 'couchdb', 'vendor', 'version']
    >>> server_info['ADMIN']
    True
    >>> server_info['version']
    'Couchbase Sync Gateway/1.5.1(4;cb9522c)'

You can use the admin client to load a list of databases currently on the Sync
Gateway (the `default Docker container
<https://hub.docker.com/r/couchbase/sync-gateway/>`_ is initialised with a
database called 'db'):

.. doctest::
    :hide:

    >>> admin_client.get_database('db').create()
    True

.. doctest::

    >>> print(admin_client.all_databases())
    [<Database "http://localhost:4985/db/">]


Create Database
---------------

Create a new instance of :class:`Database <pysyncgateway.database.Database>` to
contain our test user and document:

.. doctest::

    >>> database = admin_client.get_database('test')
    >>> database.create()
    True

The new 'test' database will not contain any documents or users:

.. doctest::

    >>> database.all_docs()
    []
    >>> database.all_users()
    []


Create some Documents
---------------------

First create a :class:`Document <pysyncgateway.document.Document>` with the ID
'message'. This will have the "Hello World!" content and be in the 'world'
channel (we'll use this to test with our User later):

.. doctest::

    >>> hello_doc = database.get_document('message')
    >>> hello_doc.data = {'content': 'Hello World!'}
    >>> hello_doc.set_channels('world')
    >>> hello_doc.create_update()
    1

Now create a second document with ID 'stuff' - this is not saved in any
channels:

.. doctest::

    >>> other_doc = database.get_document('stuff')
    >>> other_doc.data = {'private_info': 'Secret things'}
    >>> other_doc.create_update()
    1

Finally, check with the admin client that those two documents are in the
database.

.. doctest::

    >>> sorted(database.all_docs())
    [<Document "http://localhost:4985/test/message">, <Document "http://localhost:4985/test/stuff">]


Create a User
-------------

Now we need a :class:`User <pysyncgateway.user.User>` in the database to check
that our created documents work OK - we create this from the database instance.
At first the user instance will not be subscribed to any channels:

.. doctest::

    >>> user = database.get_user('friend')
    >>> user.set_password('__PASSWORD__')
    >>> user.create_update()
    1

``pysyncgateway`` provides a :class:`UserClient
<pysyncgateway.user_client.UserClient>` which we can now connect to the public
port at ``http://localhost:4984/`` with the credentials we created for the
'friend' User above. Again, load the server info to ensure that the client is
connected - but this time there is no 'ADMIN' key in the response because the
client is connected on the public port.

.. doctest::

    >>> from pysyncgateway import UserClient
    >>> user_client = UserClient('http://localhost:4984/')
    >>> user_client.auth('friend', '__PASSWORD__')
    >>> server_info = user_client.get_server()
    >>> sorted(list(server_info))
    ['couchdb', 'vendor', 'version']

Now check a list of the documents that the user can access. We first have to
generate a second database instance - this one is for the user client rather
than the admin client.

.. doctest::

    >>> user_database = user_client.get_database('test')
    >>> user_database.all_docs()
    []

They have no access to any documents!

Grant access to the 'message' document by using the admin client to subscribe
the 'friend' User to the 'world' channel:

.. doctest::

    >>> user.set_admin_channels('world')
    >>> user.create_update()
    2

Now the 'friend' user can retrieve the message document:

.. doctest::

    >>> user_docs = user_database.all_docs()
    >>> user_docs
    [<Document "http://localhost:4984/test/message">]
    >>> message = user_docs[0]
    >>> message.retrieve()
    True
    >>> message.data
    {'content': 'Hello World!'}

Success!


Clean up
--------

Finally, the admin client can be used to remove the 'test' database. This will
cascade into the Sync Gateway and remove all users and documents in that
database:

.. doctest::

    >>> database.delete()
    True


.. testcleanup::

    from tests.conftest import purge_databases
    purge_databases(admin_client)
