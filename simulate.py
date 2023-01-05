import time
import pybullet as p
import pybullet_data
import pyrosim.pyrosim as pyrosim
import numpy

SIM_LENGTH = 300
physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())

p.setGravity(0, 0, -9.8)
planeId = p.loadURDF("plane.urdf")
robotId = p.loadURDF("robot.urdf")
p.loadSDF("world.sdf")

pyrosim.Prepare_To_Simulate(robotId)
backLegSensorValues = numpy.zeros(SIM_LENGTH)
frontLegSensorValues = numpy.zeros(SIM_LENGTH)

for i in range(SIM_LENGTH):
    p.stepSimulation()
    backLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")
    frontLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link(
        "FrontLeg")
    time.sleep(1./60.)
p.disconnect()


# Save the sensor values to a the data folder
numpy.save("data/backLegSensorValues.npy", backLegSensorValues)
numpy.save("data/frontLegSensorValues.npy", frontLegSensorValues)
