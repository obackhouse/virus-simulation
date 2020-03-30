''' Defines function to log events.
'''

import numpy as np


class Log:
    def __init__(self, name='log.dat'):
        self._log = open('log.dat', 'w')
        self.t = 0

    def finalise(self):
        self._log.flush()
        self._log.close()
        del self._log

    def infected(self, source, target, d):
        line = '%12d %d infected %d at a distance of %.6f\n' % (self.t, source, target, d)
        self._log.write(line)

    def recovered(self, target):
        line = '%12d %d recovered\n' % (self.t, target)
        self._log.write(line)

    def died(self, target):
        line = '%12d %d died\n' % (self.t, target)
        self._log.write(line)

    def set_time(self, t):
        self.t = t
