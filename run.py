import numpy as np
import person, world, simulation

aworld = world.World(size_factor=1)
people = [person.Person(aworld) for x in range(1000)]
for person in people: person.set_aim()
people[0].infected = True

sim = simulation.Simulation(aworld, people)

to_print = ['timestep', 'healthy', 'infected', 'recovered', 'dead']
print(' '.join(['%12s' % x for x in to_print]))
print(' '.join(['-'*12 for x in to_print]))

for step,obj in enumerate(sim.run(timesteps=100)):
    counts = obj.count_all()
    counts['timestep'] = step
    print(' '.join(['%12d' % counts[key] for key in to_print]))

print(' '.join(['-'*12 for x in to_print]))
