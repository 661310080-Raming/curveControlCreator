try:
	from PySide6 import QtCore, QtGui, QtWidgets
	from shiboken6 import wrapInstance
except:
	from PySide2 import QtCore, QtGui, QtWidgets
	from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui
import importlib

from . import config
from . import curveControlCreatorUtil as ccutil
importlib.reload(config)
importlib.reload(ccutil)

class CurveControlCreator(QtWidgets.QDialog):
	def __init__(self, parent=None):
		super().__init__(parent)

		self.setWindowTitle('Curve Control Creator💫')
		self.resize(400,200)

		self.mainLayout = QtWidgets.QVBoxLayout()
		self.setLayout(self.mainLayout)
		self.setStyleSheet(
			'''
				QDialog{
					background-color: #4c493e;
				}
				QLabel{
					color: White;
				}
				QCheckBox{
					color: White;
				}
				QRadioButton{
					color: White;
				}
			
			'''
		)

		self.nameLayout = QtWidgets.QHBoxLayout()
		self.nameLabel = QtWidgets.QLabel('Name:')
		self.nameLineEdit = QtWidgets.QLineEdit()
		self.nameLineEdit.setStyleSheet(
			'''
				QLineEdit {
					background-color: #a4d9d5;
					color: Black;
					border-radius: 8px;
				}
			'''
		)

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
		self.shapeCombo.setStyleSheet(
			'''
				QComboBox {
					background-color: #ffdf62;
					color: Black;
				}
			'''
		)

		self.shapeLayout.addWidget(self.shapeLabel)
		self.shapeLayout.addWidget(self.shapeCombo)
		self.mainLayout.addLayout(self.shapeLayout)

		colorLayout = QtWidgets.QHBoxLayout()
		colorLabel = QtWidgets.QLabel('Color:')
		colorLayout.addWidget(colorLabel)

		self.colorGroup = QtWidgets.QButtonGroup(self)
		self.colorGroup.setExclusive(True)

		self.colorButtons = {}
		colors = {
			'Default': '#000080',
			'LightBlue': '#5ffaff',
			'Yellow': '#fff739',
			'Red': '#ff3333',
			'Pink': '#ff65d4'
		}

		i = 0
		for name, hexval in colors.items():
			btn = QtWidgets.QPushButton()
			btn.setFixedSize(70, 22)
			btn.setCheckable(True)
			btn.setStyleSheet(f'''
				QPushButton {{
					background-color: {hexval};
					border: 1px solid #666;
					border-radius: 4px;
				}}
				QPushButton:checked {{
					border: 2px solid white;
				}}
			''')
			self.colorGroup.addButton(btn, id=i)
			self.colorButtons[i] = name
			colorLayout.addWidget(btn)
			i += 1

		firstBtn = self.colorGroup.button(0)
		if firstBtn:
			firstBtn.setChecked(True)

		self.mainLayout.addLayout(colorLayout)

		self.scaleLayout = QtWidgets.QHBoxLayout()
		self.scaleLabel = QtWidgets.QLabel('Scale:')
		self.scaleSlider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
		self.scaleSlider.setMinimum(1)
		self.scaleSlider.setMaximum(100)
		self.scaleSlider.setValue(10)
		self.scaleSlider.valueChanged.connect(self.onScaleSlider)
		self.scaleValueLabel = QtWidgets.QLabel('10.0')
		self.scaleLayout.addWidget(self.scaleLabel)
		self.scaleLayout.addWidget(self.scaleSlider)
		self.scaleLayout.addWidget(self.scaleValueLabel)
		self.mainLayout.addLayout(self.scaleLayout)

		self.buttonLayout = QtWidgets.QHBoxLayout()
		self.mainLayout.addLayout(self.buttonLayout)
		self.createButton = QtWidgets.QPushButton('Create🪄')
		self.createButton.setStyleSheet(
			'''
				QPushButton {
					background-color: #266d95;
					border-radius: 12px;
					padding: 4px;
				}
				QPushButton:hover {
					background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #a7eaf9, stop:1 #4f97c0);
					color: Black; 
				}
				QPushButton:pressed {
					background-color: black;
				}
			'''
		)
		self.cancelButton = QtWidgets.QPushButton('Cancel❌')
		self.cancelButton.setStyleSheet(
			'''
				QPushButton {
					background-color: #af3110;
					border-radius: 12px;
					padding: 4px;
				}
				QPushButton:hover {
					background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #ffd285, stop:1 #c24524);
					color: Black; 
				}
				QPushButton:pressed {
					background-color: black;
				}
			'''
		)
		self.buttonLayout.addWidget(self.createButton)
		self.buttonLayout.addWidget(self.cancelButton)

		self.buttomLayout = QtWidgets.QHBoxLayout()
		self.mainLayout.addLayout(self.buttomLayout)
		self.freezeButton = QtWidgets.QPushButton('Freeze Translate📍')
		self.freezeButton.setEnabled(False)
		self.buttomLayout.addWidget(self.freezeButton)

		self.createButton.clicked.connect(self.onClickCreateCurveControl)
		self.cancelButton.clicked.connect(self.close)

	def onScaleSlider(self, value):
		scale_value = value / 10.0
		self.scaleValueLabel.setText(f"{scale_value:.1f}")

	def onClickCreateCurveControl(self):
		import curveControlCreator.curveControlCreatorUtil as ccutil
		name = self.nameLineEdit.text()
		shape = self.shapeCombo.currentText()
		scale_value = self.scaleSlider.value() / 10.0

		color_id = self.colorGroup.checkedId()
		color_name = self.colorButtons[color_id]

		if not name:
			QtWidgets.QMessageBox.warning(self, "Missing Name", "Please enter a name.")
			return
		
		grp, ctrl = ccutil.createCurveControl(name, shape, scale=scale_value, color=color_name)

		if ctrl:
			self.freezeButton.setEnabled(True)
			self.currentCtrl = ctrl
			self.currentGrp = grp
		
def run():
	global ui
	try:
		ui.close()
	except:
		pass
	ptr = wrapInstance(int(omui.MQtUtil.mainWindow()), QtWidgets.QWidget)
	ui = CurveControlCreator(parent=ptr)
	ui.show()
