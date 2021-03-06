#!/usr/bin/python
#Script by John Cooper
#12/13/15
#email jrcoop34@gmail.com with any questions

import serial
import RPi.GPIO as GPIO
import time
from datetime import datetime
from decimal import Decimal
import io


#Identifies serial connection to pH sensor
usbport = '/dev/ttyAMA0'
ser = serial.Serial(usbport,9600)

GPIO.setmode(GPIO.BCM)
S0_pin = 18
S1_pin = 23

GPIO.setup(S0_pin, GPIO.OUT)
GPIO.setup(S1_pin, GPIO.OUT)

GPIO.output(S0_pin, 0)
GPIO.output(S1_pin, 0)



sio = io.TextIOWrapper(io.BufferedRWPair(ser,ser,1), newline = "\r")
ser.write("Cal\r")

print("Calibrating to atmospheric oxygen levels...")

time.sleep(5)

GPIO.cleanup()
ser.close()

