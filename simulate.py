import math
import time
import pybullet as p
import pybullet_data
import pyrosim.pyrosim as pyrosim
import numpy as np
import random


SIM_LENGTH = 1000
PI = np.pi
physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())

p.setGravity(0, 0, -9.8)
planeId = p.loadURDF("plane.urdf")
robotId = p.loadURDF("robot.urdf")
p.loadSDF("world.sdf")

pyrosim.Prepare_To_Simulate(robotId)
backLegSensorValues = np.zeros(SIM_LENGTH)
frontLegSensorValues = np.zeros(SIM_LENGTH)

backAmplitude, backFrequency, backPhaseOffset = np.pi / 8, 10, 0
backTargetAngles = np.sin(np.linspace(0, 2*np.pi, SIM_LENGTH)
                          * backFrequency + backPhaseOffset) * backAmplitude
# np.save("data/backTargetAngles.npy", backTargetAngles)
frontAmplitude, frontFrequency, frontPhaseOffset = np.pi / 8, 10, np.pi / 4
frontTargetAngles = np.sin(np.linspace(0, 2*np.pi, SIM_LENGTH)
                           * frontFrequency + frontPhaseOffset) * frontAmplitude
# np.save("data/frontTargetAngles.npy", frontTargetAngles)


for i in range(SIM_LENGTH):
    pyrosim.Set_Motor_For_Joint(
        bodyIndex=robotId,
        jointName=b'Torso_BackLeg',
        controlMode=p.POSITION_CONTROL,
        targetPosition=backTargetAngles[i],
        maxForce=500.0)
    pyrosim.Set_Motor_For_Joint(
        bodyIndex=robotId,
        jointName=b'Torso_FrontLeg',
        controlMode=p.POSITION_CONTROL,
        targetPosition=frontTargetAngles[i],
        maxForce=500.0)

    p.stepSimulation()
    backLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")
    frontLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link(
        "FrontLeg")
    time.sleep(1./60.)
p.disconnect()


# Save the sensor values to a the data folder
np.save("data/backLegSensorValues.npy", backLegSensorValues)
np.save("data/frontLegSensorValues.npy", frontLegSensorValues)
