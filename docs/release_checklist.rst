Release checklist
=================

Items to be completed for each release. Given a new version called ``x.y.z``:

* Create a branch for the new release. Usually called something like
  ``bump-vx.y.z``.

* Update ``__version__`` in `__about__.py
  <https://github.com/constructpm/pysyncgateway/blob/master/pysyncgateway/__about__.py>`_
  with the new version number ``'x.y.z'``.

* Update `CHANGELOG <https://github.com/constructpm/pysyncgateway/blob/master/CHANGELOG.rst>`_.

  - Add a new subtitle below ``Unreleased`` after the note about latest
    documentation, in the format ``x.y.z_ - yyyy/mm/dd``, where ``yyyy/mm/dd``
    is the reverse formatted date of the day the release is created.

  - Update the ``.. _Unreleased:`` link at the bottom of the page to compare
    ``vx.y.z...HEAD``.

  - Under the ``_Unreleased`` link, create a new link for the release
    ``.. _x.y.z: https:/[...]/compare/va.b.c...vx.y.z``, where ``va.b.c`` is
    the previous release.

* Commit changes and push ``bump-vx.y.z`` branch for testing.

* Now is a good time to build and check the documentation locally.

* When branch ``bump-vx.y.z`` is green, then merge it to ``master``.

* Update master locally and ensure that you remain on master for the rest of
  the process.

* Test that a build can be shipped to test PyPI with ``make testpypi``. (Every
  build runs the full clean test suite locally to ensure that nothing has
  broken before building)

* After successful push, check the `TestPyPI page
  <https://test.pypi.org/project/pysyncgateway/>`_.

* Then tag the repo with ``make tag``. Add a short message about what the key
  change is.

* Make the new tag public with ``git push origin --tags``.

* Build and push to PyPI with ``make pypi``.

* After successful push, check the `PyPI page
  <https://pypi.org/project/pysyncgateway/>`_.

Post release checks
-------------------

* Visit the `CHANGELOG
  <https://github.com/constructpm/pysyncgateway/blob/master/CHANGELOG.rst>`_
  and ensure that the new release's comparison link works with the new tag.

* Check the `RTD builds
  <https://readthedocs.org/projects/pysyncgateway/builds/>`_ to ensure that the
  latest documentation version has been picked up and that the ``stable`` docs
  are pointed at it.

  A new docs release will not have been created for the new tag as per `this
  issue <https://github.com/rtfd/readthedocs.org/issues/3508>`_. Click "Build
  Version:" on the builds page for the new tag to be picked up.
