cdef class DateFormatter:
    cdef readonly str sep
    cdef char c_sep

    cpdef str fmt_year(self, int year, bint wildcard)
    cpdef str fmt_month(self, int year, int month, bint wildcard)
    cpdef str fmt_day(self, int year, int month, int day)


cdef class BigEndianDateFormatter(DateFormatter):
    cpdef str fmt_year(self, int year, bint wildcard)
    cpdef str fmt_month(self, int year, int month, bint wildcard)
    cpdef str fmt_day(self, int year, int month, int day)


cdef class LittleEndianDateFormatter(DateFormatter):
    cpdef str fmt_year(self, int year, bint wildcard)
    cpdef str fmt_month(self, int year, int month, bint wildcard)
    cpdef str fmt_day(self, int year, int month, int day)


cdef class MiddleEndianDateFormatter(DateFormatter):
    cpdef str fmt_year(self, int year, bint wildcard)
    cpdef str fmt_month(self, int year, int month, bint wildcard)
    cpdef str fmt_day(self, int year, int month, int day)
