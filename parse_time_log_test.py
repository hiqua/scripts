#!/usr/bin/env python3
import unittest
from datetime import datetime
from datetime import timedelta
import parse_time_log

class TestParsetime(unittest.TestCase):
  def test_within_threshold_true(self):
    d1 = datetime.fromisoformat('2023-12-01T01:10+01:00')
    d2 = datetime.fromisoformat('2023-12-01T01:19+01:00')

    self.assertTrue(parse_time_log.within_threshold(d1,d2, threshold=
            timedelta(minutes=10)))

  def test_within_threshold_false(self):
    d1 = datetime.fromisoformat('2023-12-01T01:10+01:00')
    d2 = datetime.fromisoformat('2023-12-01T01:29+01:00')

    self.assertFalse(parse_time_log.within_threshold(d1,d2, threshold=
            timedelta(minutes=10)))

if __name__ == '__main__':
  unittest.main()
