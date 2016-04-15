#Script by John Cooper && Connor Aitken
#4/12/16
#STORC
#This script takes a reading from the pH sensor and writes it to a database
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
cur.execute("create table if not exists ph(date DATETIME,ec varchar(4))")
db.commit()

#takes reading from EC sensor
ser.write('2:r')
ph  = ser.readline()



#inserts data into database 
cur.execute("INSERT INTO ph values(datetime(CURRENT_TIMESTAMP,'localtime'), (?))", (ph,))
db.commit()

#closes database connection
db.close()
#closes serial connection
ser.close()
