#!/usr/bin/python
#-*- coding: utf-8 -*-
#--------------QT----------------# 
import obd_io
import serial
import platform
import obd_sensors
from datetime import datetime
import time

from obd_utils import scanSerial
#---------------end of qt-----------------#
import sys
from PyQt4 import QtGui

class FullWindow(QtGui.QWidget):
	def __init__(self, log_items):
		super(FullWindow, self).__init__()
		self.port = None
		self.sensorlist = []
		localtime = time.localtime(time.time())
		#print"Time,\tRPM,\tMPH,\tThrottle,\tLoad,\tGear\n" 
		for item in log_items:
			self.add_log_item(item)
		self.gear_ratios = [34/13, 39/21, 36/23, 27/20, 26/21, 25/22]
		#Labels
		self.speed = QtGui.QLabel('---', self)
		self.speedUnit = QtGui.QLabel('mph', self)
		self.rpm = QtGui.QLabel('----', self)
		self.rpmUnit = QtGui.QLabel('rpm', self)
		#EndLabels

		
		self.initUI()
		self.connect()
	
	def connect(self):
		portnames = scanSerial()
		#print portnames
		while self.port is not None:
			for port in portnames:
				self.port = obd_io.OBDPort(port, None, 2, 2)
				if(self.port.State == 0):
					self.port.close()
					self.port = None
				else:
					break

		#if(self.port):
		#display connected icon
		#print "Connected to "+self.port.port.name
	
	def is_connected(self):
		return self.port
		
	def add_log_item(self, item):
		for index, e in enumerate(obd_sensors.SENSORS):
			if(item == e.shortname):
				self.sensorlist.append(index)
				#print "Logging item: "+e.name
				break
	
	def is_connected(self):
		return self.port
		
	def add_log_item(self, item):
		for index, e in enumerate(obd_sensors.SENSORS):
			if(item == e.shortname):
				self.sensorlist.append(index)
				#print "Logging item: "+e.name
				break

	def calculate_gear(self, rpm, speed):
		if speed == "" or speed == 0:
			return 0
		if rpm == "" or rpm == 0:
			return 0

		rps = rpm/60
		mps = (speed*1.609*1000)/3600
		
		primary_gear = 85/46 #street triple
		final_drive  = 47/16
		
		tyre_circumference = 1.978 #meters

		current_gear_ratio = (rps*tyre_circumference)/(mps*primary_gear*final_drive)
		
		#print current_gear_ratio
		gear = min((abs(current_gear_ratio - i), i) for i in self.gear_ratios)[1] 
		return gear

	def record_data(self):
		if(self.port is None):
			return None
		
		#print "Logging started"
		while 1:
			localtime = datetime.now()
			current_time = str(localtime.hour)+":"+str(localtime.minute)+":"+str(localtime.second)+"."+str(localtime.millisecond)
			log_string = current_time
			results = {}
			for index in self.sensorlist:
				(name, value, unit) = self.port.sensor(index)
				#log_string = log_string + ",\t"+str(value)
				results[obd_sensors.SENSORS[index].shortname] = value;
			
			speed.text = results['speed'] if results['speed'].length()>2 else ' '+results['speed']
			rpm.text = results['rpm'] if results['rpm'].length()>2 else ' '+ results['rpm']
			#gear = self.calculate_gear(results["rpm"], results["speed"])
			#log_string = log_string + ",\t" + str(gear)
			#print log_string+"\n"
	
	def initUI(self):
		uiSizes = QtGui.QDesktopWidget().availableGeometry()
		#speed = QtGui.QLabel('250', self)
		self.speed.setStyleSheet("QLabel { color:red; font-size:100px;qproperty-alignment: AlignRight;}")
		#speedUnit = QtGui.QLabel('mph', self)        
		self.speedUnit.setStyleSheet("QLabel { color:white; font-size:40px;}")
		self.speed.move(uiSizes.width()/2-60, uiSizes.height()/2-200)
		self.speedUnit.move(uiSizes.width()/2+105, uiSizes.height()/2-145)
		
		#rpm = QtGui.QLabel('6525', self)
		self.rpm.setStyleSheet("QLabel { color:red; font-size:100px;qproperty-alignment: AlignRight;}")	
		#lblRpm = QtGui.QLabel('rpm', self)
		self.rpmUnit.setStyleSheet("QLabel { color:white; font-size:40px;}")
		self.rpm.move(uiSizes.width()/2-100, uiSizes.height()/2-50)	
		self.rpmUnit.move(uiSizes.width()/2+124, uiSizes.height()/2+5)
		
		palette1 = QtGui.QPalette()
		palette1.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QImage("image.png")))
		
		self.setPalette(palette1)
		self.showFullScreen()
		self.setWindowTitle("pyO-X")
		self.show()
	
	def hideLabels(self):
		self.speed.hide()
		self.speedUnit.hide()
		self.rpm.hide()
		self.rpmUnit.hide()

def main():
	app = QtGui.QApplication(sys.argv)
	logitems = ["rpm", "speed", "throttle_pos", "load"]
	#o = OBD_Recorder('./', logitems)
	#o.connect()
	ex = FullWindow(logitems)
	sys.exit(app.exec_())

if __name__=='__main__':
	main()
