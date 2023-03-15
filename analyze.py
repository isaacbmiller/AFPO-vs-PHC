import numpy
import matplotlib.pyplot

# Make a graph of all best fitnesses
# runName = "2023-03-14_10-49-56"

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
# Show two graphs next to eachother, one per running method. Each running method has 5 lines, one for each run.
runNames = ["AFPO-run-test-250-", "parallelHC-run-test-250-"]
runTitles = ["AFPO", "Parallel HC"]
averageFitnesses = {runName: [] for runName in runNames}
for runName in runNames:
    for i in range(0, 5):
        data = [numpy.load("data/" + runName + str(i) + "/averageFitnesses.npy")]
        
        data = [x[:250] for x in data ]
        averageFitnesses[runName] += data

# Show two graphs next to eachother, one per running method. Each running method has 5 lines, one for each run.
fig, axs = matplotlib.pyplot.subplots(1, 2, sharey=True, tight_layout=True)
for i in range(0, 2):
    for j in range(0, 5):
        # Plot the average fitness as opaque dotted lines
        axs[i].plot(averageFitnesses[runNames[i]][j], label="Run " + str(j), linestyle="dotted", alpha=0.5)
    # Calculate the average of the average fitnesses at each generation
    averageAverageFitnessPerGen = [0 for _ in range(len(averageFitnesses[runNames[i]][0]))]
    for j in range(0, 5):
        for k in range(0, len(averageFitnesses[runNames[i]][0])):
            averageAverageFitnessPerGen[k] += averageFitnesses[runNames[i]][j][k]
    for j in range(0, len(averageAverageFitnessPerGen)):
        averageAverageFitnessPerGen[j] /= 5
    # Make the average line thicker
    axs[i].plot(averageAverageFitnessPerGen, label="Average", linewidth=3)
    axs[i].legend()
    axs[i].set_xlabel("Generation")
    axs[i].set_ylabel("Fitness")
    axs[i].set_title(runTitles[i])

matplotlib.pyplot.show()
    





# matplotlib.pyplot.legend()
# matplotlib.pyplot.xlabel("Generation")
# matplotlib.pyplot.ylabel("Fitness")
# matplotlib.pyplot.title("Average Fitnesses per Run")
# matplotlib.pyplot.show()
