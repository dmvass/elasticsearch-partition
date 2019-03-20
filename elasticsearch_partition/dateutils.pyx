import datetime
from libc.stdlib cimport malloc, free

cimport cython


DEF MAXMONTH = 12
DEF FEBRUARY = 2
DEF MIN_MONTH_DAYS = 28

DEF BUFFER_SIZE = 256

cdef int *month_days = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


@cython.cdivision(True)
cdef int monthrange(int year, int month) except -1:
    """Returns number of days (28-31) for year, month."""
    cdef bint isleap

    if not 1 <= month <= MAXMONTH:
        return -1

    isleap = (year % 4 == 0 and (year % 100 != 0 or year % 400 == 0))
    return month_days[month] + (month == FEBRUARY and isleap)


cdef int compare_date(date_t *date1, date_t *date2):
    cdef int res

    # Perform comparison
    if date1.year < date2.year:
        res = -1
    elif date1.year > date2.year:
        res = 1
    elif date1.month < date2.month:
        res = -1
    elif date1.month > date2.month:
        res = 1
    elif date1.day < date2.day:
        res = -1
    elif date1.day > date2.day:
        res = 1
    else:
        res = 0

    return res


cdef class TimeWindow:
    """Custom data container for allocating memory and calculating time
    window dates with the specified frequency. Allocated memory will be
    free when all Python references to the object are gone.

    """

    def __cinit__(self, since, until):
        if not isinstance(since, datetime.date):
            raise TypeError("The 'since' parameter must be a 'date' type")

        if not isinstance(until, datetime.date):
            raise TypeError("The 'until' parameter must be a 'date' type")

        if since > until:
            raise ValueError("'since' can't be more than 'until'")

        self.since = date_t(since.year, since.month, since.day)
        self.until = date_t(until.year, until.month, until.day)
        self.delta_years = self.until.year - self.since.year

        self.data_ptr = <date_t *> malloc(BUFFER_SIZE * sizeof(date_t))
        if self.data_ptr == NULL:
            raise MemoryError()

    cdef void incr_year(self, date_t *date):
        date.month = date.day = 1
        date.year += 1

    cdef void incr_month(self, date_t *date):
        if date.month == MAXMONTH:
            self.incr_year(date)
        else:
            date.day = 1
            date.month += 1

    cdef void incr_day(self, date_t *date):
        if (date.day >= MIN_MONTH_DAYS and
                date.day == monthrange(date.year, date.month)):
            self.incr_month(date)
        else:
            date.day += 1

    cdef void calculate_yearly(self, date_t *date):
        self.incr_year(date)

    cdef void calculate_monthly(self, date_t *date):
        if date.year == self.since.year or date.year == self.until.year:
            self.incr_month(date)
        else:
            self.incr_year(date)

    cdef void calculate_daily(self, date_t *date):
        if date.year == self.since.year and date.month == self.since.month:
            self.incr_day(date)
        elif date.year == self.until.year and date.month == self.until.month:
            self.incr_day(date)
        elif date.year == self.since.year or date.year == self.until.year:
            self.incr_month(date)
        else:
            self.incr_year(date)

    cdef void calculate(self, int frequency):
        """Calculate dates with specified frequency."""

        cdef date_t date = self.since
        cdef void (*func_ptr)(TimeWindow, date_t *)

        # Defines the frequency calculate function
        if frequency == FREQUENCY.YEAR:
            func_ptr = self.calculate_yearly
        elif frequency == FREQUENCY.MONTH:
            func_ptr = self.calculate_monthly
        else:
            func_ptr = self.calculate_daily

        while compare_date(&date, &self.until) != 1:
            self.data_ptr[self.size] = date
            self.size += 1

            func_ptr(self, &date)

    def __dealloc__(self):
        """Frees the array. This is called by Python when all
        references to the object are gone.

        """
        free(self.data_ptr)
