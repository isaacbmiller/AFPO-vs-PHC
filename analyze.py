import numpy
import matplotlib.pyplot

# Make a graph of all best fitnesses
runName = "parallelHC-run-test"

# bestFitnesses = numpy.load("data/" + runName + "/bestFitnesses.npy")
# averageFitnesses = numpy.load("data/" + runName + "/averageFitnesses.npy")

# matplotlib.pyplot.plot(bestFitnesses, label="Best Fitness")
# matplotlib.pyplot.plot(averageFitnesses, label="Average Fitness")
# matplotlib.pyplot.legend()
# matplotlib.pyplot.xlabel("Generation")
# matplotlib.pyplot.ylabel("Fitness")
# matplotlib.pyplot.title("Best and Average Fitnesses")

# matplotlib.pyplot.show()

# Use this for analyzing multiple runs
for i in range(0, 5):
    bestFitnesses = numpy.load("data/" + runName + str(i) + "/averageFitnesses.npy")
    matplotlib.pyplot.plot(bestFitnesses, label="Run " + str(i))


matplotlib.pyplot.legend()
matplotlib.pyplot.xlabel("Generation")
matplotlib.pyplot.ylabel("Fitness")
matplotlib.pyplot.title("Average Fitnesses per Run")
matplotlib.pyplot.show()
