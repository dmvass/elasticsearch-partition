cdef enum FREQUENCY:
    YEAR = 1
    MONTH = 2
    DAY = 3

ctypedef struct date_t:
    int year
    int month
    int day

cdef int monthrange(int year, int month) except -1

cdef int compare_date(date_t *date1, date_t *date2)

cdef class TimeWindow:
    cdef:
        int size
        int delta_years
        date_t since, until
        date_t* data_ptr

    cdef void incr_year(self, date_t *date)
    cdef void incr_month(self, date_t *date)
    cdef void incr_day(self, date_t *date)

    cdef void calculate_yearly(self, date_t *date)
    cdef void calculate_monthly(self, date_t *date)
    cdef void calculate_daily(self, date_t *date)

    cdef void calculate(self, int frequency)
