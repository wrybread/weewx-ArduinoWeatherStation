#!/usr/bin/env python


'''

Simple script that reads serial data from the Arduino attached to whatever port.


'''


# adjust this to taste
port = "/dev/ttyACM0"





import time, os, serial 


print "Connecting to %s..." % port
ser = serial.Serial(port, 9600, timeout=.5)

print "Success!"



def read_buffer():

    # read the whole buffer
    last_data=''
    while True:
        data=ser.readline()
        if data!='':
            last_data=data
        else:
            return last_data.replace("\n", "")





while True:

    data = read_buffer()

    if data:
        print data

    

