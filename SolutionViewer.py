import os
import pickle
import time

runName = "parallelHC-run-test3"

pickleFolder = "data/" + runName + "/solutions/" # Folder where the pickles are stored

# Generations to view (Multiples of 50)
generations = [0, 500]
robotsPerGeneration = 3

solutionDict = {}

for generation in generations:
    solutionDict[generation] = []
    
    # Read all solution*.pkl files in pickleFolder/generation/
    # Get list of all files in pickleFolder/generation/
    files = os.listdir(pickleFolder + str(generation))
    # Get list of all files in pickleFolder/generation/ that start with "solution" and end with ".pkl"
    files = [file for file in files if file.startswith("solution") and file.endswith(".pkl")]

    # Load all solutions
    for file in files:
        with open(pickleFolder + str(generation) + "/" + file, "rb") as f:
            solutionDict[generation].append(pickle.load(f))

    # sort solutionDict[generation] and keep the top robotsPerGeneration of them
    solutionDict[generation].sort(key=lambda x: x.fitness, reverse=True)
    solutionDict[generation] = solutionDict[generation][:robotsPerGeneration]

for generation in generations:
    print("Generation: " + str(generation))
    for i in range(robotsPerGeneration):
        print("Robot: " + str(i))
        print("Fitness: " + str(solutionDict[generation][i].fitness))
        solutionDict[generation][i].Start_Simulation("GUI")
        solutionDict[generation][i].Wait_For_Simulation_To_End("GUI")

    time.sleep(3)

        


        