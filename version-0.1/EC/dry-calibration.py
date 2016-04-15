#!/usr/bin/python
#John Cooper
#12/13/15
#jrcoop34@gmail.com with questions
#This script performs a dry calibration, always a first step with EC probes

import serial
import RPi.GPIO as GPIO
import time
from datetime import datetime
from decimal import Decimal
import io

#Identifies serial connection to ec sensor
usbport = '/dev/ttyAMA0'
ser = serial.Serial(usbport,9600)

GPIO.setmode(GPIO.BCM)
S0_pin = 18
S1_pin = 23

GPIO.setup(S0_pin, GPIO.OUT)
GPIO.setup(S1_pin, GPIO.OUT)

GPIO.output(S0_pin, 0)
GPIO.output(S1_pin, 1)

sio = io.TextIOWrapper(io.BufferedRWPair(ser,ser,1), newline = "\r")

ser.write("Cal,clear\r")
print("clearing old calibration data...")
time.sleep(3)

ser.write("Cal,dry\r")
print("performing dry calibration...")
time.sleep(3)

ser.close()
GPIO.cleanup()

