from simulation import SIMULATION
import sys

directOrGUI = sys.argv[1]
solutionID = sys.argv[2]
shouldSave = sys.argv[3]
if len(sys.argv) > 4:
    text = sys.argv[4]
else:
    text = None

if shouldSave == "True":
    shouldSave = True
else:
    shouldSave = False


simulation = SIMULATION(directOrGUI, solutionID, text)

simulation.Run()

if shouldSave:
    simulation.robot.Save_Values()

fitness = simulation.Get_Fitness()
