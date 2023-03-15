import os
import pickle
import time
from solution import SOLUTION

runName = "parallelHC-run-test3"

pickleFolder = "data/brokenRobot/solutions/" # Folder where the pickles are stored

# Generations to view (Multiples of 50)
generations = [0, 500]
# robotsPerGeneration = 3

solutions: list[SOLUTION] = []
    
# Read all solution*.pkl files in pickleFolder/generation/
# Get list of all files in pickleFolder/generation/
files = os.listdir(pickleFolder + str(0))
# Get list of all files in pickleFolder/generation/ that start with "solution" and end with ".pkl"
files = [file for file in files if file.startswith("solution") and file.endswith(".pkl")]

# Load all solutions
# for file in files:
#     with open(pickleFolder + str(0) + "/" + file, "rb") as f:
#         solutions.append(pickle.load(f))
os.system("rm brain*.nndf")
os.system("rm robot*.urdf")
# Load individual
with open(pickleFolder + str(0) + "/" + "solution943.pkl", "rb") as f:
        solutions.append(pickle.load(f))
# sort solutionDict[generation] and keep the top robotsPerGeneration of them
# solutions.sort(key=lambda x: x.fitness, reverse=True)
solutions.sort(key=lambda x: x.age)


for solution in solutions:
    print("Fitness: " + str(solution.fitness))
    print("Lineage: " + str(solution.lineage))
    solution.Start_Simulation("GUI")
    solution.Wait_For_Simulation_To_End("GUI")
    solution.Save_Robot_Body("brokenBot.urdf")
    solution.Save_Brain("brokenBrain.nndf")

    x = input("Press enter to continue")
    print()

#         solutionDict[generation][i].Start_Simulation("GUI")
#         solutionDict[generation][i].Wait_For_Simulation_To_End("GUI")
# for generation in generations:
#     print("Generation: " + str(generation))
#     for i in range(robotsPerGeneration):
#         print("Robot: " + str(i))
#         print("Fitness: " + str(solutionDict[generation][i].fitness))
#         solutionDict[generation][i].Start_Simulation("GUI")
#         solutionDict[generation][i].Wait_For_Simulation_To_End("GUI")

#     time.sleep(3)

        


        