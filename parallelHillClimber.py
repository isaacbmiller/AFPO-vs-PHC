import datetime
import numpy as np
from solution import SOLUTION
import constants as c
import copy
import os
import matplotlib.pyplot as plt


class PARALLEL_HILL_CLIMBER():

    def __init__(self):
        os.system("rm brain*.nndf")
        os.system("rm fitness*.txt")
        self.parents = {}
        self.nextAvailableID = 0
        for i in range(c.POPULATION_SIZE):
            self.parents[i] = SOLUTION(self.nextAvailableID)
            self.nextAvailableID += 1
        self.averageFitnesses = np.zeros(c.NUM_GENERATIONS)
        self.bestFitnesses = np.zeros(c.NUM_GENERATIONS)
        self.allFitnesses = np.zeros((c.POPULATION_SIZE, c.NUM_GENERATIONS))


    def Evolve(self):
        print("Evolving")
        self.Evaluate(self.parents)
        print("Evaluated Parents")
        for currentGeneration in range(c.NUM_GENERATIONS):
            self.Evolve_For_One_Generation(currentGeneration)
            self.Save_Current_Fitnesses(currentGeneration)

    def Evolve_For_One_Generation(self, currentGeneration):
        self.Spawn()
        self.Mutate()
        self.Evaluate(self.children)
        # self.Print()
        self.Print_Best(currentGeneration)
        
        self.Select()

    def Evaluate(self, solutions):
        for solution in solutions.values():
            solution.Start_Simulation("DIRECT")
        for solution in solutions.values():
            solution.Wait_For_Simulation_To_End()

    def Spawn(self):
        self.children = {}
        for key in self.parents.keys():
            self.children[key] = copy.deepcopy(self.parents[key])
            self.children[key].Set_ID(self.nextAvailableID)
            self.nextAvailableID += 1

    def Mutate(self):
        for child in self.children.values():
            child.Mutate()

    def Select(self):
        for key in self.parents.keys():
            if self.children[key].fitness > self.parents[key].fitness:
                self.parents[key] = self.children[key]

    def Print(self):
        for key in self.parents.keys():
            print("\nParent Fitness: ", str(self.parents[key].fitness),
                  " Child Fitness: ", str(self.children[key].fitness) + "\n")
    def Print_Best(self, currentGeneration):
        bestFitness = -1000
        self.bestParent = list(self.parents.values())[0]
        for key in self.parents.keys():
            if self.parents[key].fitness > bestFitness:
                self.bestParent = self.parents[key]
                bestFitness = self.parents[key].fitness
        print("Generation: ", currentGeneration, " Best Fitness: ", bestFitness)

    def Show_Best(self):
        # print("\nShowing Best\n")
        # self.Evaluate(self.parents)
        bestFitness = -1000
        self.bestParent = list(self.parents.values())[0]
        for key in self.parents.keys():
            if self.parents[key].fitness > bestFitness:
                self.bestParent = self.parents[key]
                bestFitness = self.parents[key].fitness
        self.bestParent.Start_Simulation("GUI")
        print("\nBest Parent Fitness: ", str(self.bestParent.fitness) + "\n")

    def Show_Random(self):
        randomParent = np.random.choice(list(self.parents.values()))
        randomParent.Start_Simulation("GUI")
        randomParent.Wait_For_Simulation_To_End()
    
    def Save_Best_Sensor_Data(self):
        bestFitness = -1000
        self.bestParent = list(self.parents.values())[0]
        for key in self.parents.keys():
            if self.parents[key].fitness > bestFitness:
                self.bestParent = self.parents[key]
                bestFitness = self.parents[key].fitness
        self.bestParent.Save_Sensor_Data()

    def Save_Current_Fitnesses(self, currentGeneration):
        self.averageFitnesses[currentGeneration] = 0
        self.bestFitnesses[currentGeneration] = -1000
        for key in self.parents.keys():
            self.averageFitnesses[currentGeneration] += self.parents[key].fitness
            if self.parents[key].fitness > self.bestFitnesses[currentGeneration]:
                self.bestFitnesses[currentGeneration] = self.parents[key].fitness
        self.allFitnesses[:, currentGeneration] = [self.parents[key].fitness for key in self.parents.keys()]
        self.averageFitnesses[currentGeneration] /= c.POPULATION_SIZE
        # self.Save_Fitness_To_Disk()
        
    def Save_Fitness_To_Disk(self):
        # Save it in a file named fitness-currentDate-currentTime.
        np.save(f"data/averageFitnesses{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.npy", self.averageFitnesses)
        np.save(f"data/bestFitnesses{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.npy", self.bestFitnesses)

    def Show_Fitness_Graph(self):
        plt.plot(self.averageFitnesses)
        plt.plot(self.bestFitnesses)
        # Graph all fitnesses as dots
        for i in range(c.POPULATION_SIZE):
            plt.plot(self.allFitnesses[i, :], "o", alpha=0.1)
        plt.legend(["Average Fitness", "Best Fitness"])
        plt.show()
