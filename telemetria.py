# -*- coding: utf-8 -*-
import serial
import time
import matplotlib
matplotlib.use('TKAgg')
import os
from matplotlib import pyplot as plt
from matplotlib import animation
import threading

ANCHO_X_SEG = 60

class Telemetria:
    '''
    Clase para guardar los datos de la telemetria y leerlos del serial/bluetooth
    '''
    # pylint: disable=too-many-instance-attributes
    # Eight is reasonable in this case.
    def __init__(self, serial_port):
        self.connected = True
        self.sp = serial.Serial(serial_port, 19200) #'/dev/cu.bqZUM_BT328-SPPDev'
        self.timeList = []
        self.data = []
        self.fig = plt.figure()
        self.fig.canvas.set_window_title('pyTelemetría')
        self.ax = []
        self.lines = []

    def getLines(self):
        return self.lines

    def getAx(self, i):
        return self.ax[i]

    def getTimeList(self):
        return self.timeList

    def getData(self):
        return self.data

    def getFig(self):
        return self.fig

    def inicializar(self):
        lin = self.sp.readline()
        while not lin.startswith('pT '):
            lin = self.sp.readline()
        ldata = lin[3:].split('/')
        self.timeList.append(ldata[0])
        nbloque = 0
        for bloque in ldata[1].split('|'):
            self.data.append([])
            for word in bloque.split(' '):
                self.data[nbloque].append([float(word)])
            nbloque += 1
        for i in range(1, len(self.data)+1):
            self.ax.append(self.fig.add_subplot(len(self.data)*100+10+i))
            for _ in range(len(self.data[i-1])):

                self.lines.extend(self.ax[-1].plot([], [], lw=2))

    def isRun(self):
        return self.connected

    def updateData(self):
        lin = self.sp.readline()
        while lin.startswith('pT ') == False:
            lin = self.sp.readline()
        ldata = lin[3:].split('/')
        self.timeList.append(ldata[0])
        nbloque = 0
        for bloque in ldata[1].split('|'):
            ind = 0
            for word in bloque.split(' '):
                self.data[nbloque][ind].append(float(word))
                ind += 1
            nbloque += 1

    def debug(self):
        print "DEBUG -->"
        print self.data
        print self.lines

    def stop(self):
        self.connected = False


TELEM = Telemetria('/dev/cu.bqZUM_BT328-SPPDev')
TELEM.inicializar()


def threadFun():
    global TELEM
    while(TELEM.isRun()):
        TELEM.updateData()

THREAD = threading.Thread(target=threadFun)
THREAD.start()

# initialization function: plot the background of each frame
def init():
    global TELEM
    for line in TELEM.getLines():
        line.set_data([], [])
    return TELEM.getLines()

def updatePlot(i):
    global TELEM
    ind = 0
    for i in range(len(TELEM.getData())):
        numpoints = min([len(TELEM.getTimeList()), 100])
        ltotal = [item for sublist in TELEM.getData()[i] for item in sublist[-numpoints:]]
        mmin, mmax = min(ltotal)*1.1, max(ltotal)*0.9
        ax = TELEM.getAx(i)
        ax.set_ylim([mmin, mmax])
        lasttime = 0
        if len(TELEM.getTimeList()) > 0:
            lasttime = TELEM.getTimeList()[-1]
        ax.set_xlim([int(lasttime)-ANCHO_X_SEG, int(lasttime)])
        for j in range(len(TELEM.getData()[i])):
            numpoints = len( [x for x in TELEM.getData()[i][j] if x > (int(lasttime)-100)])
            lin = TELEM.getLines()
            lin[ind].set_data(TELEM.getTimeList()[-numpoints:], TELEM.getData()[i][j][-numpoints:])
            ind += 1
    return TELEM.getLines()



# call the animator.  blit=True means only re-draw the parts that have changed.
ANIM = animation.FuncAnimation(TELEM.getFig(), updatePlot, init_func=init, frames=None, interval=50, blit=False)
plt.show()


print "Finalizando aplicación"
TELEM.stop()
os._exit(0)
