import os
import pickle
import time

# baseRunName = "AFPO-run-test-250-"
baseRunName = "parallelHC-run-test-250-"
# runName = "parallelHC-run-test-250-"
# runNames = ["AFPO-run-test-250-", "parallelHC-run-test-250-"]
runNames = [baseRunName + str(i) for i in range(0,5)]

# Generations to view (Multiples of 50)
generations = [0, 250]
robotsPerGeneration = 3
runDict = {}
for runName in runNames:
    pickleFolder = "data/" + runName + "/solutions/" # Folder where the pickles are stored
    runDict[runName] = {}
    for generation in generations:
        runDict[runName][generation] = []
        
        # Read all solution*.pkl files in pickleFolder/generation/
        # Get list of all files in pickleFolder/generation/
        files = os.listdir(pickleFolder + str(generation))
        # Get list of all files in pickleFolder/generation/ that start with "solution" and end with ".pkl"
        files = [file for file in files if file.startswith("solution") and file.endswith(".pkl")]

        # Load all solutions
        for file in files:
            with open(pickleFolder + str(generation) + "/" + file, "rb") as f:
                runDict[runName][generation].append(pickle.load(f))

        # sort solutionDict[generation] and keep the top robotsPerGeneration of them
        # for solution in runDict[runName][generation]:
        #         solution.Start_Simulation("DIRECT")
        # for solution in runDict[runName][generation]:
        #     solution.Wait_For_Simulation_To_End("DIRECT")
        runDict[runName][generation].sort(key=lambda x: x.fitness, reverse=True)
        runDict[runName][generation] = runDict[runName][generation][:robotsPerGeneration]

# print(runDict)
# for generation in generations:
#     print("Generation: " + str(generation))
#     for i in range(robotsPerGeneration):
#         print("Robot: " + str(i))
#         print("Fitness: " + str(solutionDict[generation][i].fitness))
#         solutionDict[generation][i].Start_Simulation("GUI")
#         solutionDict[generation][i].Wait_For_Simulation_To_End("GUI")

#     time.sleep(1)

# get all of the 0 generation solutions and sort them by fitness
gen0Solutions = []
for runName in runNames:
    gen0Solutions.extend(runDict[runName][0])
gen0Solutions.sort(key=lambda x: x.fitness)
gen0Solutions = [solution for solution in gen0Solutions if solution.fitness > 0]

# get all of the 250 generation solutions and sort them by fitness
gen250Solutions = []
for runName in runNames:
    gen250Solutions.extend(runDict[runName][250])
gen250Solutions.sort(key=lambda x: x.fitness, reverse=True)

# Display 10 solutions per generation
for i in range(10):
    print("Generation 0 Robot " + str(i) + " Fitness: " + str(gen0Solutions[i].fitness))
    gen0Solutions[i].Start_Simulation("GUI")
    gen0Solutions[i].Wait_For_Simulation_To_End("GUI")
    time.sleep(3)

time.sleep(3)

for i in range(10):
    print("Generation 250 Robot " + str(i) + " Fitness: " + str(gen250Solutions[i].fitness))
    gen250Solutions[i].Start_Simulation("GUI")
    gen250Solutions[i].Wait_For_Simulation_To_End("GUI")
    time.sleep(1)

        


        