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

    def add_record(self, rec_type, rec_range: DateTimeRange, add_data):
        """
        Add record
        :param rec_type:
        :param rec_range:
        :param add_data:
        :return:
        """
        record = {'type': rec_type, 'range': rec_range, 'data': add_data}
        is_last = True
        if self.records and rec_range.start_datetime <= self.records[-1]['range'].end.datetime:
            is_last = False
        self.records.append(record)
        if not is_last:
            self.records = sorted(
                self.records, key=lambda record: record.start_datetime)

    def get_records_in_range(self, required_range: DateTimeRange):
        """
        Return records, which are:
            1) located in required_range
            2) intersected by required_range
        :param required_range:
        :return:
        """
        if not self.records:
            return []
        result = []
        for record in self.records:
            rec_range = record['range']
            if required_range.is_intersection(rec_range):
                result.append(record)
        return result
