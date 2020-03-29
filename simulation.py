''' Defines the class to model the simulation.
'''

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.animation import FuncAnimation
from matplotlib.lines import Line2D

plt.style.use(['seaborn'])
plt.rc('font', family='serif')
plt.rc('figure.subplot', left=0.05, right=0.95, bottom=0.1, 
                         top=0.95, wspace=0.1, hspace=0.1)


_default_colors = { 'infected': 'r', 'healthy': 'b', 'recovered': '0.5', 'dead': 'k' }
_default_colors = { 'infected': '#df1e05', 'healthy': '#1166f4', 'recovered': '0.5', 'dead': 'k' }
_default_markers = { 'infected': 'o', 'healthy': 'o', 'recovered': 'o', 'dead': 'X' }
_default_markersize = { 'infected': 3, 'healthy': 3, 'recovered': 3, 'dead': 5 }
_default_zorder = {'infected': 2, 'healthy': 2, 'recovered': 1, 'dead': 1 }
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

        fig = plt.figure(figsize=kwargs.get('figsize', (12,4)))
        grid = fig.add_gridspec(1, 3)
        ax1 = fig.add_subplot(grid[0,0])
        ax2 = fig.add_subplot(grid[0,1:])

        ax1.set_xticks([])
        ax1.set_yticks([])
        ax2.set_xticks([])
        ax2.set_yticks([])

        ax2.set_xlabel(r'time $\rightarrow$')

        left = []
        right = []

        colors = _default_colors.copy()
        markers = _default_markers.copy()
        markersize = _default_markersize.copy()
        zorder = _default_zorder.copy()

        colors.update(kwargs.get('colors', {}))
        markers.update(kwargs.get('markers', {}))

        box = ax2.get_position()
        ax2.set_position([box.x0, box.y0, box.width * 0.85, box.height])
        patches = [mpatches.Patch(color=colors[key], label=key) for key in _keys]
        ax2.legend(handles=patches, loc='center left', bbox_to_anchor=(1, 0.5))
        
        for key in _keys:
            plot, = ax1.plot([], [], markers[key], color=colors[key], markersize=markersize[key], zorder=zorder[key])
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
                ax2.collections.clear()
                right[:] = ax2.stackplot(times, stack[:,:t+1], colors=[colors[k] for k in _keys])

            ax2.set_xlim(0, max(t, 1))

            return (*left, *right)

        anim = FuncAnimation(fig, update, blit=True, interval=0, frames=self._run(timesteps=timesteps))
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
