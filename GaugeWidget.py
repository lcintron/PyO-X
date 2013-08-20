from PyQt4 import QtGui, QtCore, Qt


class GaugeWidget(QtGui.QWidget):
 
	def __init__(self, name='', text='', initialValue=0, textformat='%f',maxValue=100,   *args, **kwargs):
		super(GaugeWidget, self).__init__(*args, **kwargs)
		self._bg = QtGui.QPixmap("speedo4.png")
		self.name = name
		self.maxValue = maxValue
		self.text = text
		self.textformat=textformat
		self.setValue(initialValue)
        
	def setValue(self, val):
		self.raw_value = val
		val = val/float(self.maxValue)
		val = float(min(max(val, 0), 1))
		self._value = -270 * val
		self.update()
 
 	def setName(self, name):
 		self.name = name
 		
 	def getName(self):
 		return self.name
 	
 	def paintEvent(self, e):
 		painter = QtGui.QPainter(self)
 		painter.setRenderHint(painter.Antialiasing)
 		rect = e.rect()
 		gauge_rect = QtCore.QRect(rect)
 		size = gauge_rect.size()
 		pos = gauge_rect.center()
 		gauge_rect.moveCenter( QtCore.QPoint(pos.x()-size.width(), pos.y()-size.height()) )
		gauge_rect.setSize(size*.9)
		gauge_rect.moveCenter(pos)

		refill_rect = QtCore.QRect(gauge_rect)
		size = refill_rect.size()
		pos = refill_rect.center()
		refill_rect.moveCenter( QtCore.QPoint(pos.x()-size.width(), pos.y()-size.height()) )
		# smaller than .9 == thicker gauge
		refill_rect.setSize(size*.9)
		refill_rect.moveCenter(pos)
		painter.setPen(QtCore.Qt.NoPen)
		painter.drawPixmap(rect, self._bg )
		painter.save()
		grad = QtGui.QConicalGradient(QtCore.QPointF(gauge_rect.center()), 270.0)
		grad.setColorAt(.75, QtCore.Qt.green)
		grad.setColorAt(.5, QtCore.Qt.yellow)
		grad.setColorAt(.1, QtCore.Qt.red)
		painter.setBrush(grad)
		painter.drawPie(gauge_rect, 225.0*16, self._value*16)
		painter.restore()
		painter.setBrush(QtGui.QBrush(self._bg.scaled(rect.size())))
		painter.drawEllipse(refill_rect)
		
		painter.setPen(QtGui.QColor(168, 34, 3))
		fontSize=size.width()*.06
		gauge_rect.moveCenter(QtCore.QPoint(pos.x(), pos.y()+3*fontSize))
		painter.setFont(QtGui.QFont('AnyStyle',fontSize))
		painter.drawText(gauge_rect, QtCore.Qt.AlignCenter, self.text)
		
		fontSize=size.width()*.20
		gauge_rect.moveCenter(QtCore.QPoint(pos.x(), pos.y()-1*fontSize))
		painter.setFont(QtGui.QFont('AnyStyle',fontSize))
		txt = '0' if self.raw_value is 0 else self.textformat % self.raw_value
		painter.drawText(gauge_rect,QtCore.Qt.AlignCenter, str(txt))
		painter.end()	
		super(GaugeWidget,self).paintEvent(e)
