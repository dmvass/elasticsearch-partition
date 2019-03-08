from datetime import date
import timeit


setup_template = """
import datetime
from elasticsearch_partition import partition

since = {since!r}
until = {until!r}
"""


def sample(name, number=100000, **kwargs):
    result = timeit.timeit(
        "partition('logs-*', since, until)",
        setup=setup_template.format(**kwargs),
        number=number
    )

    print("\nBenchmark: {}".format(name))

    for key in sorted(kwargs.keys()):
        print("{0}: {1}".format(key, kwargs[key]))

    usec = (result / number) * 1e6
    report = "{0} loops, {1:.2f} usec per loop".format(number, usec)
    print("{0}\n{1}\n".format("-" * (len(report)), report))


if __name__ == '__main__':
    sample("a", since=date(1970, 7, 10), until=date(2018, 8, 26))
    sample("b", since=date(2001, 2, 25), until=date(2018, 5, 3))
    sample("c", since=date(2012, 8, 15), until=date(2018, 3, 20))
    sample("d", since=date(2016, 10, 12), until=date(2018, 3, 20))
    sample("e", since=date(2018, 3, 1), until=date(2018, 3, 7))
