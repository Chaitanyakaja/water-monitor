#Script by John Cooper && Connor Aitken
#4/12/16
#STORC
#This script takes a reading from the DO sensor and writes it to a database
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
cur.execute("create table if not exists mgL(date DATETIME,ec varchar(4))")
cur.execute("create table if not exists percentsat(date DATETIME,tds varchar(4))")
db.commit()

#takes reading from EC sensor
ser.write('1:r')
reading  = ser.readline()

mgL,percentsat = reading.split(",")

#inserts data into database 
cur.execute("INSERT INTO mgL values(datetime(CURRENT_TIMESTAMP,'localtime'), (?))", (mgL,))
cur.execute("INSERT INTO percentsat values(datetime(CURRENT_TIMESTAMP,'localtime'), (?))", (percentsat,))
db.commit()

#closes database connection
db.close()
#closes serial connection
ser.close()
