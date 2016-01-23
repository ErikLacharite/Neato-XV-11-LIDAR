import serial,time
from pprint import pprint
from math import pi,cos,sin

import matplotlib.pyplot as pyplot

com_port  = '/dev/cu.usbmodem1411'
baud_rate = 115200


####graphing
pyplot.axis([-6000, 6000,-6000, 6000])
X=[]
Y=[]



def plot_data(angle,dist_mm):
    angle_rad = angle * pi / 180.0
    x = cos(angle_rad)*dist_mm
    y = sin(angle_rad)*dist_mm
    X.append(x)
    Y.append(y)


def plot_finalize():
    pyplot.scatter(X,Y)
    pyplot.savefig('example01.png')

####begin
ser = serial.Serial(com_port,baud_rate)
print(ser.name)

ser.write(b'hello')


while True:
    try:
        b = (ord(ser.read(1))) # init
        dati = []
        while True:
            if b==(250) and len(dati)>20:
                break
            dati.append(b)
            b = (ord(ser.read(1)))
            time.sleep(0.0001) # do not hog the processor power
        if len(dati)==21:
            dati[0]=((dati[0])-160)
            for i in (1,2,3,4):
                if dati[i*4] != 128:
                    dist_mm = dati[4*i-1] | (( dati[4*i] & 0x3f) << 8)
                    single_point = (dati[0],0,dist_mm)
                    angle = dati[0]*4+i+1
                    print (angle,dist_mm)
                    plot_data(angle,dist_mm)

            speed_rpm = float( dati[1] | (dati[2] << 8) ) / 64.0
            if speed_rpm < 185 or speed_rpm > 315: # thresh-holds by troubleshooting
                print "Speed Error:",speed_rpm

    except KeyboardInterrupt:
        ser.close()
        plot_finalize()
        print 'interrupted!'




