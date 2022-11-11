import random
import time
import scipy.integrate as integrate
from scipy.spatial.transform import Rotation as Rot #used for rotations 

flying = True

class Simulator:

    def __init__(self):

        #Defualt values
        #All
        self.lastTime = 0 # seconds
        #Alt
        self.altitude = 0 #meters
        self.u = 0 # m/s
        self.ImpulseTime = 3.2 # seconds
        #GPS
        self.lat = 50
        self.latConst = 0.0000159214
        self.long = -5
        self.longConst = -0.0000569214
        #IMU
        self.orientation = Rot.from_euler('z', 90, degrees=True)
        self.orientationQuat = None
        self.zRotationRate = 90 # degree per second
        

        return

    def IMU(self, clock):

        #IMU will output:
        #-Linear Acceleration in all three dimensions
        #-Rotation as a quternion

        zChange = self.zRotationRate * self.timeStep

        self.orientation *= Rot.from_euler('z', zChange, degrees = True)

        self.orientationQuat = self.orientation.as_quat()


        return

    def Altimiter(self, clock):
        
        #Simply outputs a hight value
        #To simulate a rocket this needs to have a short boost stage, then be subjected to the whims of gravity
        if clock < self.ImpulseTime:
            a = 131.9
        elif clock >= self.ImpulseTime:  # sets the acceleration for the parts of the flight 
            a = -9.81

        s = self.u*self.timeStep + ((1/2)*(a * self.timeStep**2)) # calculates the displacment
        self.u = self.u + a*self.timeStep # calculates the new velocity

        self.altitude = self.altitude + s #adjusts the altitude

        return 

    def GPS(self, clock):

        #Outputs a longatude and lattitiude 
        #calcualte the distance step size based on the timestep
        latChange = self.latConst * self.timeStep
        longChange = self.longConst * self.timeStep

        self.lat = self.lat + latChange
        self.long = self.long + longChange

        return

    def RunSim(self, clock):

        self.timeStep = -(self.lastTime - clock)
        self.lastTime = clock

        self.IMU(clock)
        self.Altimiter(clock)
        self.GPS(clock)

        return self.altitude, self.lat, self.long, self.orientationQuat

        



