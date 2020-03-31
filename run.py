import world, simulation

w = world.World(population=1000, social_distance=1.0)
sim = simulation.Simulation(w, log_file='log.dat')
sim.animate(timesteps=1000, batch_size=100)
