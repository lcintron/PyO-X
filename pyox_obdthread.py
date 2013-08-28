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

#Performs coupling between UI layer and the OBD connection to the Vehicle.
class pyox_obdthread(QtCore.QThread):
	def __init__(self, log_items, labels_collection):
		QtCore.QThread.__init__(self)
		self.labels_collection = labels_collection
		self.port = None
		self.sensorlist = []
		for item in log_items:
			self.add_log_item(item)
		self.gear_ratios = [34/13, 39/21, 36/23, 27/20, 26/21, 25/22]
	
	def showdisconnected(self):
		for index, e in enumerate(self.labels_collection):
			if e == 'connecting':
				self.labels_collection[e].setVisible(True)
			else:
				self.labels_collection[e].setVisible(False)

	def showconnected(self):
		for index, e in enumerate(self.labels_collection):
			if index == 'connecting':
				self.labels_collection[e].setVisible(False)
			else:
				self.labels_collection[e].setVisible(True)

	def connect(self):
		portnames = scanSerial()
		dot = 0
		while self.port is None:
			self.showdisconnected()
			if dot == 0:
				self.labels_collection['connecting'].setText('Connecting')
			elif dot == 1 :
				self.labels_collection['connecting'].setText('Connecting.')
			elif dot == 2:
				self.labels_collection['connecting'].setText('Connecting..')
			else:
				self.labels_collection['connecting'].setText('Connecting...')

			for port in portnames:
				self.port = obd_io.OBDPort(port, None, 2, 2)
				if(self.port.State == 0):
					self.port.close()
					self.port = None
				else:
					print 'Connected!'
					self.showconnected()
					break
			time.sleep(.1)
			dot = dot+1 if dot<4 else 0
	
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

	def run(self):
		while 1:
			#self.connect()
			#self.read_obd()
			self.simulate_obd()
			time.sleep(.01)


	def read_obd(self):
		for index in self.sensorlist:
			(name, value, unit) = self.port.sensor(index)
			key = obd_sensors.SENSORS[index].shortname
			if self.labels_collection[key] is not None:
				self.labels_collection[key].setText(str(value))
	
	#Debuging.. Simulate speed and rpm values.
	def simulate_obd(self):
		speed = str(randint(75,80))
		rpm = str(randint(3500,4000))
		self.labels_collection['speed'].setText(speed)
		self.labels_collection['rpm'].setText(rpm)
		#cleargear = self.calculate_gear(rpm, speed)	
