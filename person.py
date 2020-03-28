''' Defines the class to model a single person.
'''

import numpy as np


def _get_factors(f):
    _attributes = ['x', 'y', 'transmission_rate', 'contraction_rate', 'movement_rate', 'movement_speed', 'recovery_rate', 'death_rate']
    _states = ['infected', 'recovered', 'dead']

    for key in f.keys():
        if key not in _attributes and key not in _states:
            raise ValueError

    for key in _attributes:
        f[key] = f.get(key, np.random.random())

    for key in _states:
        f[key] = False

    return f

_rand = lambda x: x if x is None else np.random.random()


class Person:
    def __init__(self, world, **kwargs):
        self.world = world

        kwargs = _get_factors(kwargs)
        for key,val in kwargs.items():
            setattr(self, key, val)

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
            self.dead = False

    def attempt_transmission(self, other, r=None):
        if self.dead or not self.infected:
            return

        r = _rand(r)
        d = self.get_distance(other)

        # FIXME: do these need to be independent random numbers?
        if r < self.transmission_rate * (1-d):
            other.attempt_contraction(self, r=r)

    def attempt_contraction(self, other, r=None):
        if self.dead or self.infected or self.recovered:
            return

        r = _rand(r)
        d = self.get_distance(other)

        if r < self.contract_rate * (1-d):
            self.infected = True
            self.recovered = False
            self.dead = False


    def get_distance(self, other):
        dx = self.x - other.x
        dy = self.y - other.y
        return np.sqrt(dx*dx + dy*dy)
