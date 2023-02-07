import constants as c
import numpy as np
import pyrosim.pyrosim as pyrosim
import pybullet as p


class MOTOR:
    def __init__(self, jointName, robotId):
        self.jointName = jointName
        self.robotId = robotId

    def Set_Value(self, desiredAngle, controlMode=p.POSITION_CONTROL):
        if controlMode == p.POSITION_CONTROL:
            pyrosim.Set_Motor_For_Joint(
                bodyIndex=self.robotId,
                jointName=self.jointName,
                controlMode=controlMode,
                targetPosition=desiredAngle * c.MOTOR_JOINT_RANGE,
                maxForce=30.0)
        else:
            pyrosim.Set_Motor_For_Joint(
                bodyIndex=self.robotId,
                jointName=self.jointName,
                controlMode=controlMode,
                targetVelocity=desiredAngle * 10,
                maxForce=500.0)
        
