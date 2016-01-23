# Neato XV-11 LIDAR

This code was put together to interface with the Neato XV-11 LIDAR. Please see reference section bellow for resources I used to put this together. When the LIDAR is spinning between 180 and 310 RPM it begins transmitting useful data. That data is collected and upon a keyboard interrupt (ctrl+c) the data will be plotted to a graph and saved to the working directory.

# Connection:
    ## Motor:
        Black --> Ground
        Red --> 22ohm --> 3.3v (or just 3.3v)
    ## Sensor JST:
        Red --> 3.3v
        Brown (RX) --> RX
        Orange (TX) --> RX
        Black --> Ground
    ## Serial to Computer:
        com_port = ???
        baud_rate = 115200
        I used an Arduino UNO with a jumper between the "RESET" and "GND" as my serial adapter. The COM port can then be read from the list on COMs in the Arduino IDE.



# Notes:
1. The motor is not be controlled via PWM, between [3.3v or 22ohm+3.3v] the correct speed is reached.
2. The error checking bits are not used.
3. Data with 0x80/250_10 type errors are discarded.


# Dependencies (none that need to be installed):
## PySerial
Included

## matplotlib
Included in python

#References
<https://xv11hacking.wikispaces.com/LIDAR+Sensor>
<https://github.com/Xevel/NXV11>