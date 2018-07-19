from os.path import join, dirname
import setuptools


with open(join(dirname(__file__), "README.md"), "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="elasticsearch_partition",
    version="1.0.1",
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
    keywords=['elasticsearch', 'partition', 'partitioning'],
    tests_require=['coverage']
)
