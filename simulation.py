''' Defines the class to model the simulation.
'''

import numpy as np


class Simulation:
    def __init__(self, world, people):
        self.world = world
        self.people = people

    def check_input(self):
        if not sum([person.infected for person in people]):
            raise ValueError('At least one person must be infected '
                             'to start with!')

    def timestep(self):
        ''' Performs a timestep.
        '''

        for i,p1 in enumerate(self.people):
            fin = p1.attempt_move()
            
            for j,p2 in enumerate(self.people):
                if i == j:
                    continue
                p1.attempt_transmission(p2)

            # FIXME: swapping these could change things?
            p1.attempt_death()
            p1.attempt_recovery()

            if fin:
                p1.set_aim(aim=self.get_aim(p1))

    def run(self, timesteps=10000):
        ''' Runs the simulation.
        '''

        for t in range(timesteps):
            self.timestep()
            yield self

    def get_aim(self, person):
        ''' Defines a function to get a new aim.
        '''

        return None

    def count_healthy(self):
        return sum([not p.dead and not p.infected for p in self.people])

    def count_infected(self):
        return sum([not p.dead and p.infected for p in self.people])

    def count_recovered(self):
        return sum([p.recovered for p in self.people])

    def count_dead(self):
        return sum([p.dead for p in self.people])

    def count_alive(self):
        return sum([not p.dead for p in self.people])

    def count_all(self):
        cts = { 'healthy': 0,
                'infected': 0,
                'recovered': 0,
                'dead': 0,
                'alive': 0,
        }

        for p in self.people:
            cts['healthy'] += not p.dead and not p.infected
            cts['infected'] += not p.dead and p.infected
            cts['recovered'] += p.recovered
            cts['dead'] += p.dead
            cts['alive'] += not p.dead

        return cts

