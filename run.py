import world, simulation

w = world.World()
w.spawn()
sim = simulation.Simulation(w, log_file='log.dat')
sim.animate()
