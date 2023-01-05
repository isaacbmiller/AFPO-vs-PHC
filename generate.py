
import pyrosim.pyrosim as pyrosim

pyrosim.Start_SDF("boxes.sdf")
length, width, height = 1, 1, 1
x, y, z = 0, 0, height / 2

for x in range(-3, 3):
    for y in range(-3, 3):
        length, width, height = 1, 1, 1
        for z in range(0, 10):
            pyrosim.Send_Cube(name="Box", pos=[x, y, z], size=[
                              length, width, height])
            length *= 0.9
            width *= 0.9
            height *= 0.9
pyrosim.End()
