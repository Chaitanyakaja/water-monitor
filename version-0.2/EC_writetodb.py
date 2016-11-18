#Script by John Cooper && Connor Aitken
#4/12/16
#STORC
#This script takes a reading from the EC sensor and writes it to a database
# 0.2

import sys
import serial
import time
import sqlite3
from datetime import datetime
from decimal import Decimal

#opens serial connection to arduino
usbport = '/dev/ttyACM0'
ser = serial.Serial(usbport,9600)


#connects to and creates databse if not already connected
db = sqlite3.connect('/home/pi/STORC.db')
cur = db.cursor()
cur.execute("create table if not exists ec(date DATETIME,ec varchar(4))")
cur.execute("create table if not exists tds(date DATETIME,tds varchar(4))")
cur.execute("create table if not exists sal(date DATETIME,sal varchar(4))")
cur.execute("create table if not exists sg(date DATETIME,sg varchar(4))")
db.commit()

#takes reading from EC sensor
ser.write('0:r')
reading  = ser.readline()

ec,tds,sal,sg = reading.split(",")

#inserts data into database 
cur.execute("INSERT INTO ec values(datetime(CURRENT_TIMESTAMP,'localtime'), (?))", (ec,))
cur.execute("INSERT INTO tds values(datetime(CURRENT_TIMESTAMP,'localtime'), (?))", (tds,))
cur.execute("INSERT INTO sal values(datetime(CURRENT_TIMESTAMP,'localtime'), (?))", (sal,))
cur.execute("INSERT INTO sg values(datetime(CURRENT_TIMESTAMP,'localtime'),(?))", (sg,))
db.commit()

#closes database connection
db.close()
#closes serial connection
ser.close()
