from genericpath import exists
from sqlite3 import Row
from typing import Counter
from matplotlib.pyplot import title
from pyqtgraph.Qt import QtWidgets, QtCore, QtGui
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import sys  # We need sys so that we can pass argv to QApplication
import time
import pandas as pd
import serial
from PIL import Image
from numpy import asarray
import numpy as np
from FlightComputerSimulator import Simulator

sim = Simulator()

ser1 = {}


#checks for the existance of data feeds on the COM ports (TO DO Change this to a function that can iterate thtrough all of the COM ports, (recall there is a way to check which ones are connected to))
try:
    ser1 = serial.Serial("COM4",  15500000, timeout=None)
    ser1.flush()

except:

    print("Nothing on port 1")

try:
    ser2 = serial.Serial("COM5",  15500000, timeout=None)
    ser2.flush()

except:

    print("Nothing on port 2")


#Sets the GUI start time
startTime = time.time()

#Opens a jpg if it exists (TO DO make this into a try and except like above, also maybe fold into a function for better objectivity)
if(exists("test.jpg")):
    im = Image.open("test.jpg")
    im = im.rotate(180)
    im = im.transpose(Image.FLIP_LEFT_RIGHT)     #When importing an image, the way pyqtgraph represnts the image is weird so just transpose and rotate :(
    image = asarray(im)                          #make this update when you get the new image

#Define all data types

receiving = False
counterRec = 0
transData = [0,0,0,0,0,0,0,0,0,0]

timeData =[]

#Rocket Data

RQ1,RQ2,RQ3,RQ4 = "", "","",""

RGPS1,RGPS2 = "",""

RRRSI = ""

RXR,RYR,RZR = "","",""

dataRRRSI = []
dataRGPS1 = []
dataRGPS2 = []
dataRXR = []
dataRYR = []
dataRZR = []

#Payload Data

PQ1,PQ2,PQ3,PQ4 = "", "","",""

PGPS1,PGPS2 = "",""

PRRSI = ""

PXR,PYR,PZR = "","",""



class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):  #CONFIGURE WINDOW
        super(MainWindow, self).__init__(*args, **kwargs)

        #init graphing window
        self.graphWidget = pg.GraphicsView() 
        self.l = pg.GraphicsLayout(border=(100,100,100))
        self.graphWidget.setCentralItem(self.l)

        text = """
        Telemetry Links<br>
        1. Strength , connected?<br>
        2. Strength , connected?.
        """

        #Top Box

        self.layoutTop = self.l.addLayout(row =0 , col=3) # can create a layout which we can the arrange labels and buttons into. :)

        self.labelTop = self.l.addLabel(text)
        self.layoutTop.addItem(self.labelTop, rowspan= 3, col = 0)
       
        proxy = QtWidgets.QGraphicsProxyWidget() # needx a proxy to get the button to work
        button = QtWidgets.QPushButton('Reset Graphs')
        button.setStyleSheet("QPushButton { background-color: grey }" "QPushButton:pressed { background-color: red }" )
        button.clicked.connect(Reset)
                      
        proxy.setWidget(button)

        self.layoutTop.addItem(proxy, row = 1, col = 1)

        #Bottom Box

        self.labelBottom = self.l.addLabel(text, row =3 , col=1, colspan= 4)

        #image

        self.img = pg.ImageItem(axisOrder='row-major')
       
        self.img.setImage(image)

        self.vb = self.l.addViewBox(lockAspect=True, row=1, col=1, rowspan=2 , colspan= 4)
        self.vb.addItem(self.img)
        self.vb.autoRange()


        ##Initiate Graphs
        #Graph 1
        self.p1 = self.l.addPlot(title = "plot 1", row=0, col=0)
        self.p1.showGrid(x=True, y=True)

        self.p1.x = []
        self.p1.y = []  

        self.p1.data_line = self.p1.plot(self.p1.x, self.p1.y)

        #Graph 2
        self.p2 = self.l.addPlot(title = "plot 2", row=0, col=1)
        self.p2.showGrid(x=True, y=True)

        self.p2.x = []
        self.p2.y = []  

        self.p2.data_line = self.p2.plot(self.p2.x, self.p2.y)

        #Graph 3
        self.p3 = self.l.addPlot(title = "plot 3", row=0, col=4)
        self.p3.showGrid(x=True, y=True)

        self.p3.x = []
        self.p3.y = []  

        self.p3.data_line = self.p3.plot(self.p3.x, self.p3.y)

        #Graph 4
        self.p4 = self.l.addPlot(title = "plot 4", row=0, col=5)
        self.p4.showGrid(x=True, y=True)

        self.p4.x = []
        self.p4.y = []  

        self.p4.data_line = self.p4.plot(self.p4.x, self.p4.y)

        #Graph 5
        self.p5 = self.l.addPlot(title = "plot 5", row=1, col=0)
        self.p5.showGrid(x=True, y=True)

        self.p5.x = []
        self.p5.y = []  

        self.p5.data_line = self.p5.plot(self.p5.x, self.p5.y)

        #Graph 6
        self.p6 = self.l.addPlot(title = "plot 6", row=1, col=5)
        self.p6.showGrid(x=True, y=True)

        self.p6.x = []
        self.p6.y = []  

        self.p6.data_line = self.p6.plot(self.p6.x, self.p6.y)

        #Graph 7
        self.p7 = self.l.addPlot(title = "plot 7", row=2, col=0)
        self.p7.showGrid(x=True, y=True)

        self.p7.x = []
        self.p7.y = []  

        self.p7.data_line = self.p7.plot(self.p7.x, self.p7.y)

        #Graph 8
        self.p8 = self.l.addPlot(title = "plot 8", row=2, col=5)
        self.p8.showGrid(x=True, y=True)

        self.p8.x = []
        self.p8.y = []  

        self.p8.data_line = self.p8.plot(self.p8.x, self.p8.y)

        #Graph 9
        self.p9 = self.l.addPlot(title = "plot 9", row=3, col=0)
        self.p9.showGrid(x=True, y=True)

        self.p9.x = []
        self.p9.y = []  

        self.p9.data_line = self.p9.plot(self.p9.x, self.p9.y)

        #Graph 10
        self.p10 = self.l.addPlot(title = "plot 10", row=3, col=5)
        self.p10.showGrid(x=True, y=True)

        self.p10.x = []
        self.p10.y = []  

        self.p10.data_line = self.p10.plot(self.p10.x, self.p10.y)

        #Update Graphs
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()

        #framerate counter
        self.lastupdate = time.time()
        self.fps = 0.

        
    def update_plot_data(self): #UPDATE DATA

        #Decode()

        clock = time.time() - startTime

        #data from serial
        if(bool(ser1)):

            dataRXR.append(RXR)
            dataRYR.append(RYR)
            dataRZR.append(RZR)
            dataRGPS1.append(RGPS1)
            dataRGPS2.append(RGPS2)
            dataRRRSI.append(RRRSI)

            timeData.append(time.time() - startTime)

        #set data values live
        self.p1.data_line.setData(timeData, dataRXR)
        self.p2.data_line.setData(timeData, dataRYR)
        self.p5.data_line.setData(timeData, dataRZR)
        self.p7.data_line.setData(timeData, dataRGPS1)
        self.p9.data_line.setData(timeData, dataRGPS2)
        self.p6.data_line.setData(timeData, self.p1.y)
        self.p3.data_line.setData(timeData, self.p1.y)
        self.p8.data_line.setData(timeData, self.p1.y)
        self.p4.data_line.setData(timeData, self.p1.y)
        self.p10.data_line.setData(timeData, self.p1.y)

        #framerate counter
        now = time.time()
        dt = (now-self.lastupdate)
        if dt <= 0:
            dt = 0.000000000001
        fps2 = 1.0 / dt
        self.lastupdate = now
        self.fps = self.fps * 0.9 + fps2 * 0.1
        tx = 'Mean Frame Rate:  {fps:.3f} FPS'.format(fps=self.fps )

        text = """
        Telemetry Links<br>
        1. Strength , connected?<br>
        2. Strength , connected?<br>
        """

        #Updates Text

        text = text + tx
        text = text + str(RRRSI)
        self.labelTop.setText(text)
        sim.RunSim(clock)

def Reset(): #RESET COM PORTS

    global ser1,startTime,dataRGPS1,dataRGPS2,dataRRRSI,dataRXR,dataRYR,dataRZR,timeData

    try:
        ser1 = {}
        ser1 = serial.Serial("COM4", 15500000, timeout=None)
        ser1.flushInput()

        startTime = time.time()

        dataRRRSI = []
        dataRGPS1 = []
        dataRGPS2 = []
        dataRXR = []
        dataRYR = []
        dataRZR = []
        timeData =[]

    except:

        print("Nothing on this port")
  
def Decode(): #DECODE DATA

    global RQ1, RQ2, RQ3, RQ4, RGPS1, RGPS2, RRRSI, RXR, RYR, RZR, receiving, counterRec

    ser1.flush()
    msg = ser1.readline()
    msg = msg.decode('utf-8') #removes the endbits and the b''
    msg = msg.strip("\r\n")
    #print(msg)
    #print([str(msg)])

    if(str(msg) == "Transmition"):

        counterRec = -1
        receiving = True
        #print("starting")

    while(receiving == True and counterRec != 9):

        ser1.flush()
        msg = ser1.readline()
        msg = msg.decode('utf-8') #removes the endbits and the b''
        msg = msg.strip("\r\n")
        counterRec += 1

        #print(counterRec)

        transData[int(counterRec)] = float(msg)

    RQ1 = transData[6]
    RQ2 = transData[1]
    RQ3 = transData[2]
    RQ4 = transData[3]
    RGPS1 = transData[4]
    RGPS2 = transData[5]
    RRRSI = transData[0]
    roll_x, roll_y, roll_z = euler_from_quaternion(RQ1, RQ2, RQ3, RQ4)
    RXR = roll_x
    RYR = roll_y
    RZR = roll_z
        
def euler_from_quaternion(x, y, z, w): #CONVERT QUTERNION TO EULER
        """
        Convert a quaternion into euler angles (roll, pitch, yaw)
        roll is rotation around x in radians (counterclockwise)
        pitch is rotation around y in radians (counterclockwise)
        yaw is rotation around z in radians (counterclockwise)
        """
        t0 = +2.0 * (w * x + y * z)
        t1 = +1.0 - 2.0 * (x * x + y * y)
        roll_x = np.arctan2(t0, t1)
     
        t2 = +2.0 * (w * y - z * x)
        t2 = +1.0 if t2 > +1.0 else t2
        t2 = -1.0 if t2 < -1.0 else t2
        pitch_y = np.arcsin(t2)
     
        t3 = +2.0 * (w * z + x * y)
        t4 = +1.0 - 2.0 * (y * y + z * z)
        yaw_z = np.arctan2(t3, t4)

        roll_x = roll_x *180/np.pi
        pitch_y = pitch_y *180/np.pi
        yaw_z = yaw_z *180/np.pi
     
        return roll_x, pitch_y, yaw_z # in degrees

