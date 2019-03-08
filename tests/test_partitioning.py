import datetime
import unittest

from elasticsearch_partition import formatters, partitioning


class _PyDateFormatter(formatters.DateFormatter):

    def fmt_year(self, year, wildcard):
        date = datetime.date(year=year, month=1, day=1)
        if wildcard:
            return date.strftime("%Y{sep}*".format(sep=self.sep))
        return date.strftime("%Y")

    def fmt_month(self, year, month, wildcard):
        date = datetime.date(year=year, month=month, day=1)
        if wildcard:
            return date.strftime("%Y{sep}%m{sep}*".format(sep=self.sep))
        return date.strftime("%Y{sep}%m".format(sep=self.sep))

    def fmt_day(self, year, month, day):
        date = datetime.date(year, month, day)
        return date.strftime("%Y{sep}%m{sep}%d".format(sep=self.sep))


class TestRangePartition(unittest.TestCase):

    def setUp(self):
        self.cls = partitioning.RangePartition
        self.since = datetime.date(2014, 9, 27)
        self.until = datetime.date(2018, 2, 4)

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
        partition = self.cls(
            frequency=partitioning.DAY,
            now_func=lambda: datetime.date(2018, 7, 4)
        )
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
        partition = self.cls(
            frequency=partitioning.DAY,
            now_func=lambda: datetime.date(2018, 7, 4)
        )
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
        partition = self.cls(
            frequency=partitioning.MONTH,
            now_func=lambda: datetime.date(2018, 7, 4)
        )
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
        partition = self.cls(
            frequency=partitioning.MONTH,
            now_func=lambda: datetime.date(2018, 7, 4)
        )
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
        partition = self.cls(
            frequency=partitioning.YEAR,
            now_func=lambda: datetime.date(2018, 7, 4)
        )
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
        partition = self.cls(
            frequency=partitioning.YEAR,
            now_func=lambda: datetime.date(2018, 7, 4)
        )
        expected = ["logs-*"]
        actual = partition("logs-*", until=self.until)
        self.assertListEqual(actual, expected)

    def test_custom_partition(self):
        partition = self.cls(
            frequency=partitioning.DAY,
            formatter=formatters.MiddleEndianDateFormatter(),
            escape="@"
        )
        expected = [
            "logs-09-27-2014",
            "logs-09-28-2014",
            "logs-09-29-2014",
            "logs-09-30-2014",
            "logs-10-*-2014",
            "logs-11-*-2014",
            "logs-12-*-2014",
            "logs-*-2015",
            "logs-*-2016",
            "logs-*-2017",
            "logs-01-*-2018",
            "logs-02-01-2018",
            "logs-02-02-2018",
            "logs-02-03-2018",
            "logs-02-04-2018",
        ]
        actual = partition("logs-@", self.since, self.until)
        self.assertListEqual(actual, expected)

    def test_partition_with_py_formatter(self):
        partition = self.cls(
            frequency=partitioning.DAY,
            formatter=_PyDateFormatter(),
        )
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


if __name__ == "__main__":
    unittest.main()
