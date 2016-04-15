#!/usr/bin/python
#pH calibration script by John Cooper
#12/13/15
#This script calibrates the pH sensor to a pH of 7, if this is the only necessary calibration.
#run the 'midpoint-calibration-seven' script instead.
#After this script is run calibrate at a higher or lower point, the further
#apart these are the more accurate the data will be. Calibration should always be done in a 
#known buffer.
#jrcoop34@gmail.com with any questions. 

import serial
import time
import Rpi.GPIO as GPIO
print "Midpoint calibration to a pH of 7, sensor should be placed  in a buffer"

usbport = '/dev/ttyAMA0'
ser = serial.Serial(usbport, 9600)

#GPIO layout according to broadcom specs (GPIO.BOARD) can also be used, but breakout cable is coded for BCM
GPIO.setup(GPIO.BCM)

#switch pins on serial port expander
S0_pin = 18
S1_pin = 23

#sets pins 18 & 23 to outputs
GPIO.setup(S0_pin, GPIO.OUT)
GPIO.setup(S1_pin, GPIO.OUT)

#selects y1 on serial port expander (pH)
GPIO.output(S0_pin, 0)
GPIO.output(S1_pin, 1)

# turns on the LEDs
ser.write("L,1\r")


# delays a few seconds
time.sleep(10)

# calibrates for pH 7
ser.write("Cal,mid,7.00\r")
print "calibrating..."
time.sleep(5)

#ends session

print "calibrated!"
ser.write("L,0\r")
time.sleep(5)


