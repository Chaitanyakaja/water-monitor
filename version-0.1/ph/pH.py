#!/usr/bin/python
#Script by John Cooper
#12/13/15
#email jrcoop34@gmail.com

import serial
import time
import sqlite3
from datetime import datetime
import RPi.GPIO as GPIO
import io
from decimal import Decimal

#connects to and creates database if not already created
db = sqlite3.connect('/ph/pH.db')
cur = db.cursor()
cur.execute("create table if not exists phread(date DATETIME,ph varchar(4))")
db.commit()

#------------Temperature Start------------------

#identifies serial connection to sensor
usbport = '/dev/ttyAMA0'
ser = serial.Serial(usbport, 9600)

#sets control pins for serial port expander
GPIO.setmode(GPIO.BCM)
S0_pin = 18
S1_pin = 23

GPIO.setup(S0_pin, GPIO.OUT)
GPIO.setup(S1_pin, GPIO.OUT)

#switches to temperature sensor (y3)
GPIO.output(S0_pin, 1)
GPIO.output(S1_pin, 1)



sio = io.TextIOWrapper(io.BufferedRWPair(ser,ser,1), newline = "\r")

ser.write("R\r")

#reads temperature value
temp = sio.readline()
#print(temp)

ser.close()

GPIO.cleanup()
#closes old connetion
#--------------------END  Temperature----------------------

#-------------------pH Start---------------------------
usbport = '/dev/ttyAMA0'
ser = serial.Serial(usbport, 9600)

GPIO.setmode(GPIO.BCM)
S0_pin = 18
S1_pin = 23

GPIO.setup(S0_pin, GPIO.OUT)
GPIO.setup(S1_pin, GPIO.OUT)

GPIO.output(S0_pin, False)
GPIO.output(S1_pin, False)


sio = io.TextIOWrapper(io.BufferedRWPair(ser,ser,1), newline = "\r")

#ser.write("T," + temp + "\r")

ser.write("R\r")

reading = sio.readline()

#print(reading)
#ok = sio.readline()

ph = float(reading)

#print(ph)

#inserts data into database

cur.execute("INSERT INTO phread values(datetime(CURRENT_TIMESTAMP,'localtime'), (?))", (ph,)) 
db.commit()


#closes database connection
db.close()
ser.close()
GPIO.cleanup()
