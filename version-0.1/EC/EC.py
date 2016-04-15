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
db = sqlite3.connect('/ec/EC.db')
cur = db.cursor()
cur.execute("create table if not exists ec(date DATETIME,ec varchar(4))")
cur.execute("create table if not exists tds(date DATETIME,tds varchar(4))")
cur.execute("create table if not exists sal(date DATETIME,sal varchar(4))")
cur.execute("create table if not exists sg(date DATETIME,sg varchar(4))") 
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

ser.write("R\r")

#reads temperature value

temp = sio.readline()

#print(temp)

ser.close()
GPIO.cleanup()

#closes old connetion
#--------------------END  Temperature----------------------

#-------------------EC Start---------------------------
#opens new connection
usbport = '/dev/ttyAMA0'
ser = serial.Serial(usbport,9600)
GPIO.setmode(GPIO.BCM)
S0_pin = 18
S1_pin = 23
GPIO.setup(S0_pin, GPIO.OUT)
GPIO.setup(S1_pin, GPIO.OUT)

#switches to EC circuit and tells the EC circuit 
#which temperature to compensate readings with. 
#(EC is temperature dependent)

GPIO.output(S0_pin, False)
GPIO.output(S1_pin, True)

sio = io.TextIOWrapper(io.BufferedRWPair(ser,ser,1), newline = "\r")

ser.write("T," + temp + "\r")

print("T," + temp + "\r")

ok = sio.readline()


#for debug



#pulls the data over serial connection
#TextIOWrapper sets '\r' as EOL character rather than '\n' allowing proper data separation over serial
time.sleep(1)
ser.write("R\r")

#ok is throwaway, atlas scientific spits out *OK after every successful write command

#ok = sio.readline()
reading = sio.readline()
print(reading)


ec,tds,sal,sg = reading.split(",")




#splits the reading into it's component variabels, line comes over serial as csv
#ec, tds, sal, sg = reading.split(",")


ser.close()

GPIO.cleanup()
#pulls formatted time stamp 
#i = datetime.now()
#timestamp = i.strftime('%m-%d-%Y %H:%M:%S')

#inserts data into database

cur.execute("INSERT INTO ec values(datetime(CURRENT_TIMESTAMP,'localtime'), (?))", (ec,)) 
cur.execute("INSERT INTO tds values(datetime(CURRENT_TIMESTAMP,'localtime'), (?))", (tds,))
cur.execute("INSERT INTO sal values(datetime(CURRENT_TIMESTAMP,'localtime'), (?))", (sal,))
cur.execute("INSERT INTO sg values(datetime(CURRENT_TIMESTAMP,'localtime'), (?))", (sg,))
db.commit()


#closes database connection
db.close()
