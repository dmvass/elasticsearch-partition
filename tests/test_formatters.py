import unittest

from elasticsearch_partition import formatters


class TestBigEndianDateFormatter(unittest.TestCase):

    def setUp(self):
        self.module = formatters.BigEndianDateFormatter
        self.formatter = self.module()

    def test_fmt_year(self):
        # Test without wildcard
        actual = self.formatter.fmt_year(2018, wildcard=False)
        self.assertEqual(actual, "2018")
        # Test with wildcard
        actual = self.formatter.fmt_year(2018, wildcard=True)
        self.assertEqual(actual, "2018-*")

    def test_fmt_month(self):
        # Test without wildcard
        actual = self.formatter.fmt_month(2018, 4, wildcard=False)
        self.assertEqual(actual, "2018-04")
        # Test with wildcard
        actual = self.formatter.fmt_month(2018, 4, wildcard=True)
        self.assertEqual(actual, "2018-04-*")

    def test_fmt_day(self):
        actual = self.formatter.fmt_day(2018, 4, 20)
        self.assertEqual(actual, "2018-04-20")

    def test_sep(self):
        formatter = self.module(sep=".")
        actual_year = formatter.fmt_year(2018, wildcard=False)
        actual_month = formatter.fmt_month(2018, 4, wildcard=False)
        actual_day = formatter.fmt_day(2018, 4, 20)
        self.assertEqual(actual_year, "2018")
        self.assertEqual(actual_month, "2018.04")
        self.assertEqual(actual_day, "2018.04.20")

        for sep in formatters.INVALID_SEP_CHARS:
            with self.assertRaises(ValueError):
                self.module(sep)


class TestLittleEndianDateFormatter(unittest.TestCase):

    def setUp(self):
        self.module = formatters.LittleEndianDateFormatter
        self.formatter = self.module()

    def test_fmt_year(self):
        # Test without wildcard
        actual = self.formatter.fmt_year(2018, wildcard=False)
        self.assertEqual(actual, "2018")
        # Test with wildcard
        actual = self.formatter.fmt_year(2018, wildcard=True)
        self.assertEqual(actual, "*-2018")

    def test_fmt_month(self):
        # Test without wildcard
        actual = self.formatter.fmt_month(2018, 4, wildcard=False)
        self.assertEqual(actual, "04-2018")
        # Test with wildcard
        actual = self.formatter.fmt_month(2018, 4, wildcard=True)
        self.assertEqual(actual, "*-04-2018")

    def test_fmt_day(self):
        actual = self.formatter.fmt_day(2018, 4, 20)
        self.assertEqual(actual, "20-04-2018")

    def test_sep(self):
        formatter = self.module(sep=".")
        actual_year = formatter.fmt_year(2018, wildcard=False)
        actual_month = formatter.fmt_month(2018, 4, wildcard=False)
        actual_day = formatter.fmt_day(2018, 4, 20)
        self.assertEqual(actual_year, "2018")
        self.assertEqual(actual_month, "04.2018")
        self.assertEqual(actual_day, "20.04.2018")

        for sep in formatters.INVALID_SEP_CHARS:
            with self.assertRaises(ValueError):
                self.module(sep)


class TestMiddleEndianDateFormatter(unittest.TestCase):

    def setUp(self):
        self.module = formatters.MiddleEndianDateFormatter
        self.formatter = self.module()

    def test_fmt_year(self):
        # Test without wildcard
        actual = self.formatter.fmt_year(2018, wildcard=False)
        self.assertEqual(actual, "2018")
        # Test with wildcard
        actual = self.formatter.fmt_year(2018, wildcard=True)
        self.assertEqual(actual, "*-2018")

    def test_fmt_month(self):
        # Test without wildcard
        actual = self.formatter.fmt_month(2018, 4, wildcard=False)
        self.assertEqual(actual, "04-2018")
        # Test with wildcard
        actual = self.formatter.fmt_month(2018, 4, wildcard=True)
        self.assertEqual(actual, "04-*-2018")

    def test_fmt_day(self):
        actual = self.formatter.fmt_day(2018, 4, 20)
        self.assertEqual(actual, "04-20-2018")

    def test_sep(self):
        formatter = self.module(sep=".")
        actual_year = formatter.fmt_year(2018, wildcard=False)
        actual_month = formatter.fmt_month(2018, 4, wildcard=False)
        actual_day = formatter.fmt_day(2018, 4, 20)
        self.assertEqual(actual_year, "2018")
        self.assertEqual(actual_month, "04.2018")
        self.assertEqual(actual_day, "04.20.2018")

        for sep in formatters.INVALID_SEP_CHARS:
            with self.assertRaises(ValueError):
                self.module(sep)


if __name__ == "__main__":
    unittest.main()
