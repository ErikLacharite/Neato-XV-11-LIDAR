####################
######Reference#####
#https://xv11hacking.wikispaces.com/LIDAR+Sensor
###################

import serial, time
from math import pi,cos,sin
import matplotlib.pyplot as pyplot

com_port  = '/dev/cu.usbmodem1421' ##change the COM port if required, check in Arduino IDE
baud_rate = 115200

debug = False


##graphing
plot_super_resolution = 4
pyplot.axis([-6000*4, 6000*4, -6000*4, 6000*4])
X=[]
Y=[]


# POLAR PLOT
# r = np.arange(0, 3.0, 0.01)
# theta = 2 * np.pi * r

# ax = plt.subplot(111, projection='polar')
# ax.plot(theta, r, color='r', linewidth=3)
# ax.set_rmax(2.0)
# ax.grid(True)

# ax.set_title("A line plot on a polar axis", va='bottom')
# plt.show()


def plot_data(angle,dist_mm):
    angle_rad = angle * pi / 180.0
    x = (dist_mm*cos(angle_rad))*plot_super_resolution
    y = (dist_mm*sin(angle_rad))*plot_super_resolution
    X.append(x)
    Y.append(y)


def plot_finalize():
    pyplot.scatter(X,Y)
    pyplot.savefig('LIDAR_OUT.PNG')


##find minimum value in list and return
def minimum_value(x):
    ##set to maximum range to avoid edge case of first element being -1, because then if statement will not execute
    min_val = 7000

    for i in x[1:]:
        if i < min_val and i >= 0:
            #print i
            min_val = i

    return min_val



def main(self):
    ##begin
    ser = serial.Serial(com_port,baud_rate)
    print(ser.name)

    f = open('coordinates.txt','w')
    f.write("angle (deg), distance (mm)\n")
    dist_mm_store = [-1]*361

    ##debug
    if debug:
        print len(dist_mm_store)

    while True:
        try:
            b = (ord(ser.read(1))) ##initial read
            dati = []

            while True:
                ##250 == FA, FA is the start value - it's constant
                ##Each data packet is 22 bytes, > 20 means len(dati) == at least 21
                if b==(250) and len(dati)>20:
                    break

                ##add data to list, read again
                dati.append(b)
                b = (ord(ser.read(1)))

                ##do not hog the processor power - Python hogs 100% CPU without this in infinite loops
                time.sleep(0.0001)

            if len(dati)==21:
                ##index data packets go from 0xA0 (160) to 0xF9(359). Subtract 160 to normalize scale of data packets from 0 to 90.
                dati[0]=((dati[0])-160)

                for i in (1,2,3,4):
                    ##128 is an error code
                    if dati[i*4] != 128:
                        ##if good data, convert value in dati to value in mm. code found online
                        dist_mm = dati[4*i-1] | (( dati[4*i] & 0x3f) << 8)

                        ##dati[0] is index of each packet from 0 to 90. *4 for a value from 1 - 360, and cycle through the 4 data packets from that point at index
                        ##e.g. dati[0] is 30. 30 * 4 = 120, then the values being read are 121, 122, 123, 124
                        angle = dati[0]*4+i+1

                        ##adjust values by 2
                        if angle < 361:
                            dist_mm_store[angle] = dist_mm
                        #print(angle-2, dist_mm)

                        if debug:
                            print (angle,dist_mm)

                        ##plot
                        plot_data(angle,dist_mm)

                        ##write raw data to a file for debugging later
                        f.write("%s,%s\n" % (angle,dist_mm))

                ##debugging the speed of the DC motor, converted to RPM. code found online.
                if debug:
                    speed_rpm = float( dati[1] | (dati[2] << 8) ) / 64.0
                    if speed_rpm < 185 or speed_rpm > 315: # thresh-holds by troubleshooting
                        print "Speed Error:",speed_rpm


        except KeyboardInterrupt:
            ser.close()
            plot_finalize()
            f.close()
            quad.close()
            print 'Keyboard Interrupt'


main()


