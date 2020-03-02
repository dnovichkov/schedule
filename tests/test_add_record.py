import datetime

import pytest
from datetimerange import DateTimeRange

from schedule.schedule import Schedule


def test_simple_add():
    start_datetime = datetime.datetime(year=2020, month=1, day=1)
    schedule = Schedule(start_datetime, duration=3600)

    _range = DateTimeRange(
        start_datetime, start_datetime + datetime.timedelta(minutes=1))
    schedule.add_record('Test_type', _range)
    assert len(schedule.records) == 1
