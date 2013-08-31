import sys
import time
from PyQt4 import QtGui, QtCore, Qt
from GaugeWidget import GaugeWidget

class pygauge_thread(QtCore.QThread):
	def __init__(self, gauges):
		QtCore.QThread.__init__(self)
		self.gauges = gauges
		
	def run(self):
		x = 0
		while x<100:
			for gauge in self.gauges:
				gauge.setValue(x)
			time.sleep(.1)
			x = 0 if x ==99 else x+0.01
		
 
class Example(QtGui.QWidget):
	def __init__(self):
		super(Example, self).__init__()

		self.setGeometry(0, 0,350,700)
		self.move(300, 200)
		self.setWindowTitle('Dial Guage')

		layout = QtGui.QVBoxLayout(self)
		self.gauge = GaugeWidget('oiltemp','oil temp',0, 100,"{0:.0f}" )
		self.gauge.setSizePolicy(QtGui.QSizePolicy(
		QtGui.QSizePolicy.Expanding,
			QtGui.QSizePolicy.Expanding))
		layout.addWidget(self.gauge)
		
		self.gauge2 = GaugeWidget('mph','mph',0,100)
		self.gauge2.setSizePolicy(QtGui.QSizePolicy(
			QtGui.QSizePolicy.Expanding,
			QtGui.QSizePolicy.Expanding))
		
		self.gauges = [self.gauge, self.gauge2]
		layout.addWidget(self.gauge2)
		self.show()

	def run(self):
		self.pygauge_thread1 = pygauge_thread(self.gauges)
		self.pygauge_thread1.start()
 

       
def main():
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    #ex.raise_()
    ex.run()
    sys.exit(app.exec_())


 
 
if __name__ == '__main__':
    main()


