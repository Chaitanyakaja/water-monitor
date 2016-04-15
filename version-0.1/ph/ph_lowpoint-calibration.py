#!/usr/bin/python
#Script by John Cooper
#12/13/15
#jrcoop34@gmail.com with any questions

import serial
import time
import RPi.GPIO as GPIO
print "Calibrating to a pH of 4.00, please have the sensor in a buffer of pH 4.00"

usbport = '/dev/ttyAMA0'
ser = serial.Serial(usbport, 9600)

#sets BCM pins 18 & 23 as outputs to control serial port expander
GPIO.setmode(GPIO.BCM)
S0_pin = 18
S1_pin = 23

#sets pins 18 & 23 as outputs
GPIO.output(S0_pin,GPIO.OUT)
GPIO.output(S1_pin,GPIO.OUT)

#uses pins 18 & 23 to switch serial port expander to y1 (pH)
GPIO.output(S0_pin, 0)
GPIO.output(S1_pin, 1)


# turn on the LEDs
ser.write("L,1\r")

# delays 2 minutes
time.sleep(10)

# calibrates for pH 4, change 4.00 to whatever value your known pH buffer is.
ser.write("Cal,low,4.00\r")
print "calibrating..."
time.sleep(5)

#ends session
print "calibrated!"
ser.write("L,0\r")
time.sleep(5)


