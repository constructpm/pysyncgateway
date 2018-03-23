from __future__ import absolute_import, print_function, unicode_literals

from setuptools import setup

setup(
    name='pysyncgateway',
    version='0.1.0',
    description='Library for communication with Couchbase Sync Gateway',
    url='https://github.com/constructpm/pysyncgateway',
    author='James Cooke',
    author_email='github@jamescooke.info',
    license="http://www.apache.org/licenses/LICENSE-2.0",
    packages=['pysyncgateway'],
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python',
    ],
)
