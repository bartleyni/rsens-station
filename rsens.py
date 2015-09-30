import socket
import sys
import time
import usb.core
import MySQLdb

time.sleep(10) # wait for initialisation

dev = usb.core.find(idVendor=0x16c0, idProduct=0x5dc)

while True:
	try:
		db = MySQLdb.connect(host="RaspberryNAS.lan", user="root", passwd="raspberry", db="decibel_monitor")
		cur = db.cursor()
		ret = dev.ctrl_transfer(0xC0, 4, 0, 0, 200)
		data = (ret[0] + ((ret[1] & 3) * 256)) * 0.1 + 30
		#print "%s dB" % data
		
		try:
			cur.execute("INSERT INTO tub_raw (decibel) VALUES (%s)" % data)
			db.commit()
			cur.execute("INSERT INTO plug_raw (decibel) VALUES (%s)" % data)
			db.commit()
		except:
			db.rollback()
		db.close()
		time.sleep(0.2)
	except:
		time.sleep(10)
	


