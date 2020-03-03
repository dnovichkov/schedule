import copy
import datetime
import logging

from datetimerange import DateTimeRange
from schedule.schedule import Schedule


def test_change_record_type():
    start_datetime = datetime.datetime(year=2020, month=1, day=1)
    schedule = Schedule(start_datetime, duration=3600)

    _range = DateTimeRange(
        start_datetime, start_datetime + datetime.timedelta(minutes=1))
    assert schedule.add_record('OLD TYPE', _range)

    assert len(schedule.records) == 1
    existed_record = schedule.records[-1]
    assert 'type' in existed_record
    assert existed_record['type'] == 'OLD TYPE'
    new_record = {'type': 'NEW TYPE', 'range': _range, 'data': None}
    assert schedule.change_record(existed_record, new_record)

    assert 'type' in schedule.records[-1]
    assert schedule.records[-1]['type'] == 'NEW TYPE'


def test_change_record_range():
    start_datetime = datetime.datetime(year=2020, month=1, day=1)
    schedule = Schedule(start_datetime, duration=3600)

    _range = DateTimeRange(
        start_datetime, start_datetime + datetime.timedelta(minutes=1))
    assert schedule.add_record('OLD TYPE', _range)

    assert len(schedule.records) == 1
    existed_record = schedule.records[-1]

    assert 'range' in schedule.records[-1]
    assert schedule.records[-1]['range'] == _range

    new_range = DateTimeRange(
        start_datetime, start_datetime + datetime.timedelta(minutes=2))
    new_record = {'type': 'NEW TYPE', 'range': new_range, 'data': None}
    assert schedule.change_record(existed_record, new_record)

    assert 'range' in schedule.records[-1]
    assert schedule.records[-1]['range'] == new_range


def test_change_record_data():
    start_datetime = datetime.datetime(year=2020, month=1, day=1)
    schedule = Schedule(start_datetime, duration=3600)

    _range = DateTimeRange(
        start_datetime, start_datetime + datetime.timedelta(minutes=1))
    assert schedule.add_record('OLD TYPE', _range)

    assert len(schedule.records) == 1
    assert 'data' in schedule.records[-1]
    assert schedule.records[-1]['data'] is None

    existed_record = schedule.records[-1]

    new_range = DateTimeRange(
        start_datetime, start_datetime + datetime.timedelta(minutes=2))
    new_record = {'type': 'NEW TYPE',
                  'range': new_range, 'data': {'key': 'val'}}
    assert schedule.change_record(existed_record, new_record)

    assert 'data' in schedule.records[-1]
    assert schedule.records[-1]['data'] == {'key': 'val'}


def test_change_wrong_record():
    start_datetime = datetime.datetime(year=2020, month=1, day=1)
    schedule = Schedule(start_datetime, duration=3600)

    _range = DateTimeRange(
        start_datetime, start_datetime + datetime.timedelta(minutes=1))
    assert schedule.add_record('OLD TYPE', _range)

    not_existed_record = copy.deepcopy(schedule.records[-1])

    new_range = DateTimeRange(
        start_datetime, start_datetime + datetime.timedelta(minutes=2))
    not_existed_record['range'] = new_range
    new_record = {'type': 'NEW TYPE',
                  'range': new_range, 'data': {'key': 'val'}}
    assert not schedule.change_record(not_existed_record, new_record)

    assert 'data' in schedule.records[-1]
    assert schedule.records[-1]['data'] is None
