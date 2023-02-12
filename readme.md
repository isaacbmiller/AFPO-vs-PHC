# Isaac Miller 
## Run Button

To run the code, you can clone the repo, switch to the 'final-project' branch, and run the following command:
```
python3 search.py
```

This will run the search algorithm and output the best robot it finds to the console along with show a visualization of the robot.
## Assignment 6

### Overview

The snakes seen in this experiment have the following qualities:
1. They are made up of a chain of links of a random length between 3 and 10.
2. Each link has a 66% chance of having a sensor attached to it.
3. The brain of the snake is a neural network with the sensored links as input and all link motors as output. The neural network has 3 hidden layers of 5 neurons each.
4. To mutate each brain, every neuron is mutated with a 10% chance of being mutated. The mutation is a random number between -1 and 1.
5. To mutate each body, 10% of the dimensions of each link are mutated to be a random number from 0.3 to 1.
6. The fitness function is the average distance from the center of the screen of the head of the snake in the +x and +y direction.


- [x] random number

- [x] randomly shaped links

- [X] random sensor placement along the chain.

- [x] Links with and without sensors should be colored green and blue, respectively.

## Video

[Youtube Link](https://youtu.be/DQLIAmM41Ck)

## Assignment 5

### Overview

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


## Video

Here is the gif of the robot evolving:

![gif](./396-Assignment-5.gif)