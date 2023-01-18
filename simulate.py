import math
import time
import pybullet as p
import pybullet_data
import pyrosim.pyrosim as pyrosim
import numpy as np
import random
import constants as c
from simulation import SIMULATION
import sys

directOrGUI = sys.argv[1]

simulation = SIMULATION(directOrGUI)

simulation.Run()

fitness = simulation.Get_Fitness()
