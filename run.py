import numpy as np
import person, world, simulation
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.collections import PolyCollection

aworld = world.World(size_factor=1)
people = [person.Person(aworld) for x in range(1000)]
people[0].infected = True

sim = simulation.Simulation(aworld, people)

timesteps = 1000

stack_plot = True

#to_print = ['timestep', 'healthy', 'infected', 'recovered', 'dead']
#print(' '.join(['%12s' % x for x in to_print]))
#print(' '.join(['-'*12 for x in to_print]))

#for step,obj in enumerate(sim.run(timesteps=timesteps)):
#    counts = obj.count_all()
#    counts['timestep'] = step
#    print(' '.join(['%12d' % counts[key] for key in to_print]))
#
#print(' '.join(['-'*12 for x in to_print]))


#fig = plt.figure(figsize=(8, 4))
#ax1 = fig.add_subplot(121)
#ax2 = fig.add_subplot(122)
#
#time = np.arange(timesteps)
#loc = np.full(shape=(2, len(people)), fill_value=np.nan)
#status = np.zeros(len(people), dtype=object)
#stack = np.zeros((4, timesteps))
#fills = np.zeros((4,), dtype=object)
#
#markersize = 3
#
#inf1, = ax1.plot([], [], 'ro', markersize=markersize)
#hea1, = ax1.plot([], [], 'bo', markersize=markersize)
#rec1, = ax1.plot([], [], 'o', color='0.5', markersize=markersize)
#dea1, = ax1.plot([], [], 'X', color='0.2', markersize=markersize)
#
#inf2, = ax2.plot([], [], 'r-')
#hea2, = ax2.plot([], [], 'b-')
#rec2, = ax2.plot([], [], '-', color='0.5')
#dea2, = ax2.plot([], [], '-', color='0.2')
#
#ax1.set_xlim(0, 1)
#ax1.set_ylim(0, 1)
#ax2.set_ylim(0, len(people))
#
#def update(simulation):
#    t = simulation.t
#
#    for i,person in enumerate(people):
#        loc[:,i] = person.loc
#        status[i] = person.status
#
#    inf = status == 'infected'
#    hea = status == 'healthy'
#    rec = status == 'recovered'
#    dea = status == 'dead'
#
#    stack[0,t] = np.sum(inf)
#    stack[1,t] = np.sum(hea)
#    stack[2,t] = np.sum(rec)
#    stack[3,t] = np.sum(dea)
#
#    inf1.set_data(loc[0][inf], loc[1][inf])
#    hea1.set_data(loc[0][hea], loc[1][hea])
#    rec1.set_data(loc[0][rec], loc[1][rec])
#    dea1.set_data(loc[0][dea], loc[1][dea])
#
#    times = np.arange(t+1)
#
#    if stack_plot:
#        inf2.set_data(times, stack[0,:t+1])
#        dea2.set_data(times, 1000-stack[3,:t+1])
#        rec2.set_data(times, 1000-stack[3,:t+1]-stack[2,:t+1])
#
#        if t:
#            ax2.collections.clear()
#
#        f1, = ax2.fill_between(times, np.zeros_like(times), stack[0,:t+1], color='r'),
#        f2, = ax2.fill_between(times, stack[0,:t+1]+1, 1000-stack[3,:t+1]-stack[2,:t+1]-1, color='b'),
#        f3, = ax2.fill_between(times, 1000-stack[3,:t+1]-stack[2,:t+1], 1000-stack[3,:t+1]-1, color='0.5'),
#        f4, = ax2.fill_between(times, 1000-stack[3,:t+1], 1000, color='0.2'),
#
#    else:
#        inf2.set_data(times, stack[0,:t+1])
#        hea2.set_data(times, stack[1,:t+1])
#        rec2.set_data(times, stack[2,:t+1])
#        dea2.set_data(times, stack[3,:t+1])
#    
#    ax2.set_xlim(0, max(t, 1))
#
#    return inf1, hea1, rec1, dea1, inf2, hea2, rec2, dea2, f1, f2, f3, f4

#anim = FuncAnimation(fig, update, frames=sim.run(timesteps=timesteps), blit=True)
#plt.show()

sim.animate()
