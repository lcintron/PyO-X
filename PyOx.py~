#!/usr/bin/python
#-*- coding: utf-8 -*-
import platform
import time
import sys
import styles
from pyox_obdthread import pyox_obdthread
from random import randint
from PyQt4 import QtGui
from PyQt4 import QtCore
from datetime import datetime
from GaugeWidget import GaugeWidget

class PyOX_Gui(QtGui.QWidget):
	def __init__(self, log_items):
		self.log_items = log_items
		super(PyOX_Gui, self).__init__()
		
		#This label is required to be sent to the pyox_obdthread class
		#as the class makes a default call to it.
		self.connecting = QtGui.QLabel("Connecting...", self)
		self.speed = QtGui.QLabel('###', self)
		self.speedUnit = QtGui.QLabel('mph', self)
		self.rpm = QtGui.QLabel('####', self)
		self.rpmUnit = QtGui.QLabel('rpm', self)
		self.labels_collection = {'speed': self.speed
								, 'rpm':self.rpm
								, 'connecting':self.connecting
								, 'lbl1':self.speedUnit
								, 'lbl2':self.rpmUnit}
		self.initUI()
	
	#initialize ui components
	def initUI(self):
		uiSizes = QtGui.QDesktopWidget().availableGeometry()
		self.connecting.setStyleSheet(styles.stylesObd['style2'])
		self.connecting.move(20, 20)
		self.speed.setStyleSheet(styles.stylesObd['style1'])
		self.speed.setScaledContents(True)
		self.speedUnit.setStyleSheet(styles.stylesObd['style2'])
		self.speed.move(uiSizes.width()/2-90, uiSizes.height()/2-200)
		self.speedUnit.move(uiSizes.width()/2+105, uiSizes.height()/2-145)
		self.rpm.setStyleSheet(styles.stylesObd['style1'])	
		self.rpm.setScaledContents(True)
		self.rpmUnit.setStyleSheet(styles.stylesObd['style2'])
		self.rpm.move(uiSizes.width()/2-140, uiSizes.height()/2-50)	
		self.rpmUnit.move(uiSizes.width()/2+124, uiSizes.height()/2+5)
		palette1 = QtGui.QPalette()
		palette1.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QImage("image.png")))
		self.setPalette(palette1)
		#self.showFullScreen()
		self.setWindowTitle("PyO-X")
		self.show()

	#creates and starts a new thread that reads the obd2 port and updates the ui
	def start_obd(self):
		self.obdthread = pyox_obdthread(self.log_items, self.labels_collection)
		self.obdthread.start()

def main():
	app = QtGui.QApplication(sys.argv)
	logitems = ["rpm", "speed"]
	ex = PyOX_Gui(logitems)
	ex.start_obd()
	sys.exit(app.exec_())

if __name__=='__main__':
	main()
