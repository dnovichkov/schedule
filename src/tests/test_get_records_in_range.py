import datetime

from datetimerange import DateTimeRange
from schedule.schedule import Schedule


def test_get_records_empty_schedule():
    start_datetime = datetime.datetime(year=2020, month=1, day=1)
    schedule = Schedule(start_datetime, duration=3600)

    _range = DateTimeRange(
        start_datetime, start_datetime + datetime.timedelta(minutes=1))
    records = schedule.get_records_in_range(_range)
    assert records == []


def test_get_records_true_range():
    start_datetime = datetime.datetime(year=2020, month=1, day=1)
    schedule = Schedule(start_datetime, duration=3600)

    range_1 = DateTimeRange(
        start_datetime, start_datetime + datetime.timedelta(minutes=1))
    schedule.add_record('TYPE_1', range_1)

    range_2 = DateTimeRange(
        start_datetime + datetime.timedelta(minutes=1), start_datetime + datetime.timedelta(minutes=2))
    schedule.add_record('TYPE_1', range_2)

    assert len(schedule.records) == 2

    required_range = DateTimeRange(
        start_datetime, start_datetime + datetime.timedelta(minutes=2))

    records = schedule.get_records_in_range(required_range)
    assert len(records) == 2

    required_range = DateTimeRange(
        start_datetime + datetime.timedelta(minutes=1), start_datetime + datetime.timedelta(minutes=2))
    records = schedule.get_records_in_range(required_range)
    assert len(records) == 1


def test_get_records_wrong_range():
    start_datetime = datetime.datetime(year=2020, month=1, day=1)
    schedule = Schedule(start_datetime, duration=3600)

    range_1 = DateTimeRange(
        start_datetime, start_datetime + datetime.timedelta(minutes=1))
    schedule.add_record('TYPE_1', range_1)

    range_2 = DateTimeRange(
        start_datetime + datetime.timedelta(minutes=1), start_datetime + datetime.timedelta(minutes=2))
    schedule.add_record('TYPE_1', range_2)

    assert len(schedule.records) == 2

    required_range = DateTimeRange(
        start_datetime + datetime.timedelta(minutes=3), start_datetime + datetime.timedelta(minutes=4))

    records = schedule.get_records_in_range(required_range)
    assert len(records) == 0

    required_range = DateTimeRange(
        start_datetime + datetime.timedelta(minutes=2), start_datetime + datetime.timedelta(minutes=3))
    records = schedule.get_records_in_range(required_range)
    assert len(records) == 0
