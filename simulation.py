import time
from robot import ROBOT
from world import WORLD

import pybullet as p
import pybullet_data
import pyrosim.pyrosim as pyrosim
import constants as c

# Calculate how long the sim should sleep given c.GUI_SIM_LENGTH_SECONDS and c.SIM_LENGTH
SLEEP_LENGTH = (c.GUI_SIM_LENGTH_SECONDS / c.SIM_LENGTH) / 10000
class SIMULATION:
    def __init__(self, directOrGUI, solutionID, text=None):
        self.directOrGUI = directOrGUI
        self.solutionID = solutionID
        if directOrGUI == "GUI":
            self.physicsClient = p.connect(p.GUI)
        else:
            self.physicsClient = p.connect(p.DIRECT)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(0, 0, -9.8)
        self.text = text
        self.world = WORLD()
        self.robot = ROBOT(solutionID)

    def Run(self):
        position = [0, 0, 0.5]
        textSize = 0.01
        # Add the text to the screen
        if self.text is not None:
            p.addUserDebugText(self.text, textColorRGB=[0, 0, 0], textSize=textSize, textPosition=position)

        # Time how long it takes to run
        for i in range(c.SIM_LENGTH):
            p.stepSimulation()
            self.robot.Sense(i)
            self.robot.Think()
            self.robot.Act(i)
            if self.directOrGUI == "GUI":
                time.sleep(SLEEP_LENGTH)
        

    def Get_Fitness(self):
        return self.robot.Get_Fitness()

    def __del__(self):
        p.disconnect()
