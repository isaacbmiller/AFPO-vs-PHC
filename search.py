import os
import sys
from parallelHillClimber import PARALLEL_HILL_CLIMBER
import numpy as np

# Check if seed is in args
if len(sys.argv) > 1:
    np.random.seed(int(sys.argv[1]))
    name = str(sys.argv[2]) + str(sys.argv[1])
    selectionMethod = str(sys.argv[3])
else:
    np.random.seed(0)
    name = None
    selectionMethod="parallel-hill-climber"

phc = PARALLEL_HILL_CLIMBER(name, selectionMethod=selectionMethod)
# phc.Show_Random(num=10, text="Unevolved")

phc.Evolve()

# phc.Show_Best(num=10)

phc.Save_Robots_To_Disk()
phc.Save_Fitness_To_Disk()
# phc.Show_Fitness_Graph()
os.system("rm fitness*.txt")
