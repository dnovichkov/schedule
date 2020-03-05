import datetime
import logging

import pytest
from datetimerange import DateTimeRange
from schedule.schedule import Schedule


def test_simple_add_to_schedule_duration():
    start_datetime = datetime.datetime(year=2020, month=1, day=1)
    schedule = Schedule(start_datetime, duration=3600)

    _range = DateTimeRange(
        start_datetime, start_datetime + datetime.timedelta(minutes=1))
    assert schedule.add_record('Test_type', _range)
    assert len(schedule.records) == 1

    _range = DateTimeRange(
        start_datetime + datetime.timedelta(minutes=1), start_datetime + datetime.timedelta(minutes=2))
    assert schedule.add_record('Test_type', _range)
    assert len(schedule.records) == 2


def test_simple_add_to_schedule_range():
    start_datetime = datetime.datetime(year=2020, month=1, day=1)
    end_datetime = start_datetime + datetime.timedelta(hours=1)
    schedule = Schedule(start_datetime, end_dt=end_datetime)

    _range = DateTimeRange(
        start_datetime, start_datetime + datetime.timedelta(minutes=1))
    assert schedule.add_record('Test_type', _range)
    assert len(schedule.records) == 1

    _range = DateTimeRange(
        start_datetime + datetime.timedelta(minutes=1), start_datetime + datetime.timedelta(minutes=2))
    assert schedule.add_record('Test_type', _range)
    assert len(schedule.records) == 2


def test_failed_add_to_schedule_range():
    start_datetime = datetime.datetime(year=2020, month=1, day=1)
    end_datetime = start_datetime + datetime.timedelta(hours=1)
    schedule = Schedule(start_datetime, duration=60)

    _range = DateTimeRange(
        start_datetime + datetime.timedelta(minutes=2), start_datetime + datetime.timedelta(minutes=3))
    assert not schedule.add_record('Test_type', _range)
    assert len(schedule.records) == 0

    _range = DateTimeRange(
        start_datetime + datetime.timedelta(minutes=1), start_datetime + datetime.timedelta(minutes=2))
    assert not schedule.add_record('Test_type', _range)
    assert len(schedule.records) == 0

    _range = DateTimeRange(
        start_datetime - datetime.timedelta(minutes=1), start_datetime + datetime.timedelta(minutes=2))
    assert not schedule.add_record('Test_type', _range)
    assert len(schedule.records) == 0


def test_simple_add_to_schedule_duration_and_range(caplog):
    caplog.set_level(logging.INFO)
    start_datetime = datetime.datetime(year=2020, month=1, day=1)
    end_datetime = start_datetime + datetime.timedelta(hours=1)

    schedule = Schedule(start_datetime, duration=7200, end_dt=end_datetime)
    _range = DateTimeRange(
        start_datetime, start_datetime + datetime.timedelta(minutes=1))
    assert schedule.add_record('Test_type', _range)
    assert len(schedule.records) == 1

    _range = DateTimeRange(
        start_datetime + datetime.timedelta(minutes=1), start_datetime + datetime.timedelta(minutes=2))
    assert schedule.add_record('Test_type', _range)
    assert len(schedule.records) == 2


def test_simple_add_to_schedule_no_duration_and_no_range(caplog):
    caplog.set_level(logging.INFO)
    start_datetime = datetime.datetime(year=2020, month=1, day=1)
    schedule = Schedule(start_datetime)

    _range = DateTimeRange(
        start_datetime, start_datetime + datetime.timedelta(minutes=1))
    assert not schedule.add_record('Test_type', _range)
    assert len(schedule.records) == 0


def test_clear():
    start_datetime = datetime.datetime(year=2020, month=1, day=1)
    schedule = Schedule(start_datetime, duration=3600)

    _range = DateTimeRange(
        start_datetime, start_datetime + datetime.timedelta(minutes=1))
    assert schedule.add_record('Test_type', _range)

    assert len(schedule.records) == 1
    schedule.clear()
    assert len(schedule.records) == 0
    _range = DateTimeRange(
        start_datetime + datetime.timedelta(minutes=1), start_datetime + datetime.timedelta(minutes=2))
    schedule.add_record('Test_type', _range)
    assert len(schedule.records) == 1
