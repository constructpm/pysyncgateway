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
``http://localhost:4985/``, create an Admin Client to connect:

.. testsetup::

    from __future__ import absolute_import, print_function, unicode_literals

.. testcode::

    from pysyncgateway import AdminClient
    admin_client = AdminClient('http://localhost:4985/')

Check that your ``admin_client`` instance is connected to the admin port by
loading the server info from Sync Gateway:

.. testcode::

    print(admin_client.get_server())

.. testoutput::

    {u'ADMIN': True, u'couchdb': u'Welcome', u'vendor': {u'version': 1.5, u'name': u'Couchbase Sync Gateway'}, u'version': u'Couchbase Sync Gateway/1.5.1(4;cb9522c)'}

You can use the Admin Client to load a list of databases currently on the Sync
Gateway (the `default Docker container
<https://hub.docker.com/r/couchbase/sync-gateway/>`_ is initialised with a
Database called 'db'):

.. testcode::
    :hide:

    admin_client.get_database('db').create()

.. testcode::

    print(admin_client.all_databases())

.. testoutput::

    [<Database "http://localhost:4985/db/">]

.. testcleanup::

    from tests.conftest import purge_databases
    purge_databases(admin_client)
