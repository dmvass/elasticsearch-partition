import datetime
import unittest

from elasticsearch_partition import formatters, partitioning


class TestTimeWindow(unittest.TestCase):

    def setUp(self):
        self.tm = partitioning.TimeWindow
        self.since = datetime.date(2018, 5, 8)
        self.until = datetime.date(2018, 6, 10)

    def test_init(self):
        # Test with wrong since type
        with self.assertRaises(TypeError):
            self.tm("42", self.until)

        # Test with wrong until type
        with self.assertRaises(TypeError):
            self.tm(self.since, "42")

        # Test with since more than until
        with self.assertRaises(ValueError):
            self.tm(self.until, self.since)

        # Test succes initialization
        instance = self.tm(self.since, self.until)
        self.assertEqual(instance.since, self.since)
        self.assertEqual(instance.until, self.until)

    def test_delta_years(self):
        instance = self.tm(
            datetime.date(2015, 5, 8),
            datetime.date(2018, 6, 10)
        )
        self.assertEqual(instance.delta_years, 3)

    def test_delta_days(self):
        instance = self.tm(self.since, self.until)
        expected = (self.until - self.since).days
        self.assertEqual(instance.delta_days, expected)

    def test_iteration(self):
        instance = self.tm(self.since, self.until)
        actual = len(list(instance))
        expected = (self.until - self.since).days + 1
        self.assertEqual(actual, expected)


class TestRangePartitioning(unittest.TestCase):

    def setUp(self):
        self.cls = partitioning.RangePartitioning
        self.since = datetime.date(2014, 9, 27)
        self.until = datetime.date(2018, 2, 4)

    def test_init(self):
        # Test with wrong formatter class
        with self.assertRaises(TypeError):
            self.cls(formatter=list)

    def test_init_default(self):
        instance = self.cls()
        self.assertEqual(instance._frequency, partitioning.DAY)
        self.assertIsInstance(
            instance._formatter,
            formatters.BigEndianDateFormatter
        )
        self.assertEqual(instance._escape, "*")

    def test_init_custom(self):

        def test_now():
            pass

        instance = self.cls(
            frequency=partitioning.MONTH,
            formatter=formatters.LittleEndianDateFormatter(),
            escape="@",
            now_func=test_now
        )
        self.assertEqual(instance._frequency, partitioning.MONTH)
        self.assertIsInstance(
            instance._formatter,
            formatters.LittleEndianDateFormatter
        )
        self.assertEqual(instance._escape, "@")
        self.assertEqual(instance._now_func, test_now)

    def test_partition_by_day(self):
        partition = self.cls(frequency=partitioning.DAY)
        expected = [
            "logs-2014-09-27",
            "logs-2014-09-28",
            "logs-2014-09-29",
            "logs-2014-09-30",
            "logs-2014-10-*",
            "logs-2014-11-*",
            "logs-2014-12-*",
            "logs-2015-*",
            "logs-2016-*",
            "logs-2017-*",
            "logs-2018-01-*",
            "logs-2018-02-01",
            "logs-2018-02-02",
            "logs-2018-02-03",
            "logs-2018-02-04",
        ]
        actual = partition("logs-*", self.since, self.until)
        self.assertListEqual(actual, expected)

    def test_partition_by_day_only_since(self):
        partition = self.cls(frequency=partitioning.DAY)
        partition._now_func = lambda: datetime.date(2018, 7, 4)
        expected = [
            "logs-2014-09-27",
            "logs-2014-09-28",
            "logs-2014-09-29",
            "logs-2014-09-30",
            "logs-2014-10-*",
            "logs-2014-11-*",
            "logs-2014-12-*",
            "logs-2015-*",
            "logs-2016-*",
            "logs-2017-*",
            "logs-2018-01-*",
            "logs-2018-02-*",
            "logs-2018-03-*",
            "logs-2018-04-*",
            "logs-2018-05-*",
            "logs-2018-06-*",
            "logs-2018-07-01",
            "logs-2018-07-02",
            "logs-2018-07-03",
            "logs-2018-07-04",
        ]
        actual = partition("logs-*", self.since)
        self.assertSequenceEqual(actual, expected)

    def test_partition_by_day_only_until(self):
        partition = self.cls(frequency=partitioning.DAY)
        partition._now_func = lambda: datetime.date(2018, 7, 4)
        expected = [
            "-logs-2018-02-04",
            "-logs-2018-02-05",
            "-logs-2018-02-06",
            "-logs-2018-02-07",
            "-logs-2018-02-08",
            "-logs-2018-02-09",
            "-logs-2018-02-10",
            "-logs-2018-02-11",
            "-logs-2018-02-12",
            "-logs-2018-02-13",
            "-logs-2018-02-14",
            "-logs-2018-02-15",
            "-logs-2018-02-16",
            "-logs-2018-02-17",
            "-logs-2018-02-18",
            "-logs-2018-02-19",
            "-logs-2018-02-20",
            "-logs-2018-02-21",
            "-logs-2018-02-22",
            "-logs-2018-02-23",
            "-logs-2018-02-24",
            "-logs-2018-02-25",
            "-logs-2018-02-26",
            "-logs-2018-02-27",
            "-logs-2018-02-28",
            "-logs-2018-03-*",
            "-logs-2018-04-*",
            "-logs-2018-05-*",
            "-logs-2018-06-*",
            "-logs-2018-07-01",
            "-logs-2018-07-02",
            "-logs-2018-07-03",
            "-logs-2018-07-04",
            "logs-*"
        ]
        actual = partition("logs-*", until=self.until)
        self.assertSequenceEqual(actual, expected)

    def test_partition_by_month(self):
        partition = self.cls(frequency=partitioning.MONTH)
        expected = [
            "logs-2014-09",
            "logs-2014-10",
            "logs-2014-11",
            "logs-2014-12",
            "logs-2015-*",
            "logs-2016-*",
            "logs-2017-*",
            "logs-2018-01",
            "logs-2018-02",
        ]
        actual = partition("logs-*", self.since, self.until)
        self.assertListEqual(actual, expected)

    def test_partition_by_month_only_since(self):
        partition = self.cls(frequency=partitioning.MONTH)
        partition._now_func = lambda: datetime.date(2018, 7, 4)
        expected = [
            "logs-2014-09",
            "logs-2014-10",
            "logs-2014-11",
            "logs-2014-12",
            "logs-2015-*",
            "logs-2016-*",
            "logs-2017-*",
            "logs-2018-01",
            "logs-2018-02",
            "logs-2018-03",
            "logs-2018-04",
            "logs-2018-05",
            "logs-2018-06",
            "logs-2018-07",
        ]
        actual = partition("logs-*", self.since)
        self.assertListEqual(actual, expected)

    def test_partition_by_month_only_until(self):
        partition = self.cls(frequency=partitioning.MONTH)
        partition._now_func = lambda: datetime.date(2018, 7, 4)
        expected = [
            "-logs-2018-02",
            "-logs-2018-03",
            "-logs-2018-04",
            "-logs-2018-05",
            "-logs-2018-06",
            "-logs-2018-07",
            "logs-*"
        ]
        actual = partition("logs-*", until=self.until)
        self.assertListEqual(actual, expected)

    def test_partition_by_year(self):
        partition = self.cls(frequency=partitioning.YEAR)
        expected = [
            "logs-2014",
            "logs-2015",
            "logs-2016",
            "logs-2017",
            "logs-2018",
        ]
        actual = partition("logs-*", self.since, self.until)
        self.assertListEqual(actual, expected)

    def test_partition_by_year_only_since(self):
        partition = self.cls(frequency=partitioning.YEAR)
        partition._now_func = lambda: datetime.date(2018, 7, 4)
        expected = [
            "logs-2014",
            "logs-2015",
            "logs-2016",
            "logs-2017",
            "logs-2018",
        ]
        actual = partition("logs-*", self.since)
        self.assertListEqual(actual, expected)

    def test_partition_by_year_only_until(self):
        partition = self.cls(frequency=partitioning.YEAR)
        partition._now_func = lambda: datetime.date(2018, 7, 4)
        expected = ["logs-*"]
        actual = partition("logs-*", until=self.until)
        self.assertListEqual(actual, expected)
