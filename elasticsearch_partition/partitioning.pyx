# cython: c_string_type=str, c_string_encoding=ascii

import datetime

from dateutils cimport date_t, FREQUENCY, TimeWindow
from formatters cimport BigEndianDateFormatter, DateFormatter


__all__ = ("RangePartition", "partition")


# Public constants for convenience
YEAR = FREQUENCY.YEAR
MONTH = FREQUENCY.MONTH
DAY = FREQUENCY.DAY


def _now_func():
    return datetime.datetime.now().date


cdef class RangePartition:
    """
    Range partitioning maps data to partitions based on ranges of values
    of the partitioning index name that you establish for each partition.
    It is the most common type of partitioning and is often used with dates.

    For an index with a date prefix as the partitioning key, the January-2018
    partition would has name with partitioning prefix from '2018-01-01'
    to '2018-01-31'.

    """
    cdef:
        int frequency
        str escape
        object now_func
        DateFormatter formatter

    def __init__(self,
                 frequency=FREQUENCY.DAY,
                 formatter=None,
                 escape="*",
                 now_func=None):
        """
        Initialize range partitioning instance.

        :param int frequency: Index partitioning frequency
        :param DateFormatter formatter: Formatter instance
        :param str escape: Special character which will be replaced on a date
        :param callable now_func: Get now date function

        """
        if formatter is None:
            self.formatter = BigEndianDateFormatter()
        else:
            self.formatter = <DateFormatter> formatter

        self.frequency = frequency
        self.escape = escape
        self.now_func = now_func or _now_func

    cdef str fmt_year(self, TimeWindow tw, date_t *date):
        return self.formatter.fmt_year(date.year, wildcard=False)

    cdef str fmt_month(self, TimeWindow tw, date_t *date):
        cdef str fmt_date

        if date.year == tw.since.year or date.year == tw.until.year:
            fmt_date = self.formatter.fmt_month(
                date.year, date.month, wildcard=False
            )
        else:
            fmt_date = self.formatter.fmt_year(date.year, wildcard=True)

        return fmt_date

    cdef str fmt_day(self, TimeWindow tw, date_t *date):
        cdef str fmt_date

        if date.year == tw.since.year and date.month == tw.since.month:
            fmt_date = self.formatter.fmt_day(
                date.year, date.month, date.day
            )
        elif date.year == tw.until.year and date.month == tw.until.month:
            fmt_date = self.formatter.fmt_day(
                date.year, date.month, date.day
            )
        elif date.year == tw.since.year or date.year == tw.until.year:
            fmt_date = self.formatter.fmt_month(
                date.year, date.month, wildcard=True
            )
        else:
            fmt_date = self.formatter.fmt_year(date.year, wildcard=True)

        return fmt_date

    cdef list partition(self, str pattern, TimeWindow tw):
        """
        This method create and returns Elasticsearch partitioned indexes
        by date frequency.

        :param str pattern: Index name with a special character
        :param TimeWindow time_window: Time window instance
        :rtype: list

        """
        cdef:
            list indexes = []
            str fmt_date
            str (*func_ptr)(RangePartition, TimeWindow, date_t *)
            int idx
            date_t date

        # Defines the frequency formatting function
        if self.frequency == FREQUENCY.YEAR:
            func_ptr = self.fmt_year
        elif self.frequency == FREQUENCY.MONTH:
            func_ptr = self.fmt_month
        else:
            func_ptr = self.fmt_day

        tw.calculate(self.frequency)

        for idx in range(tw.size):
            date = <date_t> (tw.data_ptr[idx])
            fmt_date = func_ptr(self, tw, &date)
            indexes.append(pattern.replace(self.escape, fmt_date))

        return indexes

    def __call__(self, pattern, since=None, until=None):
        """
        Returns Elasticsearch partitioned indexes by date range.

        :param str pattern: Index name with a special character
        :param datetime since: Since partitioning date
        :param datetime until: Until partitioning date

        """
        if self.escape not in pattern:
            raise ValueError("Index pattern '%s' doesn't contain a special "
                             "character '%s'" % (pattern, self.escape))

        if not since and not until:
            raise ValueError("You should use 'since' or 'until' for "
                             "searching by partitioning index")

        if not since:
            tw = TimeWindow(until, self.now_func())
            if self.frequency == FREQUENCY.YEAR and tw.delta_years < 1:
                indexes = [pattern]
            else:
                indexes = self.partition("-" + pattern, tw)
                indexes.append(pattern)
        else:
            tw = TimeWindow(since, until or self.now_func())
            indexes = self.partition(pattern, tw)

        return indexes


# Default Elasticsearch partitioning by day with big-endian date formatter
partition = RangePartition()
