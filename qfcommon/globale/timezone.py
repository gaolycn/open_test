#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
#ref: https://docs.python.org/2.7/library/datetime.html#datetime.tzinfo

class CustomerZone(datetime.tzinfo):

    ZERO = datetime.timedelta(0)
    def __init__(self, z = '+0800'):
        self._zone = z
        self._offset  = self._get_offset(z)

    def __repr__(self):
        return '[Zone %s]' % self._zone

    def _get_offset(self, z):
        h = int(z[1:3])
        m = int(z[3:5])
        if z[0] == '+':
            return datetime.timedelta(hours = h, minutes = m)
        else:
            return datetime.timedelta(hours = 0-h, minutes = 0-m)

    def utcoffset(self, dt):
        return self._offset

    def tzname(self, dt):
        return self._zone

    def dst(self, dt):
        return self.ZERO
