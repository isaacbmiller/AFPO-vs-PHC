# Isaac Miller - Assignment 5

## Overview

What I decided to do with this project was to do the following objectives taken from the Ludobots reddit:
1. Sit. Good dog.

The robot I created is roughly modeled after the Boston dynamics dog.
It proved to be very difficult to get the robot to get its legs straight.
I exhibited selective pressure by having my fitness function encourage the robot to keep its upper legs off of the ground, its lower legs on the ground, and its torso off the ground.

2. Braniac
I implemented the neural network that was given to us in the assignment. I used the same fitness function as the previous objective.

From my testing, having the neural network does not make much if any of a performance difference. The beauty of neural networks is their ability to do backpropagation, which allows them to learn from their mistakes. However, in this case, the robot is not learning from its mistakes, it is just randomly searching the space and randomly mutating. This means that the robot is not learning from its mistakes, and therefore, the neural network is not helping it. There is also more dilution of neurons that can be mutated, and because of this, the robot is less likely to mutate into a better solution.

3. Not on the reddit

I did implement a custom mutator that scales with the number of weights in the neural network which helps to solve the issue of dilution. There is now a constant in the constants file called 'MUTATION_RATE' which is the probability that a weight will be mutated. This is multiplied by the number of weights in the neural network, so that the more weights there are, the more likely a weight will be mutated. This helps to solve the issue of dilution, but it does not solve the issue of the robot not learning from its mistakes.

## Run Button

To run the code, you can clone the repo, switch to the 'final-project' branch, and run the following command:
```
python3 search.py
```

This will run the search algorithm and output the best robot it finds to the console along with show a visualization of the robot.

## Video

Here is the gif of the robot evolving:

![gif](./396-Assignment-5.gif)