from FlightComputerSimulator import Simulator
import time
import matplotlib.pyplot as plt
from scipy.spatial.transform import Rotation as Rot #used for rotations 

startTime = time.time()
sim = Simulator()
alt = []
times = []
latA = []
longA = []
rotA = []

clock = 0
while clock < 3:

    clock = time.time() - startTime
    alti, lat, long, orientationQuat = sim.RunSim(clock)

    alt.append(alti)
    times.append(clock) 
    latA.append(lat)
    longA.append(long)

    rotation = Rot.from_quat(orientationQuat)
    rotationEuler = rotation.as_euler('xyz', degrees=True)
    zRot = rotationEuler[2]

    rotA.append(zRot)

#plt.plot(times, alt)
#plt.plot(longA,latA)
plt.plot(times, rotA)
plt.show()