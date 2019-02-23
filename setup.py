import glob
from os import path
import re

import setuptools

try:
    from Cython.Distutils import build_ext
    CYTHON = True
except ImportError:
    CYTHON = False

BASE_DIR = path.abspath(path.dirname(__file__))


def find_version(fname):
    """Attempts to find the version number in the file names fname.
    Raises RuntimeError if not found.
    """
    version = ""
    with open(path.join(BASE_DIR, fname), "r") as fp:
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
    with open(path.join(BASE_DIR, fname), "r") as fh:
        return fh.read()


if CYTHON:
    def modules(dirname):
        filenames = glob.glob(path.join(dirname, "*.py"))

        module_names = []
        for name in filenames:
            module, ext = path.splitext(path.basename(name))
            if module != "__init__":
                module_names.append(module)

        return module_names

    package_names = ["elasticsearch_partition"]
    ext_modules = [
        setuptools.Extension(
            package + "." + module,
            [path.join(*(package.split(".") + [module + ".py"]))]
        )
        for package in package_names
        for module in modules(path.join(BASE_DIR, *package.split(".")))
    ]

    cmdclass = {"build_ext": build_ext}
else:
    ext_modules = []
    cmdclass = {}


setuptools.setup(
    name="elasticsearch_partition",
    version=find_version("elasticsearch_partition/__init__.py"),
    author="Dmitri Vasilishin",
    author_email="vasilishin.d.o@gmail.com",
    description="A Python library for creating Elasticsearch partitioned "
                "indexes by date range",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    url="https://github.com/kandziu/elasticsearch-partition",
    packages=setuptools.find_packages(exclude=("tests")),
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
    keywords=["elasticsearch", "partition", "partitioning"],
    tests_require=["coverage"],
    extras_require={"dev": ["tox", "bumpversion"]},
    cmdclass=cmdclass,
    ext_modules=ext_modules
)
