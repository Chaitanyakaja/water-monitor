#!/usr/bin/python
#Script by John Cooper
#12/13/15
#jrcoop34@gmail.com with any questions
#Please run this script ONLY after running the midpoint-calibration script


import serial
import time
import RPi.GPIO as GPIO

print "Calibrating to a pH of 10, please have sensor in a buffer of 10 pH"

usbport = '/dev/ttyAMA0'
ser = serial.Serial(usbport, 9600)

#GPIO.BCM refers to the BCM layout of the GPIO pins. GPIO.BOARD can also be used but
#BCM is they layout that the breakout cable is labeled with.
GPIO.setmode(GPIO.BCM)
S0_pin = 18
S1_pin = 23

#sets BCM pins 18 & 23 as outputs
GPIO.setup(S0_pin, GPIO.OUT)
GPIO.setup(S1_pin, GPIO.OUT)


#selects y1 from serial port expander
GPIO.output(S0_pin, 0)
GPIO.output(S1_pin, 1)



# turn on the LEDs
ser.write("L,1\r")


# delays 2 minutes
time.sleep(30)

# calibrates for pH 10, change 10.00 to whatever your highpoint buffer is known to be
ser.write("Cal,high,10.00\r")
print "calibrating..."

time.sleep(5)

#ends session

print "calibrated!"
ser.write(L,0)
time.sleep(5)
