''' Defines the class to model the world.
'''

import numpy as np
import log


_defaults = {
    'population': 1000,
    'transmission_rate': 0.01,
    'movement_speed' : 0.01,
    'recovery_rate': 0.01,
    'death_rate': 0.002,
    'max_infection_time': 25,
    'social_distance': 0.05,
    'locality_factor': 25,
}
_status_ref = np.asarray(['healthy', 'infected', 'recovered', 'dead'], dtype=object)


class World:
    def __init__(self, **kwargs):
        opts = _defaults.copy()
        opts.update(kwargs)
        for key,val in opts.items():
            if key not in _defaults.keys():
                raise ValueError
            setattr(self, key, opts.get(key, _defaults[key]))

        self.locations = np.random.random((2, self.pop))
        self._status = np.zeros((self.pop), dtype=int)
        self._t_since_infection = np.zeros((self.pop))

    def encounter(self, mask_a=None, mask_b=None, func='exp'):
        ''' Returns a matrix of probabilities that each pair of persons
            will have a successful encounter.
        '''

        mask_a = self._full_mask if mask_a is None else mask_a
        mask_b = self._full_mask if mask_b is None else mask_b

        x, y = self.loc
        xa, xb = x[mask_a], x[mask_b]
        ya, yb = y[mask_a], y[mask_b]
        
        d = np.sqrt((xa[:,None] - xb[None,:])**2 + (ya[:,None] - yb[None,:])**2)
        d /= np.sqrt(2)

        if func == 'exp':
            p = np.exp(-self.locality_factor * d)
        elif func == 'pow':
            p = (1 - d) ** self.locality_factor

        return p

    def spawn(self):
        self._status[0] = 1

    def attempt_recovery(self, mask=None, log_file=None):
        mask = self._full_mask if mask is None else mask
        do = self.infected
        do[~mask] = False

        self._t_since_infection[do] += 1
        tfac = 1.0 + self._t_since_infection[do] / self.max_infection_time

        r = self.get_rand(do)

        mask = self._null_mask
        mask[do] = r < (self.recovery_rate * tfac)

        if log_file is not None:
            for i in range(self.pop):
                if mask[i]:
                    log_file.recovered(i)

        np.place(self._status, mask, 2)

    def attempt_death(self, mask=None, log_file=None):
        mask = self._full_mask if mask is None else mask
        do = self.infected
        do[~mask] = False

        r = self.get_rand(do)

        mask = self._null_mask
        mask[do] = r < self.death_rate

        if log_file is not None:
            for i in range(self.pop):
                if mask[i]:
                    log_file.died(i)

        np.place(self._status, mask, 3)

    def attempt_transmission(self, mask=None, log_file=None):
        mask = self._full_mask if mask is None else mask
        do = self.infected
        do[~mask] = False

        to = self.healthy

        r = np.random.random((np.sum(do), self.pop))

        mask = np.zeros((self.pop, self.pop), dtype=bool)
        mask[do] = r < (self.encounter(do) * self.transmission_rate)
        fmask = np.any(mask, axis=0)

        if log_file:
            for j in range(self.pop):
                if fmask[j]:
                    for i in range(self.pop):
                        if i != j:
                            if mask[i,j]:
                                d = self.get_distance(i, j)
                                log_file.infected(i, j, d)
                                break

        np.place(self._status, np.logical_and(to, fmask), 1)

    def attempt_move(self, mask=None):
        do = ~self.dead

        rx = self.get_rand(do)
        ry = self.get_rand(do)

        mfac = self.movement_speed

        dx = 2.0 * (rx - 0.5) * mfac
        dy = 2.0 * (ry - 0.5) * mfac
        d = np.stack((dx, dy))

        self.locations[:,do] += d
        self.locations[self.loc < 0] = 0
        self.locations[self.loc > 1] = 1

    def get_rand(self, mask=slice(None)):
        n = self._status[mask].shape
        return np.random.random(n)

    def get_distance(self, i, j):
        return np.linalg.norm(self.loc[:,i] - self.loc[:,j])

    @property
    def pop(self):
        return self.population

    @property
    def loc(self):
        return self.locations

    @property
    def _null_mask(self):
        return np.zeros((self.pop), dtype=bool)

    @property
    def _full_mask(self):
        return np.ones((self.pop), dtype=bool)

    _status_ref = _status_ref

    @property
    def status(self):
        s = np.zeros((self.pop), dtype=object)
        s = self._status_ref[self._status]
        return s

    @property
    def healthy(self):
        return self._status == 0

    @property
    def infected(self):
        return self._status == 1

    @property
    def recovered(self):
        return self._status == 2

    @property
    def dead(self):
        return self._status == 3

