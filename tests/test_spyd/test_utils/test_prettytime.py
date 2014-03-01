import unittest

from spyd.utils.prettytime import createDurationString, shortDurationString


MINUTE = 60
HOUR = 60 * MINUTE
DAY = 24 * HOUR
YEAR = 365 * DAY

class TestPrettyTime(unittest.TestCase):
    def test_duration_0sec(self):
        self.assertEqual(createDurationString(0), '0 seconds')

    def test_duration_1sec(self):
        self.assertEqual(createDurationString(1), '1 second')

    def test_duration_2sec(self):
        self.assertEqual(createDurationString(2), '2 seconds')

    def test_duration_59sec(self):
        self.assertEqual(createDurationString(59), '59 seconds')

    def test_duration_60sec(self):
        self.assertEqual(createDurationString(60), '1 minute')

    def test_duration_61sec(self):
        self.assertEqual(createDurationString(61), '1 minute, and 1 second')

    def test_duration_2min_1sec(self):
        self.assertEqual(createDurationString(121), '2 minutes, and 1 second')

    def test_duration_2hour_9sec(self):
        self.assertEqual(createDurationString(2 * HOUR + 9), '2 hours, and 9 seconds')

    def test_duration_1year_1day_1hour_1min(self):
        self.assertEqual(createDurationString(YEAR + DAY + HOUR + MINUTE), '1 year, 1 day, 1 hour, and 1 minute')

    def test_duration_5year_4day_3hour_2min(self):
        self.assertEqual(createDurationString(5 * YEAR + 4 * DAY + 3 * HOUR + 2 * MINUTE), '5 years, 4 days, 3 hours, and 2 minutes')

    def test_short_duration_0sec(self):
        self.assertEqual(shortDurationString(0), '0s')

    def test_short_duration_1sec(self):
        self.assertEqual(shortDurationString(1), '1s')

    def test_short_duration_2sec(self):
        self.assertEqual(shortDurationString(2), '2s')

    def test_short_duration_59sec(self):
        self.assertEqual(shortDurationString(59), '59s')

    def test_short_duration_60sec(self):
        self.assertEqual(shortDurationString(60), '1m')

    def test_short_duration_61sec(self):
        self.assertEqual(shortDurationString(61), '1m 1s')

    def test_short_duration_2min_1sec(self):
        self.assertEqual(shortDurationString(121), '2m 1s')

    def test_short_duration_2hour_9sec(self):
        self.assertEqual(shortDurationString(2 * HOUR + 9), '2h 9s')

    def test_short_duration_1year_1day_1hour_1min(self):
        self.assertEqual(shortDurationString(YEAR + DAY + HOUR + MINUTE), '1y 1d 1h 1m')

    def test_short_duration_5year_4day_3hour_2min(self):
        self.assertEqual(shortDurationString(5 * YEAR + 4 * DAY + 3 * HOUR + 2 * MINUTE), '5y 4d 3h 2m')
