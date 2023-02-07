from simulation import SIMULATION
import sys

directOrGUI = sys.argv[1]
solutionID = sys.argv[2]
shouldSave = sys.argv[3]
if shouldSave == "True":
    shouldSave = True
elif shouldSave == "False":
    shouldSave = False
else:
    print("Error: shouldSave must be True or False")
    exit()

simulation = SIMULATION(directOrGUI, solutionID)

simulation.Run()

if shouldSave:
    simulation.robot.Save_Values()

fitness = simulation.Get_Fitness()
