import re
import setuptools


def find_version(fname):
    """Attempts to find the version number in the file names fname.
    Raises RuntimeError if not found.
    """
    version = ''
    with open(fname, 'r') as fp:
        reg = re.compile(r'__version__ = [\'"]([^\'"]*)[\'"]')
        for line in fp:
            m = reg.match(line)
            if m:
                version = m.group(1)
                break
    if not version:
        raise RuntimeError('Cannot find version information')
    return version


__version__ = find_version('elasticsearch_partition/__init__.py')


with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="elasticsearch_partition",
    version=__version__,
    author="Dmitri Vasilishin",
    author_email="vasilishin.d.o@gmail.com",
    description="A small example package",
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
    keywords=['elasticsearch', 'partition']
)
