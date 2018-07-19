""" This module provide range partition method for your Elasticsearch
indexes. If you have a logic index partition you could use this module
for creating and searching through indexes by time range.

A partition is a division of a logical database or its constituent
elements into distinct independent parts. Database partitioning is
normally done for manageability, performance or availability reasons,
or for load balancing.
"""

from calendar import monthrange
import datetime
from itertools import groupby

from .formatters import DateFormatter, BigEndianDateFormatter


__all__ = ('RangePartitioning', 'TimeWindow', 'partition')


# Public constants for convenience
YEAR = 1
MONTH = 2
DAY = 3

_MAXMONTH = 12


def _group_by(iterable, key):
    """
    Group By implementation.

    :param Iterator iterable: Iterable sequesnce of date objects
    :param callable key: Function for getting attributes
    :yield (str, Iterator): Key with grouped values
    """
    for key, values in groupby(iterable, key=key):
        yield key, values


def _group_by_year(iterable):
    """
    Group and returns iterable sequence by year.

    :param Iterator iterable: Iterable sequesnce of date objects
    :return (year: str, Iterator): Grouped dates by year
    """
    return _group_by(iterable, key=lambda x: x.year)


def _group_by_month(iterable):
    """
    Group and returns iterable sequence by month.

    :param Iterator iterable: Iterable sequesnce of date objects
    :return (month: str, Iterator): Grouped dates by month
    """
    return _group_by(iterable, key=lambda x: x.month)


def _exclude(pattern):
    """
    Change index name to Elasticsearch exclude style.

    :param str pattern: Index name with a specified symbol
    :rtype: str
    """
    return '-' + pattern


class TimeWindow:
    __slots__ = ('since', 'until')

    def __init__(self, since, until):
        if not isinstance(since, datetime.date):
            raise TypeError("The 'since' parameter must be a 'date' type")

        if not isinstance(until, datetime.date):
            raise TypeError("The 'until' parameter must be a 'date' type")

        if since > until:
            raise ValueError("'since' can't be more than 'until'")

        self.since = since
        self.until = until

    @property
    def delta_years(self):
        """
        Returns delta in years.
        """
        return self.until.year - self.since.year

    @property
    def delta_days(self):
        """
        Returns delta in days.
        """
        return (self.until - self.since).days

    def __iter__(self):
        """
        Iterate over time periods by day.
        """
        curren_date = self.since
        while curren_date <= self.until:
            yield curren_date
            curren_date += datetime.timedelta(days=1)


class RangePartitioning:
    """
    Range partitioning maps data to partitions based on ranges of values
    of the partitioning index name that you establish for each partition.
    It is the most common type of partitioning and is often used with dates.

    For an index with a date prefix as the partitioning key, the January-2018
    partition would has name with partitioning prefix from '2018-01-01'
    to '2018-01-31'.
    """

    def __init__(self,
                 frequency=DAY,
                 formatter=None,
                 escape='*',
                 now_func=None):
        """
        Initialize range partitioning instance.

        :param int frequency: Index partitioning frequency
        :param DateFormatter formatter: Formatter instance
        :param str escape: Special character which will be replaced on a date
        :param callable now_func: Get now date function
        """

        if formatter is None:
            self._formatter = BigEndianDateFormatter()
        else:
            if not isinstance(formatter, DateFormatter):
                raise TypeError(
                    "The 'formatter' must be an instance of 'DateFormatter'"
                )
            self._formatter = formatter

        self._frequency = frequency
        self._escape = escape
        self._now_func = now_func or self.__get_now_date

    def __get_now_date(self):
        return datetime.datetime.now().date()

    def partition(self, pattern, tm):
        """
        This method create and returns Elasticsearch partitioned indexes
        by date frequency.

        :param str pattern: Index name with a special character
        :param TimeWindow tm: Time window instance
        :rtype: list
        """

        def fmt_index(fmt_date):
            # Helper function for better index formatting
            return pattern.replace(self._escape, fmt_date)

        indexes = []
        for year, iterable in _group_by_year(tm):
            # Frequency by year
            if self._frequency == YEAR:
                fmt_date = self._formatter.fmt_year(year)
                indexes.append(pattern.replace(self._escape, fmt_date))
                continue

            # Temporary list for months and days indexes
            _indexes = []
            month_count = 0
            for month, iterable in _group_by_month(iterable):
                # Frequency by day
                if self._frequency > MONTH:
                    # Load all month days to a memory
                    days = list(iterable)
                    if len(days) != monthrange(year, month)[1]:
                        for date in days:
                            fmt_date = self._formatter.fmt_day(
                                date.year, date.month, date.day
                            )
                            _indexes.append(fmt_index(fmt_date))
                    else:
                        # Increase month counter and append formatted date
                        # to the temporary indexes list
                        month_count += 1
                        fmt_date = self._formatter.fmt_month(
                            year, month, wildcard=True
                        )
                        _indexes.append(fmt_index(fmt_date))

                # Frequency by month
                else:
                    month_count += 1
                    fmt_date = self._formatter.fmt_month(year, month)
                    _indexes.append(fmt_index(fmt_date))

            if month_count == _MAXMONTH:
                # Append formatted year with wildcard character if month
                # counter is full
                fmt_date = self._formatter.fmt_year(year,  wildcard=True)
                indexes.append(fmt_index(fmt_date))
            else:
                # Append temporary indexes to the main index list
                indexes.extend(_indexes)

        return indexes

    def __call__(self, pattern, since=None, until=None):
        """
        Returns Elasticsearch partitioned indexes by date range.

        :param str pattern: Index name with a special character
        :param datetime since: Since partitioning date
        :param datetime until: Until partitioning date
        """
        if self._escape not in pattern:
            raise ValueError("Index pattern '%s' doesn't contain a special "
                             "character '%s'" % (pattern, self._escape))

        if not since and not until:
            raise ValueError("You should use 'since' or 'until' for "
                             "searching by partitioning index")

        if not since:
            tm = TimeWindow(until, self._now_func())
            if self._frequency == YEAR and tm.delta_years < 1:
                indexes = [pattern]
            else:
                indexes = self.partition(_exclude(pattern), tm)
                indexes.append(pattern)
        else:
            tm = TimeWindow(since, until or self._now_func())
            indexes = self.partition(pattern, tm)

        return indexes


# Default Elasticsearch partitioning by day with big-endian date formatter
partition = RangePartitioning()
