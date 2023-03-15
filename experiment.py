# Run search.py with a seed for 5 different seeds and wait for each of them to finish then graph the average fitnesses from data/runName

import pyrosim.pyrosim as pyrosim
import random
import math
import copy
import constants as c
import pickle
import matplotlib.pyplot as plt
import numpy as np
import os
import sys
import time
import datetime

# This file will create an exact replica of the data used for hill-climbing and afpo
for i in range(0,5):
    print("Starting Parallel HC run " + str(i))
    runName = "parallelHC-run-test-250-"
    os.system("python search.py " + str(i) + " " + runName + " parallel-hill-climber")
    while True:
        if os.path.exists("data/" + runName + str(i) + "/averageFitnesses.npy"):
            break
        time.sleep(10)

for i in range(0,5):
    print("Starting AFPO run " + str(i))
    runName = "AFPO-run-test-temp-250-"
    os.system("python search.py " + str(i) + " " + runName + " age-fitness-pareto-optimal")
    while True:
        if os.path.exists("data/" + runName + str(i) + "/averageFitnesses.npy"):
            break
        time.sleep(10)



