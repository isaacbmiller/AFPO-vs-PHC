import time
from robot import ROBOT
from world import WORLD

import pybullet as p
import pybullet_data
import pyrosim.pyrosim as pyrosim
import constants as c


class SIMULATION:
    def __init__(self, directOrGUI, solutionID):
        self.directOrGUI = directOrGUI
        self.solutionID = solutionID
        if directOrGUI == "GUI":
            self.physicsClient = p.connect(p.GUI)
        else:
            self.physicsClient = p.connect(p.DIRECT)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(0, 0, -9.8)

        self.world = WORLD()
        self.robot = ROBOT(solutionID)

    def Run(self):
        for i in range(c.SIM_LENGTH):
            p.stepSimulation()
            self.robot.Sense(i)
            self.robot.Think()
            self.robot.Act(i)
            if self.directOrGUI == "GUI":
                time.sleep(1./2000.)

    def Get_Fitness(self):
        return self.robot.Get_Fitness()

    def __del__(self):
        p.disconnect()
