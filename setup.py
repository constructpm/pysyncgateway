import os

from setuptools import setup

basedir = os.path.dirname(__file__)


def readme():
    with open(os.path.join(basedir, "README.rst")) as f:
        return f.read()


about = {}
with open(os.path.join(basedir, "pysyncgateway", "__about__.py")) as f:
    exec(f.read(), about)

setup(
    name=about["__name__"],
    version=about["__version__"],
    description=about["__description__"],
    long_description=readme(),
    url="https://github.com/constructpm/pysyncgateway",
    author=about["__author__"],
    author_email=about["__email__"],
    license="Apache License 2.0",
    install_requires=["requests>=2.23.0", "six>=1.13"],
    packages=["pysyncgateway"],
    python_requires=">=3.5, <4",
    zip_safe=False,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python",
    ],
)
