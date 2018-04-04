Changelog
=========

All notable changes to this project will be documented in this file.

The format is based on `Keep a Changelog
<http://keepachangelog.com/en/1.0.0/>`_ and this project adheres to `Semantic
Versioning <http://semver.org/spec/v2.0.0.html>`_.


Unreleased
----------

See also `latest documentation
<https://pysyncgateway.readthedocs.io/en/latest/>`_


0.2.0_ - 2018/04/18
------------------

Added
.....

* ``Database.get_query()`` shortcut for loading Query documents.

* New ``Session`` class which operates on a Database. Additional
  ``Database.get_session()`` shortcut for loading Sessions.

Changed
.......

* Adjust Resource's data dict instance to raise ``InvalidDataKey`` rather than
  ``AssertionError`` when a prohibited key is added.

Internals
.........

* Module documentation added to git and RTD.

* Bandit to test security. As a result removed many uses of ``assert`` in code.

* Initialisation of Document and Database simplified.


0.1.3 - 2018/03/26
------------------

Initial beta release.

.. _0.2.0: https://github.com/constructpm/pysyncgateway/compare/v0.4...v0.5.0
