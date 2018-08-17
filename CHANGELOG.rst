Changelog
=========

All notable changes to this project will be documented in this file.

The format is based on `Keep a Changelog
<http://keepachangelog.com/en/1.0.0/>`_ and this project adheres to `Semantic
Versioning <http://semver.org/spec/v2.0.0.html>`_.


Unreleased_
-----------

See also `latest documentation
<https://pysyncgateway.readthedocs.io/en/latest/>`_

Added
.....

* Extended linting to include ``flake8-aaa`` to lint tests.

Changed
.......

* Bumped version of ``requests`` in requirements to ``2.19.1``, but kept
  requirement in ``setup.py`` the same at ``>=2.18``.

* Improved output in stacktraces when ``RevisionMismatch`` is raised. Now
  includes URL of resource and any revision number that was sent.

1.1.0_ - 2018/05/23
-------------------

Changed
.......

* Adjusted how provided ``key`` values are serialized when querying a view in a
  Query design document. Now ``key`` values are serialized to JSON allowing for
  multi-key views to be queried.

  This is a breaking change because any single key value was previously
  converted to a string before serialization to JSON. Now ``key`` is serialized
  to JSON directly in ``Query.query_view()``.


1.0.0_ - 2018/04/09
-------------------

Stable release.

Added
.....

* Extended test suite to include initial smoke tests on Python 3 which assert
  that package is installable.


0.2.0_ - 2018/04/04
-------------------

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

.. _Unreleased: https://github.com/constructpm/pysyncgateway/compare/v1.1.0...HEAD
.. _1.1.0: https://github.com/constructpm/pysyncgateway/compare/v1.0.0...v1.1.0
.. _1.0.0: https://github.com/constructpm/pysyncgateway/compare/v0.2.0...v1.0.0
.. _0.2.0: https://github.com/constructpm/pysyncgateway/compare/v0.1.3...v0.2.0
