# cython: c_string_type=str, c_string_encoding=ascii

from libc.stdio cimport sprintf


DEF MAX_DATE_LENGTH = 11

INVALID_SEP_CHARS = ("\\", "/", "*", "?", "\"", "<", ">", "|", " ", ",")


cdef class DateFormatter:
    """Abstract date formatter class"""

    def __init__(self, str sep="-"):
        """Accepts separation character and initialize specified
        date formatter.

        """
        if sep in INVALID_SEP_CHARS:
            raise ValueError(
                "The separation character '%s' is not valid" % sep
            )
        self.sep = sep
        self.c_sep = <char> ord(sep)

    cpdef str fmt_year(self, int year, bint wildcard):
        """Format and returns year in specified order style.

        :param int year: year value
        :param bool wildcard: use wildcard instead day and month
        :rtype: str

        """
        pass

    cpdef str fmt_month(self, int year, int month, bint wildcard):
        """Format and returns month in specified order style.

        :param int year: year value
        :param int month: month value
        :param bool wildcard: use wildcard instead day
        :rtype: str

        """
        pass

    cpdef str fmt_day(self, int year, int month, int day):
        """Format and returns day in specified order style.

        :param int year: year value
        :param int month: month value
        :param int day: day value
        :rtype: str

        """
        pass


cdef class BigEndianDateFormatter(DateFormatter):
    """In this format the most significant data item is written before
    lesser data items i.e. year before month before day.

    (year, month, day), e.g. 2018-04-22 or 2018.04.22 or 2018/04/22

    """

    cpdef str fmt_year(self, int year, bint wildcard):
        cdef char date[MAX_DATE_LENGTH]

        if wildcard:
            sprintf(date, "%d%c*", year, self.c_sep)
        else:
            sprintf(date, "%d", year, self.c_sep)

        return date

    cpdef str fmt_month(self, int year, int month, bint wildcard):
        cdef char date[MAX_DATE_LENGTH]

        if wildcard:
            sprintf(date, "%d%c%02d%c*", year, self.c_sep, month, self.c_sep)
        else:
            sprintf(date, "%d%c%02d", year, self.c_sep, month)

        return date

    cpdef str fmt_day(self, int year, int month, int day):
        cdef char date[MAX_DATE_LENGTH]

        sprintf(date, "%d%c%02d%c%02d", year, self.c_sep,
                month, self.c_sep, day)
        return date


cdef class LittleEndianDateFormatter(DateFormatter):
    """In this format the most significant data item is written after
    lesser data items i.e. day before month before year.

    (day, month, year), e.g. 22-04-2018 or 22.04.2018 or 22/04/2018

    """

    cpdef str fmt_year(self, int year, bint wildcard):
        cdef char date[MAX_DATE_LENGTH]

        if wildcard:
            sprintf(date, "*%c%d", self.c_sep, year)
        else:
            sprintf(date, "%d", year, self.c_sep)

        return date

    cpdef str fmt_month(self, int year, int month, bint wildcard):
        cdef char date[MAX_DATE_LENGTH]

        if wildcard:
            sprintf(date, "*%c%02d%c%d", self.c_sep, month, self.c_sep, year)
        else:
            sprintf(date, "%02d%c%d", month, self.c_sep, year)

        return date

    cpdef str fmt_day(self, int year, int month, int day):
        cdef char date[MAX_DATE_LENGTH]

        sprintf(date, "%02d%c%02d%c%d", day, self.c_sep,
                month, self.c_sep, year)
        return date


cdef class MiddleEndianDateFormatter(DateFormatter):
    """In this format the month data item is written before day before year.

    (month, day, year), e.g. 04-22-2018 or 04.22.2018 or 04/22/2018

    """

    cpdef str fmt_year(self, int year, bint wildcard):
        cdef char date[MAX_DATE_LENGTH]

        if wildcard:
            sprintf(date, "*%c%d", self.c_sep, year)
        else:
            sprintf(date, "%d", year, self.c_sep)

        return date

    cpdef str fmt_month(self, int year, int month, bint wildcard):
        cdef char date[MAX_DATE_LENGTH]

        if wildcard:
            sprintf(date, "%02d%c*%c%d", month, self.c_sep, self.c_sep, year)
        else:
            sprintf(date, "%02d%c%d", month, self.c_sep, year)

        return date

    cpdef str fmt_day(self, int year, int month, int day):
        cdef char date[MAX_DATE_LENGTH]

        sprintf(date, "%02d%c%02d%c%d", month, self.c_sep,
                day, self.c_sep, year)
        return date
