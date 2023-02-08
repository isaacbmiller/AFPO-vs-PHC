import time
import numpy as np
import pyrosim.pyrosim as pyrosim
import os
import constants as c


class SOLUTION():
    def __init__(self, parentID):
        # Initialize the weights based on c.NUM_SENSORS and c.NUM_MOTORS and c.NUM_HIDDEN_NEURONS and c.NUM_HIDDEN_LAYERS, but repeat the number of hidden neurons for each hidden layer
        self.layerSizes = [c.NUM_SENSORS]
        for i in range(c.NUM_HIDDEN_LAYERS):
            self.layerSizes.append(c.NUM_HIDDEN_NEURONS)
        self.layerSizes.append(c.NUM_MOTORS)
        
        self.weights = []
        for i in range(len(self.layerSizes) - 1):
            self.weights.append(np.random.uniform(-1, 1, (self.layerSizes[i], self.layerSizes[i + 1])))

        self.myID = parentID

        self.numLinks = np.random.randint(3, 10)
        self.numJoints = self.numLinks - 1
        self.sizes = np.random.uniform(0.3, 1, (self.numLinks, 3))
        # Pick random locations for the sensors with 50% chance
        self.sensorLocations = np.random.choice([0, 1,1], self.numLinks)
        self.linkNames = ["Head"]
        for i in range(1, self.numLinks):
            self.linkNames.append("Link" + str(i))
        self.age = 0
        self.sensorNames = []
        for i in range(0, self.numLinks):
            if self.sensorLocations[i] == 1:
                self.sensorNames.append(self.linkNames[i])

    def Start_Simulation(self, directOrGUI, saveValues=False):
        self.Create_World()
        self.Create_Robot()
        self.Create_Brain()
        os.system("python3 simulate.py " +
                  directOrGUI + " " + str(self.myID) + " " + str(saveValues) + " 2&>1 &")

    def Wait_For_Simulation_To_End(self, method="DIRECT"):
        time_spent = 0
        while not os.path.exists("fitness" + str(self.myID) + ".txt"):
            time.sleep(0.01)
            time_spent += 0.01
            if time_spent > 5 and method == "DIRECT":
                print("Simulation " + str(self.myID) + " timed out")
                self.fitness = 0
                return
            if time_spent > 10 and method == "GUI":
                print("Simulation " + str(self.myID) + " timed out")
                self.fitness = 0
                return
        f = open("fitness" + str(self.myID) + ".txt", "r")
        self.fitness = float(f.read())
        f.close()
        os.system("rm fitness" + str(self.myID) + ".txt")

    def Create_World(self):
        pyrosim.Start_SDF("world.sdf")
        pyrosim.End()
        return

    def Create_Robot(self):
        pyrosim.Start_URDF("robot" + str(self.myID) + ".urdf")
        # Generate initial xyz sizes between 0 and 3 blocks
        
        maxHeight = max(self.sizes[:, 2])
        lowerLimit = -np.pi/4
        upperLimit = np.pi/4

        pyrosim.Send_Cube(name="Head", pos=[0, self.sizes[0], maxHeight/2+self.sizes[0][2]/2], size=self.sizes[0], color=[1, 0, 0, 1], materialName="Red")

        for i in range(1,self.numLinks):
            if i == 1:
                jointHeight = maxHeight/2 #+self.sizes[i-1][2]/2
                yPosition = self.sizes[i-1][1]/2
            else:
                jointHeight = 0
                yPosition = self.sizes[i-1][1]
            isSensor = self.sensorLocations[i]
            if isSensor == 1:
                colorName = "Green"
                colorObj = [0, 1, 0, 1]
            else:
                colorName = "Cyan"
                colorObj = [0, 1, 1, 1]
            pyrosim.Send_Cube(name=self.linkNames[i], pos=[0, self.sizes[i][1]/2, 0], size=self.sizes[i], color=colorObj, materialName=colorName)
            pyrosim.Send_Joint(name=f"{self.linkNames[i-1]}_{self.linkNames[i]}", parent=self.linkNames[i-1], child=self.linkNames[i], type="revolute", position=[0, yPosition, jointHeight],  jointAxis=[1, 0, 0], lowerLimit=lowerLimit, upperLimit=upperLimit)
        

        pyrosim.End()
        return

    def Create_Brain(self):
        pyrosim.Start_NeuralNetwork("brain" + str(self.myID) + ".nndf")
        # Get the names of the sensors using sensorLocations

        # allSensorNames = ["Head"]
        
                # self.s.append("Link" + str(i))
        # Get sensorNames only at the location that have a 1 in sensorLocations
        # sensorNames = []
        # for sensorName in self.sensorNames:
        #     if self.sensorLocations[i] == 1:
        #         sensorNames.append(sensorName)


        nameCount = 0
        for sensorName in self.sensorNames:
            
            pyrosim.Send_Sensor_Neuron(name=nameCount, linkName=sensorName)
            nameCount += 1
        # for i in range(c.NUM_HIDDEN_LAYERS):
        #     for j in range(c.NUM_HIDDEN_NEURONS):
        #         pyrosim.Send_Hidden_Neuron(name=nameCount)
        #         nameCount += 1
        motorNames = []
        for i in range(self.numJoints - 2):
            motorNames.append(f"{self.linkNames[i]}_{self.linkNames[i+1]}")    

        for motorName in motorNames:
            pyrosim.Send_Motor_Neuron(name=nameCount, jointName=motorName)
            nameCount += 1
        
        neuronNameOffset = 0
        for i in range(len(self.layerSizes) - 1):
            for j in range(self.layerSizes[i]):
                for k in range(self.layerSizes[i + 1]):
                    pyrosim.Send_Synapse(sourceNeuronName=neuronNameOffset+j, targetNeuronName=neuronNameOffset + self.layerSizes[i] + k, weight=self.weights[i][j][k])

            neuronNameOffset += self.layerSizes[i]

        pyrosim.End()
    
        return

    def Mutate(self):
        self.Mutate_Brain()
        self.Mutate_Sizes()

    def Mutate_Brain(self):
        for i in range(len(self.layerSizes) - 1):
            for j in range(self.layerSizes[i]):
                for k in range(self.layerSizes[i + 1]):
                    if np.random.random() < c.MUTATION_RATE:
                        self.weights[i][j][k] = np.random.uniform(-1, 1)

    def Mutate_Sizes(self):
        for i in range(self.numLinks):
            for j in range(3):
                if np.random.random() < c.MUTATION_RATE:
                    self.sizes[i][j] = np.random.uniform(0.3, 1)

    def Set_ID(self, id):
        self.myID = id

    def Save_Sensor_Data(self):
        self.Start_Simulation("DIRECT", True)
