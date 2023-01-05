import time
import pybullet as p

physicsClient = p.connect(p.GUI)
p.loadSDF("box.sdf")
for i in range(1000):
    print(i)
    p.stepSimulation()
    time.sleep(1./60.)
p.disconnect()
