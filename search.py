import os
from parallelHillClimber import PARALLEL_HILL_CLIMBER

phc = PARALLEL_HILL_CLIMBER()
phc.Show_Random(num=10, text="Unevolved")
exit()
phc.Evolve()
# phc.Evolve_For_One_Generation()
# phc.Save_Best_Sensor_Data()
phc.Show_Best()
# for i in range(5):
#     phc.Show_Random("Evolved")
phc.Show_Random(num=4, text="Evolved")
phc.Show_Fitness_Graph()
# phc.Save_Fitness_To_Disk()
os.system("rm fitness*.txt")
