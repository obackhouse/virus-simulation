''' Defines the class to model the simulation.
'''

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.animation import FuncAnimation
from matplotlib.lines import Line2D
import log

plt.style.use(['seaborn'])
plt.rc('font', family='serif')
plt.rc('figure.subplot', left=0.05, right=0.95, bottom=0.1, 
                         top=0.95, wspace=0.1, hspace=0.1)


_default_colors = { 'infected': 'r', 'healthy': 'b', 'recovered': '0.5', 'dead': 'k' }
_default_colors = { 'infected': '#df1e05', 'healthy': '#1166f4', 'recovered': '0.5', 'dead': 'k' }
_default_markers = { 'infected': 'o', 'healthy': 'o', 'recovered': 'o', 'dead': 'X' }
_default_markersize = { 'infected': 3, 'healthy': 3, 'recovered': 3, 'dead': 5 }
_default_zorder = {'infected': 2, 'healthy': 2, 'recovered': 1, 'dead': 1 }


class Simulation:
    def __init__(self, world, batch_size=100, log_file=None):
        self.world = world
        self.batch_size = batch_size
        self.log_file = log_file

        if isinstance(self.log_file, str):
            self.log_file = log.Log(self.log_file)

        self.t = 0

    def timestep(self):
        ''' Performs a timestep.
        '''

        self.world.attempt_move()

        for start in range(0, self.world.pop, self.batch_size):
            stop = min(start + self.batch_size, self.world.pop)
            mask = np.zeros((self.world.pop), dtype=bool)
            mask[start:stop] = True

            self.world.attempt_transmission(mask=mask, log_file=self.log_file)
            self.world.attempt_death(mask=mask, log_file=self.log_file)
            self.world.attempt_recovery(mask=mask, log_file=self.log_file)

        if self.log_file is not None:
            self.log_file.t += 1

    def run(self, **kwargs):
        ''' Runs the simulation.
        '''

        if not self.count_infected():
            self.world.spawn()

        for self.t in range(kwargs.get('timesteps', 10000)):
            self.timestep()
            yield self

        if self.log_file is not None:
            self.log_file.finalise()

    def animate(self, **kwargs):
        ''' Animates the simulation.
        '''

        keys = ['infected', 'healthy', 'recovered', 'dead']

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
        patches = [mpatches.Patch(color=colors[key], label=key) for key in keys]
        ax2.legend(handles=patches, loc='center left', bbox_to_anchor=(1, 0.5))
        
        for key in keys:
            plot, = ax1.plot([], [], markers[key], color=colors[key], markersize=markersize[key], zorder=zorder[key])
            left.append(plot)

            plot, = ax2.plot([], [], '-', color=colors[key])
            right.append(plot)

        loc = self.world.loc.copy()
        status = self.world.status.copy()
        stack = np.zeros((4, kwargs.get('timesteps', 10000)))

        ax1.set_xlim(0, 1)
        ax1.set_ylim(0, 1)
        ax2.set_ylim(0, self.world.population)

        def update(self):
            t = self.t
            times = np.arange(t + 1)

            loc = self.world.loc.copy()
            status = self.world.status.copy()

            for i,key in enumerate(keys):
                mask = status == key
                stack[i,t] = np.sum(mask)
                left[i].set_data(loc[0][mask], loc[1][mask])

                if not kwargs.get('stack_plot', True):
                    right[i].set_data(times, stack[i,:t+1])

            if kwargs.get('stack_plot', True):
                ax2.collections.clear()
                right[:] = ax2.stackplot(times, stack[:,:t+1], colors=[colors[k] for k in keys])

            ax2.set_xlim(0, max(t, 1))

            return (*left, *right)

        anim = FuncAnimation(fig, update, blit=True, interval=kwargs.get('interval', 100), frames=self.run(**kwargs), repeat=False)
        plt.show()

    def count_healthy(self):
        return np.sum(self.world.healthy)

    def count_infected(self):
        return np.sum(self.world.infected)

    def count_recovered(self):
        return np.sum(self.world.recovered)

    def count_dead(self):
        return np.sum(self.world.dead)

    def count_alive(self):
        return self.world.pop - self.count_dead()

    def count_all(self):
        cts = {
            'healthy': self.count_healthy(),
            'infected': self.count_infected(),
            'recovered': self.count_recovered(),
            'dead': self.count_dead(),
            'alive': self.count_alive(),
        }

        return cts
