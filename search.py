import os
from parallelHillClimber import PARALLEL_HILL_CLIMBER

phc = PARALLEL_HILL_CLIMBER()
phc.Show_Random()
phc.Evolve()
# phc.Evolve_For_One_Generation()
# phc.Save_Best_Sensor_Data()
phc.Show_Best()
phc.Show_Fitness_Graph()
# phc.Save_Fitness_To_Disk()
os.system("rm fitness*.txt")
