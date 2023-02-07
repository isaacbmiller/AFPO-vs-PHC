import os
from parallelHillClimber import PARALLEL_HILL_CLIMBER

phc = PARALLEL_HILL_CLIMBER()
phc.Evolve()
# phc.Evolve_For_One_Generation()
# phc.Save_Best_Sensor_Data()
phc.Show_Best()
os.system("rm fitness*.txt")
