import unittest

from elasticsearch_partition import formatters


class TestBigEndianDateFormatter(unittest.TestCase):

    def setUp(self):
        self.formatter = formatters.BigEndianDateFormatter()

    def test_fmt_year(self):
        # Test without wildcard
        actual = self.formatter.fmt_year(2018)
        self.assertEqual(actual, '2018')
        # Test with wildcard
        actual = self.formatter.fmt_year(2018, wildcard=True)
        self.assertEqual(actual, '2018-*')

    def test_fmt_month(self):
        # Test without wildcard
        actual = self.formatter.fmt_month(2018, 4)
        self.assertEqual(actual, '2018-04')
        # Test with wildcard
        actual = self.formatter.fmt_month(2018, 4, wildcard=True)
        self.assertEqual(actual, '2018-04-*')

    def test_fmt_day(self):
        actual = self.formatter.fmt_day(2018, 4, 20)
        self.assertEqual(actual, '2018-04-20')

    def test_sep(self):
        formatter = formatters.BigEndianDateFormatter(sep='.')
        actual_year = formatter.fmt_year(2018)
        actual_month = formatter.fmt_month(2018, 4)
        actual_day = formatter.fmt_day(2018, 4, 20)
        self.assertEqual(actual_year, '2018')
        self.assertEqual(actual_month, '2018.04')
        self.assertEqual(actual_day, '2018.04.20')


class TestLittleEndianDateFormatter(unittest.TestCase):

    def setUp(self):
        self.formatter = formatters.LittleEndianDateFormatter()

    def test_fmt_year(self):
        # Test without wildcard
        actual = self.formatter.fmt_year(2018)
        self.assertEqual(actual, '2018')
        # Test with wildcard

    def test_fmt_month(self):
        # Test without wildcard
        actual = self.formatter.fmt_month(2018, 4)
        self.assertEqual(actual, '04-2018')
        # Test with wildcard

    def test_fmt_day(self):
        actual = self.formatter.fmt_day(2018, 4, 20)
        self.assertEqual(actual, '20-04-2018')

    def test_sep(self):
        formatter = formatters.LittleEndianDateFormatter(sep='.')
        actual_year = formatter.fmt_year(2018)
        actual_month = formatter.fmt_month(2018, 4)
        actual_day = formatter.fmt_day(2018, 4, 20)
        self.assertEqual(actual_year, '2018')
        self.assertEqual(actual_month, '04.2018')
        self.assertEqual(actual_day, '20.04.2018')


class TestMiddleEndianDateFormatter(unittest.TestCase):

    def setUp(self):
        self.formatter = formatters.MiddleEndianDateFormatter()

    def test_fmt_year(self):
        # Test without wildcard
        actual = self.formatter.fmt_year(2018)
        self.assertEqual(actual, '2018')
        # Test with wildcard
        actual = self.formatter.fmt_year(2018, wildcard=True)
        self.assertEqual(actual, '*-2018')

    def test_fmt_month(self):
        # Test without wildcard
        actual = self.formatter.fmt_month(2018, 4)
        self.assertEqual(actual, '04-2018')
        # Test with wildcard
        actual = self.formatter.fmt_month(2018, 4, wildcard=True)
        self.assertEqual(actual, '04-*-2018')

    def test_fmt_day(self):
        actual = self.formatter.fmt_day(2018, 4, 20)
        self.assertEqual(actual, '04-20-2018')

    def test_sep(self):
        formatter = formatters.MiddleEndianDateFormatter(sep='.')
        actual_year = formatter.fmt_year(2018)
        actual_month = formatter.fmt_month(2018, 4)
        actual_day = formatter.fmt_day(2018, 4, 20)
        self.assertEqual(actual_year, '2018')
        self.assertEqual(actual_month, '04.2018')
        self.assertEqual(actual_day, '04.20.2018')


if __name__ == '__main__':
    unittest.main()
