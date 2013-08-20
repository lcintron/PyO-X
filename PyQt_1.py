#!/usr/bin/python
#-*- coding: utf-8 -*-
import obd_io
import serial
import platform
import obd_sensors
import time
import sys
from obd_utils import scanSerial
from random import randint
from PyQt4 import QtGui
from PyQt4 import QtCore
from datetime import datetime



class ObdThread(QtCore.QThread):
	def __init__(self, log_items, labels_collection):
		QtCore.QThread.__init__(self)
		self.labels_collection = labels_collection
		self.port = None
		self.sensorlist = []
		for item in log_items:
			self.add_log_item(item)
		self.gear_ratios = [34/13, 39/21, 36/23, 27/20, 26/21, 25/22]
	
	def connect(self):
		portnames = scanSerial()
		print 'Connecting...'
		while self.port is None:
			for port in portnames:
				self.port = obd_io.OBDPort(port, None, 2, 2)
				if(self.port.State == 0):
					self.port.close()
					self.port = None
				else:
					print 'Connected!    '
					break
	
	def is_connected(self):
		return self.port
		
	def add_log_item(self, item):
		for index, e in enumerate(obd_sensors.SENSORS):
			if(item == e.shortname):
				self.sensorlist.append(index)
				break
	
	def is_connected(self):
		return self.port
		
	def add_log_item(self, item):
		for index, e in enumerate(obd_sensors.SENSORS):
			if(item == e.shortname):
				self.sensorlist.append(index)
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

	def update(self):
		print 'Updating with OBD data...'		
		#if(self.port is None):
		#	return None
		
		while 1:
			results = {}
			for index in self.sensorlist:
				(name, value, unit) = self.port.sensor(index)
				if self.labels_collection[name] is not None:
					self.labels_collection[name].setText(value)
				results[obd_sensors.SENSORS[index].shortname] = value;
			
			#speed = str(randint(75,80))
			#rpm = str(randint(3500,4000))
			#self.labels_collection['speed'].setText(speed)
			#self.labels_collection['rpm'].setText(rpm)
			time.sleep(.1)
			#print 'Updating speed '+ speed + ' and rpm ' + rpm
			#gear = self.calculate_gear(results["rpm"], results["speed"])	

	def run(self):
		self.connect()
		self.update()

class FullWindow(QtGui.QWidget):
	def __init__(self, log_items):
		self.log_items = log_items
		super(FullWindow, self).__init__()
		self.speed = QtGui.QLabel('###', self)
		self.speedUnit = QtGui.QLabel('mph', self)
		self.rpm = QtGui.QLabel('####', self)
		self.rpmUnit = QtGui.QLabel('rpm', self)
		self.labels_collection = {'speed': self.speed, 'rpm':self.rpm}
		self.initUI()
	
	def initUI(self):
		print 'Initializing UI...'
		uiSizes = QtGui.QDesktopWidget().availableGeometry()
		self.speed.setStyleSheet("QLabel { color:red; font-size:100px;qproperty-alignment: AlignRight;}")
		self.speed.setScaledContents(True)
		self.speedUnit.setStyleSheet("QLabel { color:white; font-size:40px;}")
		self.speed.move(uiSizes.width()/2-90, uiSizes.height()/2-200)
		self.speedUnit.move(uiSizes.width()/2+105, uiSizes.height()/2-145)
		self.rpm.setStyleSheet("QLabel { color:red; font-size:100px;qproperty-alignment: AlignRight;}")	
		self.rpm.setScaledContents(True)
		self.rpmUnit.setStyleSheet("QLabel { color:white; font-size:40px;}")
		self.rpm.move(uiSizes.width()/2-140, uiSizes.height()/2-50)	
		self.rpmUnit.move(uiSizes.width()/2+124, uiSizes.height()/2+5)
		palette1 = QtGui.QPalette()
		palette1.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QImage("image.png")))
		self.setPalette(palette1)
		#self.showFullScreen()
		self.setWindowTitle("pyO-X")
		self.show()
	
	def hideLabels(self):
		self.speed.hide()
		self.speedUnit.hide()
		self.rpm.hide()
		self.rpmUnit.hide()

	def startOBD(self):
		self.obdthread = ObdThread(self.log_items, self.labels_collection)
		self.obdthread.start()

def main():
	app = QtGui.QApplication(sys.argv)
	logitems = ["rpm", "speed"]
	ex = FullWindow(logitems)
	ex.startOBD()
	sys.exit(app.exec_())

if __name__=='__main__':
	main()
