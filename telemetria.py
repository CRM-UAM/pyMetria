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
from matplotlib import pyplot as plt
from matplotlib import animation


ser = serial.Serial('/dev/cu.bqZUM_BT328-SPPDev', 19200, timeout=0)

sum = 250
# First set up the figure, the axis, and the plot element we want to animate
fig = plt.figure()
ax1 =fig.add_subplot(211)
ax2 =fig.add_subplot(212)
#ax = plt.axes(xlim=(0, 2), ylim=(-2, 2))
ax1.set_xlim([-5, 5])
ax1.set_ylim([-5, 5])
ax2.set_xlim([-5, 5])
ax2.set_ylim([-5, 5])
line, = ax1.plot([], [], lw=2)
line2, = ax2.plot([], [], lw=2)

# initialization function: plot the background of each frame
def init():
    line.set_data([], [])
    line2.set_data([], [])
    return line,


def getXYdata(t):
    global sum
    #while sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
    #    line = sys.stdin.readline()
    #    if line:
    #        sum = float(line)
    #
    #print(time.time())
    line = ser.readline()
    if line:
        sum = float(line)
        print(line)
    x = np.linspace(-5, 0, 1000)
    y = (sum/250) * np.cos( 2 * np.pi * (x - 0.01 * t))
    return x, y
# animation function.  This is called sequentially
def animate(i):
    #print(i)
    x, y = getXYdata(i)
    line.set_data(x, y)
    line2.set_data(x, -y)
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

