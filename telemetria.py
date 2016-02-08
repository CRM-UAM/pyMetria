"""
Matplotlib Animation Example

author: Jake Vanderplas
email: vanderplas@astro.washington.edu
website: http://jakevdp.github.com
license: BSD
Please feel free to use and modify this, but keep the above information. Thanks!
"""
import time
import sys
import select
import serial
import numpy as np
import matplotlib
matplotlib.use('TKAgg')
import time
import os

from matplotlib import pyplot as plt
from matplotlib import animation


import serial
import threading
connected = False
serial_port = serial.Serial('/dev/cu.bqZUM_BT328-SPPDev', 19200)


i=0
times  = [0]*100
data1 = [0]*100
data2 = [0]*100



def handle_data(s):
    global data1
    global times
    global data2
    arg = s.split(' ')
    times.append(float(arg[0]))
    data1.append(float(arg[1]))
    data2.append(float(arg[2]))


def read_from_port(ser):
    global connected
    while not connected:
        #serin = ser.read()
        connected = True

        while True:
           reading = ser.readline().decode('utf8')
           handle_data(reading)

thread = threading.Thread(target=read_from_port, args=(serial_port,))
thread.start()


# First set up the figure, the axis, and the plot element we want to animate
fig = plt.figure()
ax1 =fig.add_subplot(211)
ax2 =fig.add_subplot(212)
#ax = plt.axes(xlim=(0, 2), ylim=(-2, 2))
ax1.set_xlim([-5, 0.1])
ax1.set_ylim([-5, 500])
ax2.set_xlim([-5, 0.1])
ax2.set_ylim([-5, 500])
line, = ax1.plot([], [], lw=2)
line2, = ax2.plot([], [], lw=2)

# initialization function: plot the background of each frame
def init():
    line.set_data([], [])
    line2.set_data([], [])
    return line,


def getXYdata1(t):
    global data1
    x = np.linspace(-5, 0, 100)
    return x, data1[-100:]

# animation function.  This is called sequentially
def animate(i):
    #print(i)
    #x, y = getXYdata1(i)
    ax1.set_xlim([times[-100], times[-1]])
    line.set_data(times[-100:], data1[-100:])
    ax2.set_xlim([times[-100], times[-1]])
    line2.set_data(times[-100:], data2[-100:])
    #ax2.set_xlim([-2.2+float(i)/100, 2.2+float(i)/100])
    return line,line2,

# call the animator.  blit=True means only re-draw the parts that have changed.
anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=None, interval=50, blit=False)

# save the animation as an mp4.  This requires ffmpeg or mencoder to be
# installed.  The extra_args ensure that the x264 codec is used, so that
# the video can be embedded in html5.  You may need to adjust this for
# your system: for more information, see
# http://matplotlib.sourceforge.net/api/animation_api.html
#anim.save('basic_animation.mp4', fps=30, extra_args=['-vcodec', 'libx264'])

plt.show()


print("FIN")
connected = False
os._exit(0)
