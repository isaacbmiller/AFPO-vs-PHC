import datetime
import random
import numpy as np
from solution import SOLUTION
import constants as c
import copy
import os
import matplotlib.pyplot as plt


class PARALLEL_HILL_CLIMBER():

    def __init__(self, runName=None, selectionMethod="parallel-hill-climber"):
        os.system("rm brain*.nndf")
        os.system("rm fitness*.txt")
        self.parents = {}
        self.nextAvailableID = 0
        for i in range(c.POPULATION_SIZE):
            self.parents[self.nextAvailableID] = SOLUTION(self.nextAvailableID)
            self.nextAvailableID += 1
        self.averageFitnesses = np.zeros(c.NUM_GENERATIONS)
        self.bestFitnesses = np.zeros(c.NUM_GENERATIONS)
        self.allFitnesses = np.zeros((c.POPULATION_SIZE, c.NUM_GENERATIONS))
        if runName is None:
            self.runName = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        else:
            self.runName = runName
        self.currentGeneration = 0


    def Evolve(self):
        print("Evolving")
        self.Evaluate(self.parents)
        print("Evaluated Parents")
        for currentGeneration in range(c.NUM_GENERATIONS):
            self.currentGeneration = currentGeneration
            if currentGeneration % 50 == 0:
                self.Save_Robots_To_Disk()
            self.Evolve_For_One_Generation(currentGeneration)
            self.Save_Current_Fitnesses(currentGeneration)

    def Evolve_For_One_Generation(self, currentGeneration):
        self.Spawn()
        # self.parents is a dictionary of solutions where solutions has a fitness
        # EDIT HERE
        self.Evaluate(self.parents)

        population = list(self.parents.values())
        non_domination_levels = self.non_dominated_sorting(population)
        non_domination_levels = self.crowding_distance(non_domination_levels)
        new_generation = self.create_next_generation(population=population, non_domination_levels=non_domination_levels)

        # For all of the parents that survived, keep them in the parents dictionary
        # Remove all of the parents that did not survive
        # Add the new children to the parents dictionary
        # Age all of the parents
        parentsToDel = []
        for parent in self.parents:
            if parent not in new_generation:
                parentsToDel.append(parent)
        for parent in parentsToDel:
            del self.parents[parent]

        for parent in self.parents:
            self.parents[parent].age += 1
        for child in new_generation:
            if child not in self.parents:
                self.parents[child.myID] = child
            

        # self.Mutate()
        
        # self.Print()
        self.Print_Status(currentGeneration)
        self.Print_Status(currentGeneration)
        
        # self.Select()

    def non_dominated_sorting(self, population):
        population_size = len(population)
        non_domination_level = []
        for i in range(population_size):
            dominated_individuals = []
            for j in range(population_size):
                if i == j:
                    continue
                if population[i].fitness <= population[j].fitness and population[i].age <= population[j].age:
                    dominated_individuals.append(j)
                elif population[j].fitness <= population[i].fitness and population[j].age <= population[i].age:
                    break
            if not dominated_individuals:
                non_domination_level.append([population[i]])
        if not non_domination_level:
            non_domination_level.append(population)
        return non_domination_level

    def crowding_distance(self, non_domination_levels):
        for level in non_domination_levels:
            n = len(level)
            if n == 0:
                continue
            elif n == 1:
                level[0].crowding_distance = np.inf
                continue
            elif n == 2:
                level[0].crowding_distance = np.inf
                level[1].crowding_distance = np.inf
                continue
            
            fitness_values = np.array([individual.fitness for individual in level])
            age_values = np.array([individual.age for individual in level])
            
            fitness_min, fitness_max = np.min(fitness_values), np.max(fitness_values)
            age_min, age_max = np.min(age_values), np.max(age_values)
            
            for i in range(n):
                level[i].crowding_distance = 0
                
            sort_index = np.argsort(fitness_values)
            level[sort_index[0]].crowding_distance = np.inf
            level[sort_index[n - 1]].crowding_distance = np.inf
            
            for i in range(1, n-1):
                level[sort_index[i]].crowding_distance += (fitness_values[sort_index[i + 1]] - fitness_values[sort_index[i - 1]]) / (fitness_max - fitness_min)
                
            sort_index = np.argsort(age_values)
            level[sort_index[0]].crowding_distance = np.inf
            level[sort_index[n - 1]].crowding_distance = np.inf
            
            for i in range(1, n-1):
                level[sort_index[i]].crowding_distance += (age_values[sort_index[i + 1]] - age_values[sort_index[i - 1]]) / (age_max - age_min)
                
        return non_domination_levels
    

    def select_next_generation(self, non_domination_levels):
        next_generation = []
        for level in non_domination_levels:
            if len(level) <= 2:
                next_generation.extend(level)
                continue
            
            level = sorted(level, key=lambda x: x.crowding_distance, reverse=True)
            next_generation.extend(level[:2])

        return next_generation
    
    def create_next_generation(self, population, non_domination_levels):
        selected_population = self.select_next_generation(non_domination_levels)
        next_generation = selected_population.copy()
        while len(next_generation) < len(population):
            individual = random.choice(selected_population)
            new_individual = copy.deepcopy(individual)
            new_individual.myID = self.nextAvailableID
            self.nextAvailableID += 1
            new_individual.age = 0
            new_individual.Mutate()
            next_generation.append(new_individual)
        return next_generation
    
    def Evaluate(self, solutions):
        for solution in solutions.values():
            solution.Start_Simulation("DIRECT")
        for solution in solutions.values():
            solution.Wait_For_Simulation_To_End("DIRECT")
            solution.Wait_For_Simulation_To_End("DIRECT")

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
            
    def Print_Status(self, currentGeneration):
        bestFitness = -1000
        self.bestParent = list(self.parents.values())[0]
        for key in self.parents.keys():
            if self.parents[key].fitness > bestFitness:
                self.bestParent = self.parents[key]
                bestFitness = self.parents[key].fitness
        averageFitness = 0
        for key in self.parents.keys():
            averageFitness += self.parents[key].fitness
        averageFitness /= len(self.parents)
        print("Generation: ", currentGeneration, " Best Fitness: ", bestFitness, " Average Fitness: ", averageFitness)

    def Show_Best(self):
        # print("\nShowing Best\n")
        # self.Evaluate(self.parents)
        bestFitness = -1000
        self.bestParent = list(self.parents.values())[0]
        averageFitness = 0
        for key in self.parents.keys():
            averageFitness += self.parents[key].fitness
        averageFitness /= len(self.parents)
        print("Generation: ", self.currentGeneration, " Best Fitness: ", bestFitness, " Average Fitness: ", averageFitness)

    def Show_Best(self, num=1):
        # Get the top num parents
        topParents = sorted(self.parents.values(), key=lambda x: x.fitness, reverse=True)[:num]
        for parent in topParents:
            parent.Start_Simulation("GUI")
            parent.Wait_For_Simulation_To_End("GUI")
            print("\nBest Parent Fitness: ", str(parent.fitness) + "\n")

    def Get_Random_Parent(self):
        randomParent = np.random.choice(list(self.parents.values()))
        randomParent.Start_Simulation("GUI")
        randomParent.Wait_For_Simulation_To_End("GUI")
        return randomParent.myID
    
    def Show_By_ID(self, idToTrack):
        hasShown = False
        for key in self.parents.keys():
            if self.parents[key].myID == idToTrack:
                self.parents[key].Start_Simulation("GUI")
                self.parents[key].Wait_For_Simulation_To_End("GUI")
                hasShown = True
                # print("\nTracked Parent Fitness: ", str(self.parents[key].fitness) + "\n")
        if not hasShown:
            for key in self.children.keys():
                if self.children[key].myID == idToTrack:
                    self.children[key].Start_Simulation("GUI")
                    self.children[key].Wait_For_Simulation_To_End("GUI")
                    hasShown = True
                    # print("\nTracked Child Fitness: ", str(self.children[key].fitness) + "\n")
        if not hasShown:
            print("\nID not found\n")

    def Show_Random(self, num=5, text=None):
        if len(self.parents) < num:
            num = len(self.parents)

        # Choose num unique random parents
        randomParents = np.random.choice(list(self.parents.values()), num, replace=False) 
        
        for randomParent in randomParents:
            randomParent.Start_Simulation("GUI", text)
            randomParent.Wait_For_Simulation_To_End("GUI")
    
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
        
    def Save_Fitness_To_Disk(self):
        # Save average and best fitnesses to separate files with a timestamp
        np.save(f"data/{self.runName}/averageFitnesses.npy", self.averageFitnesses)
        np.save(f"data/{self.runName}/bestFitnesses.npy", self.bestFitnesses)

    def Save_Robots_To_Disk(self):
        # Save all robots to disk
        for key in self.parents.keys():
            self.parents[key].Save_To_Disk(self.runName, self.currentGeneration)

    def Show_Fitness_Graph(self):
        plt.plot(self.averageFitnesses)
        plt.plot(self.bestFitnesses)
        # Graph all fitnesses as dots
        for i in range(c.POPULATION_SIZE):
            plt.plot(self.allFitnesses[i, :], "o", alpha=0.1)
        plt.legend(["Average Fitness", "Best Fitness"])
        plt.show()
