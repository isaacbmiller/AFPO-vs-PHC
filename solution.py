import time
import numpy as np
import pyrosim.pyrosim as pyrosim
import os
import constants as c


class SOLUTION():
    def __init__(self, parentID):
        # Initialize the weights based on c.NUM_SENSORS and c.NUM_MOTORS and c.NUM_HIDDEN_NEURONS and c.NUM_HIDDEN_LAYERS, but repeat the number of hidden neurons for each hidden layer
        self.layerSizes = [c.NUM_SENSORS]
        for i in range(c.NUM_HIDDEN_LAYERS):
            self.layerSizes.append(c.NUM_HIDDEN_NEURONS)
        self.layerSizes.append(c.NUM_MOTORS)
        
        self.weights = []
        for i in range(len(self.layerSizes) - 1):
            self.weights.append(np.random.uniform(-1, 1, (self.layerSizes[i], self.layerSizes[i + 1])))

        self.myID = parentID

        self.numLinks = np.random.randint(3, 10)
        
        self.numJoints = self.numLinks - 1
        self.sizes = np.random.uniform(0.7, 0.7, (self.numLinks, 3))
        # # Pick random locations for the sensors with 50% chance
        self.sensorLocations = np.random.choice([0, 1,1], self.numLinks)
        self.linkNames = ["Head"]
        for i in range(1, self.numLinks):
            self.linkNames.append("Link" + str(i))

        # Create an acylcic directed graph representing the connections between links using joints as edges
        # The graph needs to also specify the face of the link that the joint is attached to
        # Each entry in the graph is a list of tuples, where each tuple is a link and the face of the link that the joint is attached to
        # Each link other than the head can connect to any other link
        # There can be no two links attached to the same face of the same link
        # The faces are +x, -x, +y, -y, +z, -z
        connectingNodes = {}
        availableFaces = {}
        availableNodes = ["Head"]
        for i in range(0, self.numLinks):
            connectingNodes[self.linkNames[i]] = []
            availableFaces[self.linkNames[i]] = ["+x", "-x", "+y", "-y", "+z", "-z"]
        for i in range(1, self.numLinks):
            # Pick a random link to connect to weighted by the number of available faces
            linkWeights = [len(availableFaces[name]) for name in self.linkNames if name != self.linkNames[i] and availableFaces[name] != [] and name in availableNodes]
            linkWeights = [weight / sum(linkWeights) for weight in linkWeights]
            linkToConnectTo = np.random.choice([name for name in self.linkNames if name != self.linkNames[i] and availableFaces[name] != [] and name in availableNodes], p=linkWeights)

            # linkToConnectTo = np.random.choice([name for name in self.linkNames if name != self.linkNames[i] and availableFaces[name] != [] and name in availableNodes])
            # Pick a random face to connect to
            faceToConnectTo = np.random.choice(availableFaces[linkToConnectTo])
            # Add the connection to the graph
            connectingNodes[linkToConnectTo].append((self.linkNames[i], faceToConnectTo))
            # Remove the face from the list of available faces
            availableFaces[linkToConnectTo].remove(faceToConnectTo)
            # Remove the node from the list of available nodes if there are no more available faces
            if availableFaces[linkToConnectTo] == []:
                availableNodes.remove(linkToConnectTo)
            # Remove the inverse of the face that the current link is connected to from the list of its own available faces
            availableFaces[self.linkNames[i]].remove(("-" if faceToConnectTo[0] == "+" else "+") + faceToConnectTo[1])
            # Add the node to available nodes
            availableNodes.append(self.linkNames[i])

        # Create a list of joints that will be used to create the joints in the robot
        # Each joint is a tuple of the form (link1, link2, jointType, axis, link1Face, link2Face)
        # link1 is the name of the link that the joint is attached to
        # link2 is the name of the link that the joint is attached to
        # jointType is the type of joint, which can be "fixed", "hinge", or "universal"
        # axis is the axis of rotation for the joint, which can be "x", "y", or "z"
        self.joints = []
        self.jointNames = []
        for link in connectingNodes.keys():
            for connection in connectingNodes[link]:
                # Pick a random joint type
                jointType = np.random.choice([ "revolute"]) #, "fixed", "hinge", "universal"])
                # Pick a random axis
                axis = np.random.choice(["x", "y", "z"])
                faceToConnectTo = connection[1]
                # Determine the joint axis based on the face
                if faceToConnectTo == "+x" or faceToConnectTo == "-x":
                    axis = "x"
                elif faceToConnectTo == "+y" or faceToConnectTo == "-y":
                    axis = "y"
                elif faceToConnectTo == "+z" or faceToConnectTo == "-z":
                    axis = "z"
                link1Face = connection[1]
                link2Face = ("-" if connection[1][0] == "+" else "+") + connection[1][1]
                self.joints.append((link, connection[0], jointType, axis, link1Face, link2Face))
                self.jointNames.append(link + "_" + connection[0])


        
        self.age = 0
        self.sensorNames = []
        for i in range(0, self.numLinks):
            if self.sensorLocations[i] == 1:
                self.sensorNames.append(self.linkNames[i])
    
    def Create_Robot(self):
        pyrosim.Start_URDF("robot" + str(self.myID) + ".urdf")
        # Generate initial xyz sizes between 0 and 3 blocks
        
        maxHeight = max(self.sizes[:, 2])
        lowerLimit = -np.pi/4
        upperLimit = np.pi/4

        pyrosim.Send_Cube(name="Head", pos=[0, 0, 2], size=self.sizes[0], color=[1, 0, 0, 0.8], materialName="Red")# +self.sizes[0][2]/2

        # Do a depth first search to create the robot
        stack = ["Head"]
        while len(stack) > 0:
            currentNode = stack.pop(0)
            for i in range(0, len(self.joints)):
                if self.joints[i][0] == currentNode:
                    #Special case for the head

                    # calculate the position of the joint based on the size of the links and the connection face
                    face = self.joints[i][4]
                    multiplier = 1
                    offsetPosition = 0
                    if face[0] == "+":
                        multiplier = 1
                    elif face[0] == "-":
                        multiplier = -1

                    if face[1] == "x":
                        offsetPosition = 0
                    elif face[1] == "y":
                        offsetPosition = 1
                    elif face[1] == "z":
                        offsetPosition = 2
                    base = (self.sizes[self.linkNames.index(self.joints[i][0])][offsetPosition] + self.sizes[self.linkNames.index(self.joints[i][1])][offsetPosition])/2
                    offset = multiplier*(base)
                    position = [0, 0, 0]
                    position[offsetPosition] = offset

                    if currentNode == "Head":
                        position[2] += 2

                    # Create the joint
                    axis = [0, 0, 0]
                    if self.joints[i][3] == "x":
                        axis[0] = 1
                    elif self.joints[i][3] == "y":
                        axis[1] = 1
                    elif self.joints[i][3] == "z":
                        axis[2] = 1

                    # print("Creating joint " + self.joints[i][0] + "_" + self.joints[i][1] + " at position " + str(position) + " with axis " + str(axis) + " and parent " + self.joints[i][0] + " and child " + self.joints[i][1])
                    # print("Head size: " + str(self.sizes[0]))
                    # print("Head position: " + str([0, 0, 2]))
                    # print("Link size: " + str(self.sizes[self.linkNames.index(self.joints[i][1])]))
                    # print("Link position: " + str(position))

                    # Change the material and color if the joint has a sensor
                    if self.joints[i][1] in self.sensorNames:
                        color = [0, 1, 0, 0.8]
                        material = "Green"
                    else:
                        color = [0, 0, 1, 0.8]
                        material = "Blue"

                    pyrosim.Send_Cube(name=self.joints[i][1], pos=[0, 0, 0], size=self.sizes[self.linkNames.index(self.joints[i][1])], color=color, materialName=material)

                    pyrosim.Send_Joint(name=self.joints[i][0] + "_" + self.joints[i][1], parent=self.joints[i][0], child=self.joints[i][1], type=self.joints[i][2], position=position, jointAxis=axis, upperLimit=upperLimit, lowerLimit=lowerLimit)
                    # Add the child node to the stack
                    stack.append(self.joints[i][1])

        pyrosim.End()
        return

    def Start_Simulation(self, directOrGUI, saveValues=False, text=""):
        self.Create_World()
        self.Create_Robot()
        self.Create_Brain()
        os.system("python3 simulate.py " +
                  directOrGUI + " " + str(self.myID) + " " + str(saveValues) + " " + str(text) + " 2&>1 &")

    def Wait_For_Simulation_To_End(self, method="DIRECT"):
        time_spent = 0
        while not os.path.exists("fitness" + str(self.myID) + ".txt"):
            time.sleep(0.01)
            time_spent += 0.01
            if time_spent > 5 and method == "DIRECT":
                print("Simulation " + str(self.myID) + " timed out")
                self.fitness = 0
                return
            if time_spent > 10 and method == "GUI":
                print("Simulation " + str(self.myID) + " timed out")
                self.fitness = 0
                return
        f = open("fitness" + str(self.myID) + ".txt", "r")
        self.fitness = float(f.read())
        f.close()
        os.system("rm fitness" + str(self.myID) + ".txt")

    def Create_World(self):
        pyrosim.Start_SDF("world.sdf")
        pyrosim.End()
        return


    def Create_Brain(self):
        pyrosim.Start_NeuralNetwork("brain" + str(self.myID) + ".nndf")

        nameCount = 0
        for sensorName in self.sensorNames:
            
            pyrosim.Send_Sensor_Neuron(name=nameCount, linkName=sensorName)
            nameCount += 1

        for i in range(c.NUM_HIDDEN_LAYERS):
            for j in range(c.NUM_HIDDEN_NEURONS):
                pyrosim.Send_Hidden_Neuron(name=nameCount)
                nameCount += 1   

        for jointName in self.jointNames:
            pyrosim.Send_Motor_Neuron(name=nameCount, jointName=jointName)
            nameCount += 1
        
        neuronNameOffset = 0
        for i in range(len(self.layerSizes) - 1):
            for j in range(self.layerSizes[i]):
                for k in range(self.layerSizes[i + 1]):
                    pyrosim.Send_Synapse(sourceNeuronName=neuronNameOffset+j, targetNeuronName=neuronNameOffset + self.layerSizes[i] + k, weight=self.weights[i][j][k])

            neuronNameOffset += self.layerSizes[i]

        pyrosim.End()
    
        return

    def Mutate(self):
        self.Mutate_Brain()
        self.Mutate_Sizes()

    def Mutate_Brain(self):
        for i in range(len(self.layerSizes) - 1):
            for j in range(self.layerSizes[i]):
                for k in range(self.layerSizes[i + 1]):
                    if np.random.random() < c.MUTATION_RATE:
                        self.weights[i][j][k] = np.random.uniform(-1, 1)

    def Mutate_Sizes(self):
        for i in range(self.numLinks):
            for j in range(3):
                if np.random.random() < c.MUTATION_RATE:
                    self.sizes[i][j] = np.random.uniform(0.3, 1)

    def Set_ID(self, id):
        self.myID = id

    def Save_Sensor_Data(self):
        self.Start_Simulation("DIRECT", True)
