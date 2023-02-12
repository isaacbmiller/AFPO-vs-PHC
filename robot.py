import math
import os
from motor import MOTOR
from sensor import SENSOR
import pybullet as p
import pyrosim.pyrosim as pyrosim
from pyrosim.neuralNetwork import NEURAL_NETWORK
import constants as c


class ROBOT:
    def __init__(self, solutionID, saveValues=False):
        self.robotId = p.loadURDF("robot" + str(solutionID) + ".urdf")
        pyrosim.Prepare_To_Simulate(self.robotId)
        self.Prepare_To_Sense()
        self.Prepare_To_Act()
        self.saveValues = saveValues
        self.solutionID = solutionID
        self.nn = NEURAL_NETWORK("brain" + str(solutionID) + ".nndf")
        os.system("rm brain" + str(solutionID) + ".nndf")
        os.system("rm robot" + str(solutionID) + ".urdf")

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
            # if linkName == "Torso":
            #     self.sensors[linkName].Get_Value(timeStep, True, math.sin(timeStep))
            # else:
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
                # self.motors[encoded_joint_name].Set_Value(desiredAngle)
                self.motors[encoded_joint_name].Set_Value(desiredAngle, p.VELOCITY_CONTROL)

    def Get_Fitness(self):
        basePositionAndOrientation = p.getBasePositionAndOrientation(self.robotId)
        basePosition = basePositionAndOrientation[0]
        xPosition = basePosition[0]
        yPosition = basePosition[1]
        zPosition = basePosition[2]
        fitness = 0
        # Calculate the mean time that the torso is above the ground
        
        # torsoOffGround = - self.sensors["Torso"].values.mean()
        # fitness += torsoOffGround
        # Incentivize the robot to keep the lower legs on the ground but not the upper legs
        # lowerLegSensors = ["LowerFrontLeftLeg", "LowerFrontRightLeg", "LowerBackLeftLeg", "LowerBackRightLeg"]
        # upperLegSensors = ["FrontLeftLeg", "FrontRightLeg", "BackLeftLeg", "BackRightLeg"]
        # legIncentive = 0
        # for sensor in lowerLegSensors:
        #     legIncentive += self.sensors[sensor].values.mean()
        # for sensor in upperLegSensors:
        #     legIncentive -= self.sensors[sensor].values.mean()
        # legIncentive = legIncentive / 4
        # fitness += legIncentive

        
        # Make distance from the origin in the +x -y direction a fitness function
        if yPosition < 0:
            yPosition = 0
        if xPosition > 0:
            xPosition = 0
        distance = math.sqrt(xPosition**2 + yPosition**2)
        

        fitness += distance

        fitness = str(fitness)
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
