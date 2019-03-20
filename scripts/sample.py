import datetime
import pprint

from elasticsearch_partition import partition


pp = pprint.PrettyPrinter(indent=2)

since = datetime.date(1970, 7, 10)
until = datetime.date(2018, 8, 26)

pp.pprint(partition("logs-*", since, until))
