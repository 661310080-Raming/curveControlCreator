try:
	from PySide6 import QtCore, QtGui, QtWidgets
	from shiboken6 import wrapInstance
except:
	from PySide2 import QtCore, QtGui, QtWidgets
	from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui
import importlib

from . import config
importlib.reload(config)

class CurveControlCreator(QtWidgets.QDialog):
	def __init__(self, parent=None):
		super().__init__(parent)

		self.setWindowTitle('Curve Control Creator💫')
		self.resize(400,300)

		self.mainLayout = QtWidgets.QVBoxLayout()
		self.setLayout(self.mainLayout)

		self.nameLayout = QtWidgets.QHBoxLayout()
		self.nameLabel = QtWidgets.QLabel('Name:')
		self.nameLineEdit = QtWidgets.QLineEdit()
		self.suffixLabel = QtWidgets.QLabel('_ctrl')
		self.nameLayout.addWidget(self.nameLabel)
		self.nameLayout.addWidget(self.nameLineEdit)
		self.nameLayout.addWidget(self.suffixLabel)
		self.mainLayout.addLayout(self.nameLayout)

		self.shapeLayout = QtWidgets.QHBoxLayout()
		self.shapeLabel = QtWidgets.QLabel('Shape:')
		self.shapeCombo = QtWidgets.QComboBox()
		self.shapeCombo.addItems(config.CURVE)
		self.shapeCombo.setFixedWidth(400)
		self.shapeLayout.addWidget(self.shapeLabel)
		self.shapeLayout.addWidget(self.shapeCombo)
		self.mainLayout.addLayout(self.shapeLayout)

		self.orientLayout = QtWidgets.QHBoxLayout()
		self.orientLabel = QtWidgets.QLabel('Orientation:')
		self.xyRadio = QtWidgets.QRadioButton('XY')
		self.yzRadio = QtWidgets.QRadioButton('YZ')
		self.xzRadio = QtWidgets.QRadioButton('XZ')
		self.xyRadio.setChecked(True)
		self.orientLayout.addWidget(self.orientLabel)
		self.orientLayout.addWidget(self.xyRadio)
		self.orientLayout.addWidget(self.yzRadio)
		self.orientLayout.addWidget(self.xzRadio)
		self.mainLayout.addLayout(self.orientLayout)

		colorLayout = QtWidgets.QHBoxLayout()
		colorLabel = QtWidgets.QLabel('Color:')
		colorLayout.addWidget(colorLabel)
		self.colorGroup = QtWidgets.QButtonGroup()
		self.colorButtons = {}
		colors = {
			'Default': '#000080',
			'LightBlue': '#00FFFF',
			'Green': '#66FF66',
			'Yellow': '#FFD700',
			'Red': '#FF5050',
			'Pink': '#FF0099'
		
		}

		for name, hexval in colors.items():
			btn = QtWidgets.QPushButton()
			btn.setFixedSize(60, 25)
			btn.setStyleSheet(f'background-color:{hexval}; border:2px solid #888; border-radius:5px;')
			btn.setCheckable(True)
			self.colorGroup.addButton(btn)
			self.colorButtons[btn] = name
			colorLayout.addWidget(btn)

		self.mainLayout.addLayout(colorLayout)

		self.scaleLayout = QtWidgets.QHBoxLayout()
		self.scaleLabel = QtWidgets.QLabel('Scale:')
		self.scaleSlider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
		self.scaleSlider.setMinimum(1)
		self.scaleSlider.setMaximum(10)
		self.scaleSlider.setValue(10)
		self.scaleValueLabel = QtWidgets.QLabel('10.0')
		self.scaleLayout.addWidget(self.scaleLabel)
		self.scaleLayout.addWidget(self.scaleSlider)
		self.scaleLayout.addWidget(self.scaleValueLabel)
		self.mainLayout.addLayout(self.scaleLayout)

		self.freezeCheck = QtWidgets.QCheckBox('Freeze Transform')
		self.groupCheck = QtWidgets.QCheckBox('Create Group (_grp)')
		self.mainLayout.addWidget(self.freezeCheck)
		self.mainLayout.addWidget(self.groupCheck)

		self.buttonLayout = QtWidgets.QHBoxLayout()
		self.mainLayout.addLayout(self.buttonLayout)
		self.createButton = QtWidgets.QPushButton('Create🪄')
		self.cancelButton = QtWidgets.QPushButton('Cancel❌')
		self.buttonLayout.addWidget(self.createButton)
		self.buttonLayout.addWidget(self.cancelButton)

def run():
	global ui
	try:
		ui.close()
	except:
		pass
	ptr = wrapInstance(int(omui.MQtUtil.mainWindow()), QtWidgets.QWidget)
	ui = CurveControlCreator(parent=ptr)
	ui.show()
