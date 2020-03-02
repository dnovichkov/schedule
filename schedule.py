"""
Base class for schedule
"""
import datetime
import logging

from datetimerange import DateTimeRange


class Schedule:
    """
    Ranged schedule class
    """

    def __init__(self,
                 start_dt: datetime.datime,
                 end_dt: datetime.datetime = None,
                 duration: int = 0):
        """
        Create schedule
        :param start_dt:
        :param end_dt:
        :param duration:
        """
        if not duration and not end_dt:
            logging.error(f'Please, set end_dt or duration')
        elif duration and end_dt:
            logging.error(f'Using end_dt and duration both is deprecated, '
                          f'use end_dt as default')
        elif duration:
            end_dt = start_dt + datetime.timedelta(seconds=duration)
        self.range = DateTimeRange(start_dt, end_dt)
        self.records = []

    def add_record(self, rec_type, rec_range, add_data):
        record = {'type': rec_type, 'range': rec_range, 'data': add_data}
        self.records.append(record)
        self.records = sorted(
            self.records, key=lambda record: record.start_datetime)
