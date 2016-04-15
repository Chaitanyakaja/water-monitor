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
db = sqlite3.connect('/temperature/temperature.db')
cur = db.cursor()
cur.execute("create table if not exists temp(date DATETIME,temp varchar(4))")
db.commit()

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

ser.write("R\r")


sio = io.TextIOWrapper(io.BufferedRWPair(ser,ser,1),newline = "\r")


#reads temperature value

temp = sio.readline()

ser.close()

#inserts data into database

cur.execute("INSERT INTO temp values(datetime(CURRENT_TIMESTAMP,'localtime'), (?))", (temp,)) 
db.commit()


#closes database connection
db.close()

GPIO.cleanup()
