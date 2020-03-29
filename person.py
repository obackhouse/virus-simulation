''' Defines the class to model a single person.
'''

import numpy as np
from copy import deepcopy as copy


_rand = lambda x: np.random.random() if x is None else x

def _get_factors(f):
    _attributes = ['loc', 'transmission_rate', 'movement_speed', 'recovery_rate', 'death_rate']
    _states = ['infected', 'recovered', 'dead']

    for key in f.keys():
        if key not in _attributes and key not in _states:
            raise ValueError

    f['loc'] = f.get('loc', [_rand(None), _rand(None)])
    f['transmission_rate'] = 0.001
    f['movement_speed'] = 0.01
    f['recovery_rate'] = 0.01
    f['death_rate'] = 0.001

    for key in _states:
        f[key] = False

    return f


class Person:
    def __init__(self, world, **kwargs):
        self.world = world

        kwargs = _get_factors(kwargs)
        for key,val in kwargs.items():
            setattr(self, key, val)

        # Defines the current journey:
        self._src = copy(self.loc)
        self._aim = None

    def attempt_recovery(self, r=None):
        if self.dead or not self.infected:
            return

        r = _rand(r)

        if r < self.recovery_rate:
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

    def attempt_move(self, r=None):
        ''' Returns True if the person has reached their aim.
        '''

        if self.dead or self._aim is None:
            return

        r = _rand(r)
        
        dx = self._aim[0] - self._src[0]
        dy = self._aim[1] - self._src[1]

        dx *= self.movement_speed / self.world.size_factor
        dy *= self.movement_speed / self.world.size_factor

        if self.loc[0] < self._aim[0]:
            self.loc[0] = max(self.loc[0]+dx, self._aim[0])
        else:
            self.loc[0] = min(self.loc[0]+dx, self._aim[0])

        if self.loc[1] < self._aim[1]:
            self.loc[1] = max(self.loc[1]+dy, self._aim[1])
        else:
            self.loc[1] = min(self.loc[1]+dy, self._aim[1])

        return np.allclose(self.loc, self._aim)

    def set_aim(self, aim=None):
        if self.dead:
            return

        if aim is None:
            aim = [_rand(None), _rand(None)]

        self._src = copy(self.loc)
        self._aim = aim

    def move(self, loc):
        self.loc = loc

    def get_distance(self, other):
        dx = self.loc[0] - other.loc[0]
        dy = self.loc[1] - other.loc[1]
        return np.sqrt(dx*dx + dy*dy)

