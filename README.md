# Elasticsearch Partitioning
[![image](https://img.shields.io/pypi/v/elasticsearch-partition.svg)](https://pypi.python.org/pypi/elasticsearch-partition)
[![Build Status](https://travis-ci.com/dmvass/elasticsearch-partition.svg?branch=master)](https://travis-ci.com/kandziu/elasticsearch-partition)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/dmvass/elasticsearch-partition/blob/master/LICENSE)

A Python library for creating indexes by date range and fetching data from
partitioned indexes. This can be achieved with the Elasticsearch Multiple
Indeces API because most Elasticsearch APIs that refer to an index parameter
support execution across multiple indices, using simple `test1,test2,test3`
notation (or _all for all indices). It also support wildcards, for example:
test*, `*test`, `te*t` or `*test*`, and the ability to "exclude" (-), for
example: test*,-test3.

For time oriented data, such as logs, a common strategy is to partition data
into indexes that hold data for a certain time range. For example, the index
`logstash-2018.01.01` holds data for events that happened on `2018-01-01`, i.e.
a time range of a day. You can of course choose bigger or smaller time ranges
as well(`year`, `month` or `day` frequencies), depending on your needs. Using
index templates, you can easily manage settings and mappings for any index
created with a name starting with e.g. `logstash-*`.

When the day is over, nothing new will be written to its corresponding index.
Such indexes can be fully optimized to be as compact as possible, and possibly
moved somewhere for archiving purposes. When the data becomes too old to be of
interest, the data can easily be deleted by deleting the entire index for the
obsolete time ranges.

Searches can be run on just the relevant indexes for a selected time span. If
you are searching for something that happened on `2018-01-01`, there's no point
in searching any other index than that for `2018-01-01`.

Using this technique and `elasticsear-partition` module you can easy implemet
`Range Partitionnig` approach for your Elasticsearch queries. Some of this
examples we will consider below.

## Installation
Install the elasticsearch partition package with pip:
```
pip install elasticsearch-partition
```

## How to Use
### Basic usage
How to import and use partition module with `since` and `until` dates:
```python
import datetime
from elasticsearch_partition import partition

partition('logs-*', datetime.date(2016, 11, 29), datetime.date(2018, 2, 4))
# ['logs-2016-11-29', 'logs-2016-11-30', 'logs-2016-12-*', 'logs-2017-*',
# 'logs-2018-01-*', 'logs-2018-02-01', 'logs-2018-02-02', 'logs-2018-02-03',
# 'logs-2018-02-04']
```

When you are using `partition` only with `since` date, `until` will be replaced
on a current date.
```python
partition('logs-*', since=datetime.date(2018, 7, 10))
# ['logs-2018-07-10', 'logs-2018-07-11', 'logs-2018-07-12', 'logs-2018-07-13',
# 'logs-2018-07-14', 'logs-2018-07-15', 'logs-2018-07-16', 'logs-2018-07-17']
```

Or when you are using `partition` only with `until` all dates from `until` to
current date will be excluded.
```python
partition('logs-*', until=datetime.date(2018, 7, 10))
# ['-logs-2018-07-10', '-logs-2018-07-11', '-logs-2018-07-12',
# '-logs-2018-07-13', '-logs-2018-07-14', '-logs-2018-07-15',
# '-logs-2018-07-16', '-logs-2018-07-17', 'logs-*']
```

> Note: If `until` more then current date you can get an error.

### How to customize partitioning
If you want to change some `partition` bahavior you can do it ease with
`RangePartition` and `formatters` module, also you can use your custom date
`now` functions.
```python
from elasticsearch_partition import RangePartition
from elasticsearch_partition.partitioning import MONTH
from elasticsearch_partition.formatters import LittleEndianDateFormatter

# frequency - Index partitioning frequency
# formatter - Formatter instance
# escape - Special character which will be replaced on a date
# now_func - Get now date function
my_partition = RangePartition(
    frequency=MONTH,
    formatter=LittleEndianDateFormatter(sep='.'),
    escape='@',
    now_func=custom_date_now,
)

my_partition('logs-@', datetime.date(2016, 11, 29), datetime.date(2018, 2, 4))
# ['logs-11.2016', 'logs-12.2016', 'logs-*.2017', 'logs-01.2018', 'logs-02.2018']
```

### How to create custom date formatter
All date formatters must be inherited from abstract `DateFormatter` class and
implement `fmt_year`, `fmt_month` and `fmt_day` methods. Some method accept
additional keyword parameter `wildcard` which used for creating formatted date
with specified wildcard character. For example `2018-04` will be replced on
`2018-04-*`, `2018` on `2018-*` etc.
```python
class MyDateFormatter(DateFormatter):
    def fmt_year(self, year, wildcard=False):
        # Should be implemented

    def fmt_month(self, year, month, wildcard=False):
        # Should be implemented
    
    def fmt_day(self, year, month, day):
        # Should be implemented
        # This method not accept 'wildcard' parameter

my_formatter = MyDateFormatter()
partition = RangePartition(formatter=my_formatter)
```

### How to use with [elasticsearch-py](https://github.com/elastic/elasticsearch-py)
This is useful for all Elasticsearch APIs that refer to an index parameter
support execution across multiple indices.
```python
from elasticsearch import Elasticsearch

es = Elasticsearch()
indexes = partition(
    'logs-*',
    datetime.date(2016, 11, 29),
    datetime.date(2018, 2, 4)
)
res = es.search(index=indexes, body={"query": {"match_all": {}}})
```

### How to use with [elasticsearch-dsl-py](https://github.com/elastic/elasticsearch-dsl-py)
This is useful for all Elasticsearch APIs that refer to an index parameter
support execution across multiple indices and similar for simple Search and
Persistance DSL.
```python
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search

client = Elasticsearch()

indexes = partition(
    'logs-*',
    datetime.date(2016, 11, 29),
    datetime.date(2018, 2, 4)
)
search = Search(using=client, index=indexes) \
    .filter("term", category="search") \
    .query("match", title="python") \
    .exclude("match", description="beta")

response = search.execute()
```

## Cython
For an extra speed boost when deploying your application in production, Elasticsearch
Partitioning can compile itself with Cython.
```
pip install cython
pip install elasticsearch-partition
```

## Changes
A full changelog is maintained in the [CAHNGELOG](https://github.com/dmvass/elasticsearch-partition/blob/master/CHANGELOG.md) file.

## Contributing 
**elasticsearch-partition** is an open source project and contributions are
welcome! Check out the [Issues](https://github.com/dmvass/elasticsearch-partition/issues)
page to see if your idea for a contribution has already been mentioned, and feel
free to raise an issue or submit a pull request.
