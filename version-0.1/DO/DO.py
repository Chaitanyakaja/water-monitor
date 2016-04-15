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
db = sqlite3.connect('/do/DO.db')
cur = db.cursor()
cur.execute("create table if not exists mgL(date DATETIME,mgL varchar(4))")
cur.execute("create table if not exists percent(date DATETIME,percent varchar(4))")
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


sio = io.TextIOWrapper(io.BufferedRWPair(ser,ser,1),newline = "\r")


#reads temperature value
ser.write("R\r")

temp = sio.readline()
print(temp)

ser.close()
#closes old connetion
#--------------------END  Temperature----------------------

#-------------------DO Start---------------------------
#opens new connection
usbport = '/dev/ttyAMA0'
ser = serial.Serial(usbport,9600)
GPIO.setmode(GPIO.BCM)
S0_pin = 18
S1_pin = 23
GPIO.setup(S0_pin, GPIO.OUT)
GPIO.setup(S1_pin, GPIO.OUT)

#switches to DO circuit and tells the DO circuit 
#which temperature to compensate readings with. 
#(DO is temperature dependent)

GPIO.output(S0_pin, 1)
GPIO.output(S1_pin, 0)
sio = io.TextIOWrapper(io.BufferedRWPair(ser,ser,1), newline = "\r")

ser.write("T," + temp + "\r")
#ok = sio.readline()
#print(ok) #for debug



#pulls the data over serial connection
#TextIOWrapper sets '\r' as EOL character rather than '\n' allowing proper data separation over serial
ser.write("R\r")

#ok is throwaway, atlas scientific spits out *OK after every successful write command
#ok = sio.readline()


reading = sio.readline()
#print(reading)

mgL,percent = reading.split(",")


#ends session with pH stamp
ser.close()
GPIO.cleanup()
#pulls formatted time stamp 
#i = datetime.now()
#timestamp = i.strftime('%m-%d-%Y %H:%M:%S')

#inserts data into database

cur.execute("INSERT INTO mgL values(datetime(CURRENT_TIMESTAMP,'localtime'), (?))", (mgL,))
cur.execute("INSERT INTO percent values(datetime(CURRENT_TIMESTAMP,'localtime'), (?))", (percent,))
db.commit()


#closes database connection
db.close()
