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

    def Start_Simulation(self, directOrGUI, saveValues=False):
        self.Create_World()
        self.Create_Robot()
        self.Create_Brain()
        os.system("python3 simulate.py " +
                  directOrGUI + " " + str(self.myID) + " " + str(saveValues) + " 2&>1 &")

    def Wait_For_Simulation_To_End(self):
        while not os.path.exists("fitness" + str(self.myID) + ".txt"):
            time.sleep(0.01)
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
        pyrosim.Send_Cube(name="Torso", pos=[0, 0, 1.25], size=[2, 1, 0.5])
        
        # Create a version of SpotMini, the dog from Boston Dynamics
        # lowerLimit = -np.pi/4
        # upperLimit = np.pi/4
        lowerLimit = 0
        upperLimit = 0

        # Create the back left leg
        pyrosim.Send_Cube(name="BackLeftLeg", pos=[0, 0, -0.25], size=[0.1, 0.1, 0.5], materialName="asd", color=[0, 0, 1, 1])
        pyrosim.Send_Joint(name="Torso_BackLeftLeg", parent="Torso", child="BackLeftLeg", type="revolute", jointAxis="0 1 0", position=[0.75, -0.5+-0.05, 1.125])

        # Create the lower left leg
        pyrosim.Send_Cube(name="LowerBackLeftLeg", pos=[0, 0, -0.25], size=[0.1, 0.1, 0.5], materialName="asd3", color=[0, 0, 1, 0.5])
        pyrosim.Send_Joint(name="BackLeftLeg_LowerBackLeftLeg", parent="BackLeftLeg", child="LowerBackLeftLeg", type="revolute", jointAxis="0 1 0", position=[0, 0, -0.5])

        # Create the back right leg
        pyrosim.Send_Cube(name="BackRightLeg", pos=[0, 0, -0.25], size=[0.1, 0.1, 0.5]) 
        pyrosim.Send_Joint(name="Torso_BackRightLeg", parent="Torso", child="BackRightLeg", type="revolute", jointAxis="0 1 0", position=[0.75, 0.5+0.05, 1.125])

        # Create the back right leg
        pyrosim.Send_Cube(name="LowerBackRightLeg", pos=[0, 0, -0.25], size=[0.1, 0.1, 0.5])
        pyrosim.Send_Joint(name="BackRightLeg_LowerBackRightLeg", parent="BackRightLeg", child="LowerBackRightLeg", type="revolute", jointAxis="0 1 0", position=[0, 0, -0.5])

        # Create the front left leg
        pyrosim.Send_Cube(name="FrontLeftLeg", pos=[0, 0, -0.25], size=[0.1, 0.1, 0.5], materialName="asd2", color=[1, 0, 1, 1])
        pyrosim.Send_Joint(name="Torso_FrontLeftLeg", parent="Torso", child="FrontLeftLeg", type="revolute", jointAxis="0 1 0", position=[-0.75, -0.5+-0.05, 1.125])

        # Create the lower front left leg
        pyrosim.Send_Cube(name="LowerFrontLeftLeg", pos=[0, 0, -0.25], size=[0.1, 0.1, 0.5])
        pyrosim.Send_Joint(name="FrontLeftLeg_LowerFrontLeftLeg", parent="FrontLeftLeg", child="LowerFrontLeftLeg", type="revolute", jointAxis="0 1 0", position=[0, 0, -0.5])

        # Create the front right leg
        pyrosim.Send_Cube(name="FrontRightLeg", pos=[0, 0, -0.25], size=[0.1, 0.1, 0.5])
        pyrosim.Send_Joint(name="Torso_FrontRightLeg", parent="Torso", child="FrontRightLeg", type="revolute", jointAxis="0 1 0", position=[-0.75, 0.5+0.05, 1.125])

        # Create the lower front right leg
        pyrosim.Send_Cube(name="LowerFrontRightLeg", pos=[0, 0, -0.25], size=[0.1, 0.1, 0.5])
        pyrosim.Send_Joint(name="FrontRightLeg_LowerFrontRightLeg", parent="FrontRightLeg", child="LowerFrontRightLeg", type="revolute", jointAxis="0 1 0", position=[0, 0, -0.5])

        pyrosim.End()
        return

    def Create_Brain(self):
        pyrosim.Start_NeuralNetwork("brain" + str(self.myID) + ".nndf")
        sensorNames = ["Torso","LowerBackLeftLeg", "LowerBackRightLeg", "LowerFrontLeftLeg", "LowerFrontRightLeg", "FrontLeftLeg", "FrontRightLeg", "BackLeftLeg", "BackRightLeg"]
        nameCount = 0
        for sensorName in sensorNames:
            
            pyrosim.Send_Sensor_Neuron(name=nameCount, linkName=sensorName)
            nameCount += 1
        for i in range(c.NUM_HIDDEN_LAYERS):
            for j in range(c.NUM_HIDDEN_NEURONS):
                pyrosim.Send_Hidden_Neuron(name=nameCount)
                nameCount += 1
        motorNames = ["Torso_FrontLeftLeg", "Torso_FrontRightLeg", "Torso_BackLeftLeg", "Torso_BackRightLeg", "FrontLeftLeg_LowerFrontLeftLeg", "FrontRightLeg_LowerFrontRightLeg", "BackLeftLeg_LowerBackLeftLeg", "BackRightLeg_LowerBackRightLeg"]
        for motorName in motorNames:
            pyrosim.Send_Motor_Neuron(name=nameCount, jointName=motorName)
            nameCount += 1
         #]
        neuronNameOffset = 0
        for i in range(len(self.layerSizes) - 1):
            for j in range(self.layerSizes[i]):
                for k in range(self.layerSizes[i + 1]):
                    pyrosim.Send_Synapse(sourceNeuronName=neuronNameOffset+j, targetNeuronName=neuronNameOffset + self.layerSizes[i] + k, weight=self.weights[i][j][k])

            neuronNameOffset += self.layerSizes[i]


        # for currentRow in range(c.NUM_SENSORS):
        #     for currentColumn in range(c.NUM_MOTORS):
        #         pyrosim.Send_Synapse(sourceNeuronName=currentRow,
        #                              targetNeuronName=c.NUM_SENSORS+currentColumn, weight=self.weights[currentRow][currentColumn])

        pyrosim.End()
    
        return

    def Mutate(self):
        for i in range(len(self.layerSizes) - 1):
            for j in range(self.layerSizes[i]):
                for k in range(self.layerSizes[i + 1]):
                    if np.random.random() < c.MUTATION_RATE:
                        self.weights[i][j][k] = np.random.uniform(-1, 1)

    def Set_ID(self, id):
        self.myID = id

    def Save_Sensor_Data(self):
        self.Start_Simulation("DIRECT", True)
