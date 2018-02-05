#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
# Description: renderd syslog netdata python.d module
# Debug: /usr/libexec/netdata/plugins.d/python.d.plugin debug 1 tiles


import re
from os import access as is_accessible, R_OK
from os.path import getsize


from bases.FrameworkServices.LogService import LogService

priority = 60000
retries = 60
# Feb  2 11:27:32 scw-bc06a7 renderd[13031]: DEBUG: DONE TILE piano2x 7 64-71 64-71 in 3.858 seconds  # noqa
REGEX_DATA = re.compile('DEBUG: DONE TILE (?P<style>\w+) (?P<zoom>\d{1,2}) [\w -]+ in (?P<duration>[\d\.]+) seconds')  # noqa
ORDER = ['styles']
CHARTS = {
    'styles': {
        'options': [None, 'Tiles generation by style', 'tiles/s',
                    'renderd', 'renderd', 'line'],
        'lines': []
    },
    'duration': {
        'options': [None, 'Tiles generation time', 'seconds',
                    'renderd', 'renderd', 'line'],
        'lines': [['duration_'+str(i), str(i)] for i in range(21)]
    },
}


class Service(LogService):
    """
    renderd syslog class
    Reads logs line by line
    It produces following charts:
    * Tiles computed per second
    """
    def __init__(self, configuration=None, name=None):
        LogService.__init__(self, configuration=configuration, name=name)
        self.order = CHARTS
        self.definitions = CHARTS
        self.log_path = '/var/log/syslog'
        self.data = dict()
        self.cache = dict()
        for i in range(21):
            self.cache['duration_'+str(i)] = (0, 0)
            self.data['duration_'+str(i)] = 0

    def _get_data(self):
        """
        Parse new log lines
        :return: dict
        """
        raw = self._get_raw_data()
        for key in self.data:
            if key.startswith('style_'):
                self.data[key] = 0  # Reset style to have a smooth line.

        if raw is None:
            return self.data

        for row in raw:
            match = REGEX_DATA.search(row)
            if match:
                style, zoom, duration = match.groups()
                duration_key = 'duration_' + zoom
                total, average = self.cache[duration_key]
                new_total = total + 1
                new_average = (total * average + float(duration)) / new_total
                self.cache[duration_key] = (new_total, new_average)
                self.data[duration_key] = new_average
                style_key = 'style_' + style
                if style_key not in self.charts['styles']:
                    self.charts['styles'].add_dimension([style_key, style,
                                                         'absolute'])
                if style_key not in self.data:
                    self.data[style_key] = 0
                self.data[style_key] += 1

        return self.data

    def check(self):
        """
        :return: bool

        Check if the "log_path" is not empty and readable
        """

        if not (is_accessible(self.log_path, R_OK)
           and getsize(self.log_path) != 0):
            self.error('%s is not readable or empty' % self.log_path)
            return False
        return True
