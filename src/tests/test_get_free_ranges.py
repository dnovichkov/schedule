import copy
import datetime
import logging

from datetimerange import DateTimeRange
from schedule.schedule import Schedule


def test_get_ranges_without_duration():
    start_datetime = datetime.datetime(year=2020, month=1, day=1)
    end_datetime = start_datetime + datetime.timedelta(hours=1)
    schedule = Schedule(start_datetime, end_dt=end_datetime)

    assert [DateTimeRange(start_datetime, end_datetime)
            ] == schedule.get_free_ranges(3600)
    assert [] == schedule.get_free_ranges(7200)

    range_1 = DateTimeRange(
        start_datetime, start_datetime + datetime.timedelta(minutes=1))
    assert schedule.add_record('SOME TYPE', range_1)
    assert [] == schedule.get_free_ranges(7200)
    assert [DateTimeRange(range_1.end_datetime, end_datetime)
            ] == schedule.get_free_ranges()

    range_2 = DateTimeRange(start_datetime + datetime.timedelta(minutes=10),
                            start_datetime + datetime.timedelta(minutes=11))
    assert schedule.add_record('SOME TYPE', range_2)

    expected_free_ranges = \
        [
            DateTimeRange(range_1.end_datetime, range_2.start_datetime),
            DateTimeRange(range_2.end_datetime, end_datetime),
        ]
    assert expected_free_ranges == schedule.get_free_ranges()

    range_3 = DateTimeRange(start_datetime + datetime.timedelta(minutes=50),
                            end_datetime)
    assert schedule.add_record('SOME TYPE', range_3)

    expected_free_ranges = \
        [
            DateTimeRange(range_1.end_datetime, range_2.start_datetime),
            DateTimeRange(range_2.end_datetime, range_3.start_datetime),
        ]
    assert expected_free_ranges == schedule.get_free_ranges()


def test_get_ranges_with_duration():
    start_datetime = datetime.datetime(year=2020, month=1, day=1)
    end_datetime = start_datetime + datetime.timedelta(hours=1)
    schedule = Schedule(start_datetime, end_dt=end_datetime)

    assert [DateTimeRange(start_datetime, end_datetime)
            ] == schedule.get_free_ranges(3600)
    assert [] == schedule.get_free_ranges(7200)

    range_1 = DateTimeRange(
        start_datetime, start_datetime + datetime.timedelta(minutes=1))
    assert schedule.add_record('SOME TYPE', range_1)
    assert [] == schedule.get_free_ranges(7200)
    assert [DateTimeRange(range_1.end_datetime, end_datetime)
            ] == schedule.get_free_ranges(50 * 60)
    assert [DateTimeRange(range_1.end_datetime, end_datetime)
            ] == schedule.get_free_ranges(59 * 60)
    assert [] == schedule.get_free_ranges(60 * 60)
    assert [] == schedule.get_free_ranges(120 * 60)

    range_2 = DateTimeRange(start_datetime + datetime.timedelta(minutes=10),
                            start_datetime + datetime.timedelta(minutes=11))
    assert schedule.add_record('SOME TYPE', range_2)

    expected_free_ranges = \
        [
            DateTimeRange(range_1.end_datetime, range_2.start_datetime),
            DateTimeRange(range_2.end_datetime, end_datetime),
        ]
    assert expected_free_ranges == schedule.get_free_ranges(1 * 60)
    assert expected_free_ranges == schedule.get_free_ranges(5 * 60)
    assert expected_free_ranges == schedule.get_free_ranges(9 * 60)
    assert [DateTimeRange(range_2.end_datetime, end_datetime)
            ] == schedule.get_free_ranges(10 * 60)
    assert [] == schedule.get_free_ranges(50 * 60)

    range_3 = DateTimeRange(start_datetime + datetime.timedelta(minutes=50),
                            end_datetime)
    assert schedule.add_record('SOME TYPE', range_3)

    expected_free_ranges = \
        [
            DateTimeRange(range_1.end_datetime, range_2.start_datetime),
            DateTimeRange(range_2.end_datetime, range_3.start_datetime),
        ]
    assert expected_free_ranges == schedule.get_free_ranges(1 * 60)
    assert expected_free_ranges == schedule.get_free_ranges(9 * 60)
    assert expected_free_ranges[1:] == schedule.get_free_ranges(10 * 60)
    assert expected_free_ranges[1:] == schedule.get_free_ranges(39 * 60)
    assert [] == schedule.get_free_ranges(40 * 60)
