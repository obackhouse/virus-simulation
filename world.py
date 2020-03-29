''' Defines the class to model the world.
'''

import numpy as np


class World:
    def __init__(self, size_factor=10, locality_factor=3):
        self.size_factor = size_factor
        self.locality_factor = locality_factor

    def encounter(self, p1, p2):
        ''' Essentially finds the probability that two people encounter
            eachother based on how closed they are and how big the
            world is, for use in transmission probabilities.
        '''

        d = p1.get_distance(p2)
        d = min(d, 1.0)

        p = (1 - d) ** self.locality_factor
        p /= self.size_factor

        return p
