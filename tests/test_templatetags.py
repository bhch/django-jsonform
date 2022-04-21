from unittest import TestCase
from datetime import datetime, date, time
from django_jsonform.templatetags.django_jsonform import parse_datetime, parse_time


class ParseDatetimeFilterTests(TestCase):
    def test_datetime_string_is_converted_to_datetime_object(self):
        now = datetime.now()
        now_iso = now.isoformat()

        parsed = parse_datetime(now_iso)

        self.assertTrue(isinstance(parsed, datetime))
        self.assertEqual(parsed, now)


    def test_date_string_is_converted_to_datetime_object(self):
        self.assertTrue(isinstance(parse_datetime('2022-04-21'), datetime))


class ParseTimeFilterTests(TestCase):
    def test_time_string_is_converted_to_time_object(self):
        self.assertTrue(isinstance(parse_time('10:10:00'), time))
