#!/usr/bin/env python3

import datetime
import calendar


class date_help:

    sys = datetime.datetime.now()

    def __init__(self, *args, **kwargs):
        """ these elements should be made composable
        and some might-be useful combinations provided

        we should stick to one format and arguments format variable
        here we process on string format basis

        this is essentially a design technique """

        # if no arguments provided default to current month
        self.usr_yy = self.sys.year
        self.usr_mm = self.sys.month
        self.days = calendar.monthrange(self.usr_yy, self.usr_mm)[1]

        if args and len(args) >= 2:
            self.update(args[0], args[1])
        elif kwargs and len(kwargs) >= 2:
            self.update(kwargs['yy'], kwargs['mm'])

    def update(self, year, month):
        self.usr_yy = year
        self.usr_mm = month
        self.days = calendar.monthrange(year, month)[1]

    def is_valid(self, year, month, day):
        """ actually we can plug in a filter module here
        but here is another topic anyway """

        usr_yy_mm = '{0:04d}{1:02d}'.format(self.usr_yy, self.usr_mm)
        link_yy_mm = year + month

        if usr_yy_mm != link_yy_mm:
            return False

        int_day = int(day)
        if int_day < 1 or int_day > self.days:
            return False

        return True

    def sys_date(self):
        return '{0:04d}{1:02d}{2:02d}'.format(self.sys.year, self.sys.month, self.sys.day)

    def stop_date(self):
        """ currently only support downloading on a monthly basis
        this is enough for personal use """
        return '{0:04d}{1:02d}'.format(self.usr_yy, self.usr_mm) + '01'
