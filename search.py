import os
from parallelHillClimber import PARALLEL_HILL_CLIMBER
import numpy as np
np.random.seed(5)

phc = PARALLEL_HILL_CLIMBER()
phc.Show_Random(num=10, text="Unevolved")
# idToTrack = phc.Get_Random_Parent()

# idToTrack = phc.parents.keys()
# phc.Show_By_ID(idToTrack)
# phc.parents[idToTrack].Mutate()
phc.Evolve()
# phc.Show_By_ID(idToTrack)

phc.Show_Best(num=10)
# phc.Show_Random(num=4, text="Evolved")
# phc.Show_By_ID(idToTrack)

phc.Show_Fitness_Graph()
phc.Save_Fitness_To_Disk()
os.system("rm fitness*.txt")
