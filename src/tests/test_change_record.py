import datetime
import logging

from datetimerange import DateTimeRange
from schedule.schedule import Schedule


def test_change_record_type():
    start_datetime = datetime.datetime(year=2020, month=1, day=1)
    schedule = Schedule(start_datetime, duration=3600)

    _range = DateTimeRange(
        start_datetime, start_datetime + datetime.timedelta(minutes=1))
    schedule.add_record('OLD TYPE', _range)

    assert len(schedule.records) == 1
    existed_record = schedule.records[-1]
    assert 'type' in existed_record
    assert existed_record['type'] == 'OLD TYPE'
    new_record = {'type': 'NEW TYPE', 'range': _range, 'data': None}
    schedule.change_record(existed_record, new_record)

    assert 'type' in schedule.records[-1]
    assert schedule.records[-1]['type'] == 'NEW TYPE'


def test_change_record_range():
    start_datetime = datetime.datetime(year=2020, month=1, day=1)
    schedule = Schedule(start_datetime, duration=3600)

    _range = DateTimeRange(
        start_datetime, start_datetime + datetime.timedelta(minutes=1))
    schedule.add_record('OLD TYPE', _range)

    assert len(schedule.records) == 1
    existed_record = schedule.records[-1]

    assert 'range' in schedule.records[-1]
    assert schedule.records[-1]['range'] == _range

    new_range = DateTimeRange(
        start_datetime, start_datetime + datetime.timedelta(minutes=2))
    new_record = {'type': 'NEW TYPE', 'range': new_range, 'data': None}
    schedule.change_record(existed_record, new_record)

    assert 'range' in schedule.records[-1]
    assert schedule.records[-1]['range'] == new_range
