import numpy
import matplotlib.pyplot

# backLegSensorValues = numpy.load("data/backLegSensorValues.npy")
# frontLegSensorValues = numpy.load("data/frontLegSensorValues.npy")
# matplotlib.pyplot.plot(backLegSensorValues, linewidth=4.0)
# matplotlib.pyplot.plot(frontLegSensorValues, linewidth=4.0)
# matplotlib.pyplot.legend(["Back Leg", "Front Leg"])
# matplotlib.pyplot.show()

# matplotlib.pyplot.close()

# targetAngles = numpy.load("data/targetAngles.npy")
frontTargetAngles = numpy.load("data/frontTargetAngles.npy")
backTargetAngles = numpy.load("data/backTargetAngles.npy")
matplotlib.pyplot.plot(frontTargetAngles)
matplotlib.pyplot.plot(backTargetAngles)
matplotlib.pyplot.legend(["Front Target", "Back Target"])
matplotlib.pyplot.show()
