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
                 start_dt: datetime.datetime,
                 end_dt: datetime.datetime = None,
                 duration: int = 0):
        """
        Create schedule
        :param start_dt: Time point, all records must be started after this point.
        :param end_dt: All records must be ended before this point.
        :param duration: Duration in seconds - used only when end_dt is None.
        """
        if not duration and not end_dt:
            logging.error(f'Please, set end_dt or duration')
            end_dt = start_dt
        elif duration and end_dt:
            logging.error(f'Using end_dt and duration both is deprecated, '
                          f'use end_dt as default')
        elif duration:
            end_dt = start_dt + datetime.timedelta(seconds=duration)
        self.range = DateTimeRange(start_dt, end_dt)
        self.records = []

    def add_record(self, rec_type: str, rec_range: DateTimeRange, add_data=None):
        """
        Add record to schedule.
        :param rec_type:
        :param rec_range: Must be placed in Schedule.range.
        :param add_data:
        :return: Return True if record was added, else return False
        """
        if rec_range.end_datetime > self.range.end_datetime:
            return False
        if rec_range.start_datetime < self.range.start_datetime:
            return False
        record = {'type': rec_type, 'range': rec_range, 'data': add_data}
        is_last = True
        if self.records and rec_range.start_datetime <= self.records[-1]['range'].end_datetime:
            is_last = False
        self.records.append(record)
        if not is_last:
            self.records = sorted(
                self.records, key=lambda record: record['range'].start_datetime)
        return True

    def get_records_in_range(self, required_range: DateTimeRange):
        """
        Return records, which are:
            1) located in required_range
            2) intersected by required_range
        :param required_range:
        :return: List of records
        """
        if not self.records:
            return []
        result = []
        for record in self.records:
            rec_range = record['range']
            if required_range.is_intersection(rec_range) and \
                    required_range.end_datetime != rec_range.start_datetime and \
                    required_range.start_datetime != rec_range.end_datetime:
                result.append(record)
        return result

    def change_record(self, old_record, new_record):
        """
        Modify records which are equal old record
        :param old_record:
        :param new_record:
        :return: True, if old record is in schedule's records. Otherwise return False.
        """
        if old_record not in self.records:
            logging.error(f'Record {old_record} not in schedule')
            return False

        for index, item in enumerate(self.records):
            if item == old_record:
                self.records[index] = new_record
        return True

    def clear(self):
        """
        Delete all records from schedule
        :return:
        """
        self.records.clear()
