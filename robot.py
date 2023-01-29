import os
from motor import MOTOR
from sensor import SENSOR
import pybullet as p
import pyrosim.pyrosim as pyrosim
from pyrosim.neuralNetwork import NEURAL_NETWORK
import constants as c


class ROBOT:
    def __init__(self, solutionID, saveValues=False):
        self.robotId = p.loadURDF("robot.urdf")
        pyrosim.Prepare_To_Simulate(self.robotId)
        self.Prepare_To_Sense()
        self.Prepare_To_Act()
        self.saveValues = saveValues
        self.solutionID = solutionID
        self.nn = NEURAL_NETWORK("brain" + str(solutionID) + ".nndf")
        os.system("rm brain" + str(solutionID) + ".nndf")

    def Prepare_To_Sense(self):
        self.sensors = {}
        for linkName in pyrosim.linkNamesToIndices:
            self.sensors[linkName] = SENSOR(linkName)

    def Prepare_To_Act(self):
        self.motors = {}
        for jointName in pyrosim.jointNamesToIndices:
            self.motors[jointName] = MOTOR(jointName, self.robotId)

    def Sense(self, timeStep):
        for linkName in self.sensors:
            self.sensors[linkName].Get_Value(timeStep)

    def Think(self):
        self.nn.Update()
        # self.nn.Print()

    def Act(self, timeStep):
        for neuronName in self.nn.neurons.keys():
            if self.nn.Is_Motor_Neuron(neuronName):
                jointName = self.nn.Get_Motor_Neurons_Joint(neuronName)
                desiredAngle = self.nn.Get_Value_Of(neuronName)
                desiredAngle = desiredAngle * c.MOTOR_JOINT_RANGE
                encoded_joint_name = jointName.encode('utf-8')
                self.motors[encoded_joint_name].Set_Value(desiredAngle)

    def Get_Fitness(self):
        stateOfLinkZero = p.getLinkState(self.robotId, 0)
        positionOfLinkZero = stateOfLinkZero[0]
        x = positionOfLinkZero[0]
        fitness = str(-x)
        f = open("tmp" + str(self.solutionID) + ".txt", "w")
        f.write(fitness)
        f.close()
        os.system("mv tmp" + str(self.solutionID) +
                  ".txt fitness" + str(self.solutionID) + ".txt")
        exit()

    def Save_Values(self):
        if self.saveValues:
            for linkName in self.sensors:
                self.sensors[linkName].Save_Values()
            for jointName in self.motors:
                self.motors[jointName].Save_Values()
