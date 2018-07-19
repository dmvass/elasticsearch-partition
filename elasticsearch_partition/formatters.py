from abc import ABCMeta, abstractmethod
import datetime


INVALID_SEP_CHARS = ['\\', '/', '*', '?', '"', '<', '>', '|', ' ', ',']

# Abstract metaclass with py2/py3 support
Abstract = ABCMeta('Abstract', (object,), {})


class DateFormatter(Abstract):
    """
    Abstract date formatter class.
    """

    def __init__(self, sep='-'):
        """
        Accepts separation character and initialize specified
        date formatter.
        """
        if sep in INVALID_SEP_CHARS:
            raise ValueError(
                "The separation character '%s' is not valid" % sep
            )
        self._sep = sep

    @abstractmethod
    def fmt_year(self, year, wildcard=False):
        pass

    @abstractmethod
    def fmt_month(self, year, month, wildcard=False):
        pass

    @abstractmethod
    def fmt_day(self, year, month, day):
        pass


class BigEndianDateFormatter(DateFormatter):
    """
    In this format the most significant data item is written before
    lesser data items i.e. year before month before day.

    (year, month, day), e.g. 2018-04-22 or 2018.04.22 or 2018/04/22
    """

    def fmt_year(self, year, wildcard=False):
        """
        Format and returns year in big-endian order style.

        :param int year: Year
        :param bool wildcard: Use wildcard instead day and month
        :rtype: str
        """
        date = datetime.date(year=year, month=1, day=1)
        if wildcard:
            return date.strftime('%Y{sep}*'.format(sep=self._sep))
        return date.strftime('%Y')

    def fmt_month(self, year, month, wildcard=False):
        """
        Format and returns month in big-endian order style.

        :param int year: Year
        :param int month: Month
        :param bool wildcard: Use wildcard instead day
        :rtype: str
        """
        date = datetime.date(year=year, month=month, day=1)
        if wildcard:
            return date.strftime('%Y{sep}%m{sep}*'.format(sep=self._sep))
        return date.strftime('%Y{sep}%m'.format(sep=self._sep))

    def fmt_day(self, year, month, day):
        """
        Format and returns day in big-endian order style.

        :param int year: Year
        :param int month: Month
        :param int day: Day
        :rtype: str
        """
        date = datetime.date(year, month, day)
        return date.strftime('%Y{sep}%m{sep}%d'.format(sep=self._sep))


class LittleEndianDateFormatter(DateFormatter):
    """
    In this format the most significant data item is written after
    lesser data items i.e. day before month before year.

    (day, month, year), e.g. 22-04-2018 or 22.04.2018 or 22/04/2018
    """

    def fmt_year(self, year, wildcard=False):
        """
        Format and returns year in little-endian order style.

        :param int year: Year
        :param bool wildcard: Use wildcard instead day and month
        :rtype: str
        """
        date = datetime.date(year=year, month=1, day=1)
        if wildcard:
            return date.strftime('*{sep}%Y'.format(sep=self._sep))
        return date.strftime('%Y'.format(sep=self._sep))

    def fmt_month(self, year, month, wildcard=False):
        """
        Format and returns month in little-endian order style.

        :param int year: Year
        :param int month: Month
        :param bool wildcard: Use wildcard instead day
        :rtype: str
        """
        date = datetime.date(year=year, month=month, day=1)
        if wildcard:
            return date.strftime('*{sep}%m{sep}%Y{sep}'.format(sep=self._sep))
        return date.strftime('%m{sep}%Y'.format(sep=self._sep))

    def fmt_day(self, year, month, day):
        """
        Format and returns day in little-endian order style.

        :param int year: Year
        :param int month: Month
        :param int day: Day
        :rtype: str
        """
        date = datetime.date(year, month, day)
        return date.strftime('%d{sep}%m{sep}%Y'.format(sep=self._sep))


class MiddleEndianDateFormatter(DateFormatter):
    """
    In this format the month data item is written before day before year.

    (month, day, year), e.g. 04-22-2018 or 04.22.2018 or 04/22/2018
    """

    def fmt_year(self, year, wildcard=False):
        """
        Format and returns year in middle-endian order style.

        :param int year: Year
        :param bool wildcard: Use wildcard instead day and month
        :rtype: str
        """
        date = datetime.date(year=year, month=1, day=1)
        if wildcard:
            return date.strftime('*{sep}%Y'.format(sep=self._sep))
        return date.strftime('%Y')

    def fmt_month(self, year, month, wildcard=False):
        """
        Format and returns month in middle-endian order style.

        :param int year: Year
        :param int month: Month
        :param bool wildcard: Use wildcard instead day
        :rtype: str
        """
        date = datetime.date(year=year, month=month, day=1)
        if wildcard:
            return date.strftime('%m{sep}*{sep}%Y'.format(sep=self._sep))
        return date.strftime('%m{sep}%Y'.format(sep=self._sep))

    def fmt_day(self, year, month, day):
        """
        Format and returns day in middle-endian order style.

        :param int year: Year
        :param int month: Month
        :param int day: Day
        :rtype: str
        """
        date = datetime.date(year, month, day)
        return date.strftime('%m{sep}%d{sep}%Y'.format(sep=self._sep))
