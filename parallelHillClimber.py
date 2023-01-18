from solution import SOLUTION
import constants as c
import copy
import os


class PARALLEL_HILL_CLIMBER():

    def __init__(self):
        # self.parent = SOLUTION()
        os.system("rm brain*.nndf")
        os.system("rm fitness*.txt")
        self.parents = {}
        self.nextAvailableID = 0
        for i in range(c.POPULATION_SIZE):
            self.parents[i] = SOLUTION(self.nextAvailableID)
            self.nextAvailableID += 1

    def Evolve(self):
        self.Evaluate(self.parents)
        for currentGeneration in range(c.NUM_GENERATIONS):
            self.Evolve_For_One_Generation()

    def Evolve_For_One_Generation(self):
        self.Spawn()
        self.Mutate()
        # self.child.Evaluate("DIRECT")
        self.Evaluate(self.children)
        self.Print()
        self.Select()
        # pass

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
            if self.parents[key].fitness < self.children[key].fitness:
                self.parents[key] = self.children[key]

    def Print(self):
        for key in self.parents.keys():
            print("\nParent Fitness: ", str(self.parents[key].fitness),
                  " Child Fitness: ", str(self.children[key].fitness) + "\n")

    def Show_Best(self):
        self.bestParent = list(self.parents.values())[0]
        for key in self.parents.keys():
            if self.parents[key].fitness > self.bestParent.fitness:
                self.bestParent = self.parents[key]
        self.bestParent.Start_Simulation("GUI")
        print("\nBest Parent Fitness: ", str(self.bestParent.fitness) + "\n")
