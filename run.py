import world, simulation

w = world.World()
sim = simulation.Simulation(w, log_file='log.dat')
sim.animate(timesteps=1000, batch_size=100)
