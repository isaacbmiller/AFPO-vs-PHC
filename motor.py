import constants as c
import numpy as np
import pyrosim.pyrosim as pyrosim
import pybullet as p


class MOTOR:
    def __init__(self, jointName, robotId):
        self.jointName = jointName
        self.robotId = robotId
        print(self.jointName)
        self.Prepare_To_Act()

    def Prepare_To_Act(self):
        self.amplitude = c.PI / 8
        self.frequency = 10
        self.phaseOffset = 0
        if self.jointName == b"Torso_FrontLeg":
            self.frequency = 5

        self.motorValues = np.sin(np.linspace(0, 2*np.pi, c.SIM_LENGTH)
                                  * self.frequency + self.phaseOffset) * self.amplitude

    def Set_Value(self, timeStep):
        self.value = self.motorValues[timeStep]
        pyrosim.Set_Motor_For_Joint(
            bodyIndex=self.robotId,
            jointName=self.jointName,
            controlMode=p.POSITION_CONTROL,
            targetPosition=self.motorValues[timeStep],
            maxForce=500.0)

    def Save_Values(self):
        np.save("data/" + self.jointName + "MotorValues.npy", self.motorValues)
