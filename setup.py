import re
import setuptools
import pathlib


# Loading version
here = pathlib.Path(__file__).parent
txt = (here / 'elasticsearch_partition' / '__init__.py').read_text()
__version__ = re.findall(r"^__version__ = '([^']+)'\r?$", txt, re.M)[0]


with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="elasticsearch_partition",
    version=__version__,
    author="Dmitri Vasilishin",
    author_email="vasilishin.d.o@gmail.com",
    description="A Python library for creating Elasticsearch partitioned indexes by date range",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kandziu/elasticsearch-partition",
    packages=setuptools.find_packages(exclude=('test*')),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords=['elasticsearch', 'partition', 'partitioning']
)
