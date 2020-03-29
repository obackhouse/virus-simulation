''' Defines the class to model the simulation.
'''

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


_default_colors = { 'infected': 'r', 'healthy': 'b', 'recovered': '0.5', 'dead': '0.2' }
_default_markers = { 'infected': 'o', 'healthy': 'o', 'recovered': 'o', 'dead': 'x' }
_keys = ['infected', 'healthy', 'recovered', 'dead']


class Simulation:
    def __init__(self, world, people):
        self.world = world
        self.people = people

        self.t = 0

    def check_input(self):
        if not sum([person.infected for person in people]):
            raise ValueError('At least one person must be infected '
                             'to start with!')

    def timestep(self):
        ''' Performs a timestep.
        '''

        for i,p1 in enumerate(self.people):
            p1.attempt_move()
            
            for j,p2 in enumerate(self.people):
                if i == j:
                    continue
                p1.attempt_transmission(p2)

            # FIXME: swapping these could change things?
            p1.attempt_death()
            p1.attempt_recovery()

    def run(self, timesteps=10000, animate=True, **kwargs):
        ''' Runs the simulation.
        '''

        if animate:
            yield from self.animate(**kwargs)
        else:
            yield from self._run(timesteps=timesteps)

    def _run(self, timesteps=10000):
        for self.t in range(timesteps):
            self.timestep()
            yield self

    def animate(self, timesteps=10000, **kwargs):
        ''' Animates the simulation.
        '''

        fig = plt.figure(figsize=kwargs.get('figsize', (8,4)))
        ax1 = fig.add_subplot(121)
        ax2 = fig.add_subplot(122)

        left = []
        right = []

        colors = _default_colors.copy()
        markers = _default_markers.copy()

        colors.update(kwargs.get('colors', {}))
        markers.update(kwargs.get('markers', {}))
        
        for key in _keys:
            plot, = ax1.plot([], [], markers[key], color=colors[key], markersize=kwargs.get('markersize', 3))
            left.append(plot)

            plot, = ax2.plot([], [], '-', color=colors[key])
            right.append(plot)

        loc = np.zeros((2, len(self.people)))
        status = np.zeros((len(self.people),), dtype=object)
        stack = np.zeros((4, timesteps))

        ax1.set_xlim(0, 1)
        ax1.set_ylim(0, 1)
        ax2.set_ylim(0, len(self.people))

        def update(self):
            t = self.t
            times = np.arange(t + 1)

            for i,person in enumerate(self.people):
                loc[:,i] = person.loc
                status[i] = person.status

            for i,key in enumerate(_keys):
                mask = status == key
                stack[i,t] = np.sum(mask)
                left[i].set_data(loc[0][mask], loc[1][mask])

                if not kwargs.get('stack_plot', True):
                    right[i].set_data(times, stack[i,:t+1])

            if kwargs.get('stack_plot', True):
                right[:] = ax2.stackplot(times, stack[:,:t+1], colors=[colors[k] for k in _keys])

            ax2.set_xlim(0, max(t, 1))

            return (*left, *right)

        anim = FuncAnimation(fig, update, frames=self._run(timesteps=timesteps), blit=True)
        plt.show()

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
