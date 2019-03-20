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
    """This class implements a callable interface for create range
    partition indexes by date with specified frequency.

    :attr int frequency: index partitioning frequency
    :attr str escape: special character which will be replaced on a date
    :attr callable now_func: get now date function
    :attr DateFormatter formatter: formatter instance

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

        if formatter is None:
            self.formatter = BigEndianDateFormatter()
        else:
            self.formatter = <DateFormatter> formatter

        self.frequency = frequency
        self.escape = escape
        self.now_func = now_func or _now_func

    cdef str fmt_yearly(self, TimeWindow tw, date_t *date):
        return self.formatter.fmt_year(date.year, wildcard=False)

    cdef str fmt_monthly(self, TimeWindow tw, date_t *date):
        cdef str fmt_date

        if date.year == tw.since.year or date.year == tw.until.year:
            fmt_date = self.formatter.fmt_month(
                date.year, date.month, wildcard=False
            )
        else:
            fmt_date = self.formatter.fmt_year(date.year, wildcard=True)

        return fmt_date

    cdef str fmt_daily(self, TimeWindow tw, date_t *date):
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
        """Creates and returns Elasticsearch partitioned indexes by
        date with specified frequency.

        :param str pattern: index name with a special character
        :param TimeWindow time_window: time window instance
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
            func_ptr = self.fmt_yearly
        elif self.frequency == FREQUENCY.MONTH:
            func_ptr = self.fmt_monthly
        else:
            func_ptr = self.fmt_daily

        tw.calculate(self.frequency)

        for idx in range(tw.size):
            date = <date_t> (tw.data_ptr[idx])
            fmt_date = func_ptr(self, tw, &date)
            indexes.append(pattern.replace(self.escape, fmt_date))

        return indexes

    def __call__(self, pattern, since=None, until=None):
        """Creates and returns Elasticsearch partitioned indexes by
        date with specified frequency.

        :param str pattern: index name with a special character
        :param datetime since: since partitioning date
        :param datetime until: until partitioning date

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
