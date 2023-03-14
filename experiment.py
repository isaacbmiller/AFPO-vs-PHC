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


for i in range(1,5):
    print("Starting run " + str(i))
    runName = "parallelHC-run-test"
    os.system("python search.py " + str(i) + " " + runName + " parallel-hill-climber")
    while True:
        if os.path.exists("data/" + runName + str(i) + "/averageFitnesses.npy"):
            break
        time.sleep(10)

# Get the data from the files
data = []
for i in range(5):
    with open("data/run" + str(i) + "/averageFitnesses.npy", "rb") as f:
        data.append(np.load(f))

# Graph the data
# plt.plot(data[0], label="run0")
# plt.plot(data[1], label="run1")
# plt.plot(data[2], label="run2")
# plt.plot(data[3], label="run3")
# plt.plot(data[4], label="run4")
# plt.legend()
# plt.show()
