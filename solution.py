import pickle
import shutil
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

        self.numLinks = np.random.randint(5, 10)
        
        self.numJoints = self.numLinks - 1
        self.sizes = np.random.uniform(0.3, 1, (self.numLinks, 3))
        # # Pick random locations for the sensors with 50% chance
        self.sensorLocations = np.random.choice([0,1,1], self.numLinks)
        self.linkNames = ["Head"]
        for i in range(1, self.numLinks):
            self.linkNames.append("Link" + str(i))

        # Create an acylcic directed graph representing the connections between links using joints as edges
        # The graph needs to also specify the face of the link that the joint is attached to
        # Each entry in the graph is a list of tuples, where each tuple is a link and the face of the link that the joint is attached to
        # Each link other than the head can connect to any other link
        # There can be no two links attached to the same face of the same link
        # The faces are +x, -x, +y, -y, +z, -z
        self.connectingNodes = {}
        self.availableFaces = {}
        self.availableNodes = ["Head"]
        for i in range(0, self.numLinks):
            self.connectingNodes[self.linkNames[i]] = []
            self.availableFaces[self.linkNames[i]] = ["+x", "-x", "+y", "-y", "+z", "-z"]
        for i in range(1, self.numLinks):
            # Pick a random link to connect to weighted by the number of available faces
            linkWeights = [len(self.availableFaces[name]) for name in self.linkNames if name != self.linkNames[i] and self.availableFaces[name] != [] and name in self.availableNodes]
            linkWeights = [weight / sum(linkWeights) for weight in linkWeights]
            linkToConnectTo = np.random.choice([name for name in self.linkNames if name != self.linkNames[i] and self.availableFaces[name] != [] and name in self.availableNodes], p=linkWeights)

            # linkToConnectTo = np.random.choice([name for name in self.linkNames if name != self.linkNames[i] and self.availableFaces[name] != [] and name in self.availableNodes])
            # Pick a random face to connect to
            faceToConnectTo = np.random.choice(self.availableFaces[linkToConnectTo])
            # Add the connection to the graph
            self.connectingNodes[linkToConnectTo].append((self.linkNames[i], faceToConnectTo))
            # Remove the face from the list of available faces
            self.availableFaces[linkToConnectTo].remove(faceToConnectTo)
            # Remove the node from the list of available nodes if there are no more available faces
            if self.availableFaces[linkToConnectTo] == []:
                self.availableNodes.remove(linkToConnectTo)
            # Remove the inverse of the face that the current link is connected to from the list of its own available faces
            self.availableFaces[self.linkNames[i]].remove(("-" if faceToConnectTo[0] == "+" else "+") + faceToConnectTo[1])
            # Add the node to available nodes
            self.availableNodes.append(self.linkNames[i])

        # Create a list of joints that will be used to create the joints in the robot
        # Each joint is a tuple of the form (link1, link2, jointType, axis, link1Face, link2Face)
        # link1 is the name of the link that the joint is attached to
        # link2 is the name of the link that the joint is attached to
        # jointType is the type of joint, which can be "fixed", "hinge", or "universal"
        # axis is the axis of rotation for the joint, which can be "x", "y", or "z"
        self.joints = []
        self.jointNames = []
        for link in self.connectingNodes.keys():
            for connection in self.connectingNodes[link]:
                # Pick a random joint type
                jointType = np.random.choice([ "revolute"]) #, "hinge", "universal"])
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

        self.lineage = []
    
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
            if time_spent > 3 and method == "DIRECT":
                print("Simulation " + str(self.myID) + " timed out")
                self.fitness = 0
                # Broken robot
                self.Save_To_Disk("brokenRobot", 0)
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
            # print("Sending sensor neuron " + str(nameCount) + " for sensor " + sensorName)
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
        # Mutate a link size randomly
        for i in range(self.numLinks):
            for j in range(3):
                if np.random.random() < c.MUTATION_RATE:
                    self.sizes[i][j] = np.random.uniform(0.3, 1)

        # Add or remove a link with 50% chance each
        if np.random.random() < c.MUTATION_RATE:
            # Add a link
            if np.random.random() < 0.5:
                self.Add_Link()
            # Remove a link
            else:
                # print("Before:")
                # print(self.linkNames)
                # print(self.jointNames)
                # print(self.availableNodes)
                # print(self.connectingNodes)
                self.Remove_Link()
                # print("After:")
                # print(self.linkNames)
                # print(self.jointNames)
                # print(self.availableNodes)
                # print(self.connectingNodes)
            self.Reset_Brain()
            self.Recreate_Simulation()
    
    def Reset_Brain(self):
        self.layerSizes = [len(self.sensorNames)]
        for i in range(c.NUM_HIDDEN_LAYERS):
            self.layerSizes.append(c.NUM_HIDDEN_NEURONS)
        self.layerSizes.append(len(self.jointNames))

        # Initialize the weights from the old weights but add random weights for the new links
        newWeights = []
        for i in range(len(self.layerSizes) - 1):
            newWeights.append(np.zeros((self.layerSizes[i], self.layerSizes[i + 1])))
            for j in range(self.layerSizes[i]):
                for k in range(self.layerSizes[i + 1]):
                    if i < len(self.weights) and j < len(self.weights[i]) and k < len(self.weights[i][j]):
                        newWeights[i][j][k] = self.weights[i][j][k]
                    else:
                        newWeights[i][j][k] = np.random.uniform(-1, 1)
        self.weights = newWeights
    
    def Add_Link(self):
        linkName = "Link" + str(self.numLinks)
        self.linkNames.append(linkName)
        size = np.random.uniform(0.3, 1, 3)
        self.sizes = np.concatenate((self.sizes, np.array([size])))
        self.availableFaces[linkName] = ["+x", "-x", "+y", "-y", "+z", "-z"]
        self.connectingNodes[linkName] = []
        # Pick a random link to connect to weighted by the number of available faces
        linkWeights = [len(self.availableFaces[name]) for name in self.linkNames if name != self.linkNames[-1] and self.availableFaces[name] != [] and name in self.availableNodes]
        linkWeights = [weight / sum(linkWeights) for weight in linkWeights]
        linkToConnectTo = np.random.choice([name for name in self.linkNames if name != self.linkNames[-1] and self.availableFaces[name] != [] and name in self.availableNodes], p=linkWeights)

        # Pick a random face to connect to
        faceToConnectTo = np.random.choice(self.availableFaces[linkToConnectTo])

        # Add the connection to the graph
        self.connectingNodes[linkToConnectTo].append((linkName, faceToConnectTo))
        # Remove the face from the list of available faces
        self.availableFaces[linkToConnectTo].remove(faceToConnectTo)
        # Remove the node from the list of available nodes if there are no more available faces
        if self.availableFaces[linkToConnectTo] == []:
            self.availableNodes.remove(linkToConnectTo)
        # Remove the inverse of the face that the current link is connected to from the list of its own available faces
        self.availableFaces[linkName].remove(("-" if faceToConnectTo[0] == "+" else "+") + faceToConnectTo[1])
        # Add the node to available nodes
        self.availableNodes.append(linkName)

        # Add the joint
        jointType = np.random.choice([ "revolute"]) #, "hinge", "universal"])
        # Pick a random axis
        axis = np.random.choice(["x", "y", "z"])
        # Determine the joint axis based on the face
        if faceToConnectTo == "+x" or faceToConnectTo == "-x":
            axis = "x"
        elif faceToConnectTo == "+y" or faceToConnectTo == "-y":
            axis = "y"
        elif faceToConnectTo == "+z" or faceToConnectTo == "-z":
            axis = "z"

        link1Face = faceToConnectTo
        link2Face = ("-" if faceToConnectTo[0] == "+" else "+") + faceToConnectTo[1]
        self.joints.append((linkToConnectTo, linkName,  jointType, axis, link1Face, link2Face))
        self.jointNames.append(linkToConnectTo + "_" + linkName)
        # Add it so sensor locartions with 50% chance
        if np.random.random() < 0.5:
            self.sensorLocations = np.concatenate((self.sensorLocations, np.array([1])))
            self.sensorNames.append(linkName)
        else:
            self.sensorLocations = np.concatenate((self.sensorLocations, np.array([0])))

        self.numLinks += 1

    def Remove_Link(self, linkToRemove=None):
        # Pick a random link to remove
        if linkToRemove == None:
            linkToRemove = np.random.choice([name for name in self.linkNames if name != "Head"])
            # print("randomly removing link " + linkToRemove)
        
            # print("Removing link " + linkToRemove)
        # Remove the link from the list of links
        # Remove the link from the list of available nodes
        self.availableNodes.remove(linkToRemove)
        # Remove the link from the list of sensor locations
        self.sensorLocations = np.delete(self.sensorLocations, self.linkNames.index(linkToRemove))
       # Remove the link from the list of sensor names if it is a sensor
        if linkToRemove in self.sensorNames:
            self.sensorNames.remove(linkToRemove)
        # Remove the link from the list of sizes
        self.sizes = np.delete(self.sizes, self.linkNames.index(linkToRemove), 0)
        self.linkNames.remove(linkToRemove)

        # Remove the link from its upstream links
        for link in self.connectingNodes:
            if link != linkToRemove:
                for connection in self.connectingNodes[link]:
                    if connection[0] == linkToRemove:
                        self.connectingNodes[link].remove(connection)
                        # Add the face to the list of available faces
                        self.availableFaces[link].append(connection[1])
                        # Add the node to the list of available nodes
                        self.availableNodes.append(link)

        # Remove the link from the list of joints
        for joint in self.joints:
            if joint[0] == linkToRemove or joint[1] == linkToRemove:
                self.joints.remove(joint)
                self.jointNames.remove(joint[0] + "_" + joint[1])
        # If the link has other links connected to it, remove those connections and connect the other links to the links connected to the removed link
        if self.connectingNodes[linkToRemove] != []:
            for link in self.connectingNodes[linkToRemove]:
                # print("Removing link " + link[0] + " connected to " + linkToRemove)
                
                self.Remove_Link(link[0])
        

        # Remove the link from the list of connecting nodes
        del self.connectingNodes[linkToRemove]
        del self.availableFaces[linkToRemove]


        self.numLinks -= 1
    

    def Recreate_Simulation(self):
        self.Create_World()
        self.Create_Robot()
        self.Create_Brain()

    def Set_ID(self, id):
        self.myID = id

    def Save_Sensor_Data(self):
        self.Start_Simulation("DIRECT", True)

    def Save_To_Disk(self, runName, currentGeneration):
        baseFolder = "./data/" + runName + "/solutions/"
        if not os.path.exists(baseFolder):
            os.makedirs(baseFolder)
        folder = baseFolder + str(currentGeneration) + "/"
        if not os.path.exists(folder):
            os.makedirs(folder)

        # Pickle the current solution object
        with open(folder + "solution" + str(self.myID) + ".pkl", "wb") as f:
            pickle.dump(self, f)
            f.close()
            

    def Save_Robot_Body(self, fileName):
        self.Create_Robot()
        # Copy the file into the folder
        shutil.copyfile("./robot" + str(self.myID) + ".urdf", fileName)

    def Save_Brain(self, fileName):
        self.Create_Brain()
        # Copy the file into the folder
        shutil.copyfile("./brain" + str(self.myID) + ".nndf", fileName)


