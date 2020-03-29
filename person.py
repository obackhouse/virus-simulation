''' Defines the class to model a single person.
'''

import numpy as np
from copy import deepcopy as copy


_rand = lambda x: np.random.random() if x is None else x

def _get_factors(f):
    _attributes = ['loc', 'transmission_rate', 'movement_speed', 'recovery_rate', 'death_rate', 'max_infection_length']
    _states = ['infected', 'recovered', 'dead']

    for key in f.keys():
        if key not in _attributes and key not in _states:
            raise ValueError

    f['loc'] = f.get('loc', [_rand(None), _rand(None)])
    f['transmission_rate'] = 0.001
    f['movement_speed'] = 0.01
    f['recovery_rate'] = 0.01
    f['death_rate'] = 0.001
    f['max_infection_length'] = 50

    for key in _states:
        f[key] = False

    return f


class Person:
    def __init__(self, world, **kwargs):
        self.world = world

        kwargs = _get_factors(kwargs)
        for key,val in kwargs.items():
            setattr(self, key, val)

        # Incremented during recovery attempt:
        self._t_since_infection = 0

    def attempt_recovery(self, r=None):
        if self.dead or not self.infected:
            return

        self._t_since_infection += 1
        time_factor = 1.0 + self._t_since_infection / self.max_infection_length

        r = _rand(r)

        if r < (self.recovery_rate * time_factor):
            self.infected = False
            self.recovered = True
            self.dead = False

    def attempt_death(self, r=None):
        if self.dead or not self.infected:
            return

        r = _rand(r)

        if r < self.death_rate:
            self.infected = False
            self.recovered = False
            self.dead = True

    def attempt_transmission(self, other, r=None):
        if self.dead or not self.infected or other.dead or other.infected or other.recovered:
            return

        r = _rand(r)

        # FIXME: do these need to be independent random numbers?
        if r < self.transmission_rate * self.world.encounter(self, other):
            other.infected = True

    def attempt_move(self, rx=None, ry=None):
        ''' Returns True if the person has reached their aim.
        '''

        if self.dead:
            return

        rx = _rand(rx)
        ry = _rand(ry)
        
        dx = 2.0 * (rx - 0.5) * self.movement_speed / self.world.size_factor
        dy = 2.0 * (ry - 0.5) * self.movement_speed / self.world.size_factor

        self.loc[0] += dx
        self.loc[1] += dy

    def move(self, loc):
        self.loc = loc

    def get_distance(self, other):
        dx = self.loc[0] - other.loc[0]
        dy = self.loc[1] - other.loc[1]
        return np.sqrt(dx*dx + dy*dy)

    @property
    def status(self):
        if self.dead:
            return 'dead'
        elif self.infected:
            return 'infected'
        elif self.recovered:
            return 'recovered'
        else:
            return 'healthy'


