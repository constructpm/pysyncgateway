Changelog
=========

All notable changes to this project will be documented in this file.

The format is based on `Keep a Changelog
<http://keepachangelog.com/en/1.0.0/>`_ and this project adheres to `Semantic
Versioning <http://semver.org/spec/v2.0.0.html>`_.


Unreleased
----------

Added
.....

* ``Database.get_query()`` shortcut for loading Query documents.

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
