import os
import re

import setuptools
from Cython.Build import cythonize  # NOQA


BASE_DIR = os.path.abspath(os.path.dirname(__file__))


def find_version(fname):
    """Attempts to find the version number in the file names fname.
    Raises RuntimeError if not found.
    """
    version = ""
    with open(os.path.join(BASE_DIR, fname), "r") as fp:
        regex = re.compile(r'__version__ = [\'"]([^\'"]*)[\'"]')
        for line in fp:
            m = regex.match(line)
            if m:
                version = m.group(1)
                break
    if not version:
        raise RuntimeError("Cannot find version information")
    return version


def read(fname):
    with open(os.path.join(BASE_DIR, fname), "r") as fh:
        return fh.read()


setuptools.setup(
    name="elasticsearch_partition",
    version=find_version("elasticsearch_partition/__init__.py"),
    author="Dmitri Vasilishin",
    author_email="vasilishin.d.o@gmail.com",
    description="A Python library for creating Elasticsearch partitioned "
                "indexes by date range",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    url="https://github.com/dmvass/elasticsearch-partition",
    packages=setuptools.find_packages(exclude=("tests", "scripts")),
    include_package_data=True,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords=["elasticsearch", "partition", "cython", "bigdata"],
    install_requires=["cython"],
    extras_require={"dev": ["tox", "bumpversion"]},
    ext_modules=cythonize(["elasticsearch_partition/*.pyx"])
)
