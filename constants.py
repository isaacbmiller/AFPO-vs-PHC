import math
import numpy as np

SIM_LENGTH = 1200
PI = np.pi

AMPLITUDE = PI / 8
FREQUENCY = 10
PHASE_OFFSET = 0

NUM_GENERATIONS = 250
POPULATION_SIZE = 20
SELECTION_SIZE = math.floor(POPULATION_SIZE / 2)

NUM_SENSORS = 9
NUM_MOTORS = 8

NUM_HIDDEN_NEURONS = 5
NUM_HIDDEN_LAYERS = 3

MOTOR_JOINT_RANGE = 0.45

MUTATION_RATE = 0.1

GUI_SIM_LENGTH_SECONDS = 1
WEIGHT_AGE = 0.2
WEIGHT_FITNESS = 1 - WEIGHT_AGE

# SELECTION_METHOD = 'parallel-hill-climber'  # 'parallel-hill-climber' or 'age-fitness-pareto-optimal'
SELECTION_METHOD = 'age-fitness-pareto-optimal'  # 'parallel-hill-climber' or 'age-fitness-pareto-optimal'