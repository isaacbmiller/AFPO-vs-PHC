import numpy
import matplotlib.pyplot

# Make a graph of all best fitnesses
# Read from bestFitnesses-X.npy where X 1-5
for i in range(1, 6):
    bestFitnesses = numpy.load("data/bestFitnesses-%d.npy" % i)
    matplotlib.pyplot.plot(bestFitnesses, label="Run %d" % i)

matplotlib.pyplot.legend()
matplotlib.pyplot.xlabel("Generation")
matplotlib.pyplot.ylabel("Fitness")
matplotlib.pyplot.title("Best Fitnesses per Run")
matplotlib.pyplot.show()
