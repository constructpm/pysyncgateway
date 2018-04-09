from __future__ import absolute_import, print_function, unicode_literals

import os

from setuptools import setup

basedir = os.path.dirname(__file__)


def readme():
    with open(os.path.join(basedir, 'README.rst')) as f:
        return f.read()


about = {}
with open(os.path.join(basedir, 'pysyncgateway', '__about__.py')) as f:
    exec (f.read(), about)

setup(
    name=about['__name__'],
    version=about['__version__'],
    description=about['__description__'],
    long_description=readme(),
    url='https://github.com/constructpm/pysyncgateway',
    author=about['__author__'],
    author_email=about['__email__'],
    license='Apache License 2.0',
    install_requires=[
        'requests>=2.18',
        'six>=1.10',
    ],
    packages=['pysyncgateway'],
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python',
    ],
)
