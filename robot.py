from motor import MOTOR
from sensor import SENSOR
import pybullet as p
import pyrosim.pyrosim as pyrosim


class ROBOT:
    def __init__(self, saveValues=False):
        self.robotId = p.loadURDF("robot.urdf")
        pyrosim.Prepare_To_Simulate(self.robotId)
        self.Prepare_To_Sense()
        self.Prepare_To_Act()
        self.saveValues = saveValues

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

    def Act(self, timeStep):
        for jointName in self.motors:
            self.motors[jointName].Set_Value(timeStep)

    def Save_Values(self):
        if self.saveValues:
            for linkName in self.sensors:
                self.sensors[linkName].Save_Values()
            for jointName in self.motors:
                self.motors[jointName].Save_Values()
