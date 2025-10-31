try:
	from PySide6 import QtCore, QtGui, QtWidgets
	from shiboken6 import wrapInstance
except:
	from PySide2 import QtCore, QtGui, QtWidgets
	from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui
import maya.cmds as cmds
import importlib
import os

from . import config
from . import curveControlCreatorUtil as ccutil
importlib.reload(config)
importlib.reload(ccutil)

IMAGE_DIR = 'C:/Users/ASUS/Documents/maya/2024/scripts/curveControlCreator/icons'

class ImageButton(QtWidgets.QPushButton):
	def __init__(self, normal_img, hover_img=None, pressed_img=None, parent=None):
		super().__init__(parent)
		self.normal_img = normal_img
		self.hover_img = hover_img or normal_img
		self.pressed_img = pressed_img or normal_img

		self.setFixedSize(200, 60)
		self.setIcon(QtGui.QIcon(self.normal_img))
		self.setIconSize(QtCore.QSize(180, 60))
		self.setFlat(True)
		self.setStyleSheet("border: none; background: transparent;")

	def enterEvent(self, event):
		self.setIcon(QtGui.QIcon(self.hover_img))
		super().enterEvent(event)

	def leaveEvent(self, event):
		self.setIcon(QtGui.QIcon(self.normal_img))
		super().leaveEvent(event)

	def mousePressEvent(self, event):
		self.setIcon(QtGui.QIcon(self.pressed_img))
		self.move(self.x(), self.y() + 2)
		super().mousePressEvent(event)

	def mouseReleaseEvent(self, event):
		self.setIcon(QtGui.QIcon(self.hover_img))
		self.move(self.x(), self.y() - 2)
		super().mouseReleaseEvent(event)

class CurveControlCreator(QtWidgets.QDialog):
	def __init__(self, parent=None):
		super().__init__(parent)

		self.setWindowTitle('Curve Control Creator💫')
		self.resize(500,500)

		self.mainLayout = QtWidgets.QVBoxLayout()
		self.setLayout(self.mainLayout)
		self.setStyleSheet(
			'''
				QDialog{
					background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #000000, stop:1 #015a51);
					background-image: url('C:/Users/ASUS/Documents/maya/2024/scripts/curveControlCreator/icons/Background.png') 0 0 0 0 stretch stretch;
					background-repeat: no-repeat;
					background-position: bottom center;
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

		self.imageLabel = QtWidgets.QLabel()
		self.imageThumb = QtGui.QPixmap(f'{IMAGE_DIR}/ThumbNail.png')
		scaledPixmap = self.imageThumb.scaled(
			QtCore.QSize(550,300),
			QtCore.Qt.KeepAspectRatio,
			QtCore.Qt.SmoothTransformation
		)

		self.imageLabel.setPixmap(scaledPixmap)
		self.imageLabel.setAlignment(QtCore.Qt.AlignCenter)

		self.mainLayout.addWidget(self.imageLabel)

		self.instructionLabel = QtWidgets.QLabel('★彡[ᴘʟᴇᴀꜱᴇ ꜱᴇʟᴇᴄᴛ ᴀ ᴊᴏɪɴᴛ ʙᴇꜰᴏʀᴇ ᴄʀᴇᴀᴛɪɴɢ ᴀ ᴄᴜʀᴠᴇ ᴄᴏɴᴛʀᴏʟ]彡★')
		self.instructionLabel.setStyleSheet(
			'''
				QLabel{
					color: #8a8a8a;
				}
			'''
		)
		self.mainLayout.addWidget(self.instructionLabel)

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

		self.suffixLabel = QtWidgets.QLabel('_CC')
		self.nameLayout.addWidget(self.nameLabel)
		self.nameLayout.addWidget(self.nameLineEdit)
		self.nameLayout.addWidget(self.suffixLabel)
		self.mainLayout.addLayout(self.nameLayout)

		self.shapeLayout = QtWidgets.QHBoxLayout()
		self.shapeLabel = QtWidgets.QLabel('Shape:')
		self.shapeCombo = QtWidgets.QComboBox()
		self.shapeCombo.addItems(config.CURVE)
		self.shapeCombo.setFixedWidth(450)
		self.shapeCombo.setStyleSheet(
			'''
				QComboBox {
					background-color: #f0f090;
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
			btn.setFixedSize(85, 22)
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
		self.scaleSlider.setStyleSheet(
			"""
				QSlider::groove:horizontal {
					background: #444;
					height: 6px;
					border-radius: 3px;
				}
				
				QSlider::handle:horizontal {
					image: url('C:/Users/ASUS/Documents/maya/2024/scripts/curveControlCreator/icons/Slider.png');  /* 👉 รูปของปุ่ม */
					width: 30px;
					height: 0px;
					margin: -8px 0;
				}
				
				QSlider::sub-page:horizontal {
					background: #00a764;
					border-radius: 3px;
				}
			"""
		)

		self.scaleLayout.addWidget(self.scaleValueLabel)
		self.mainLayout.addLayout(self.scaleLayout)

		self.buttonLayout = QtWidgets.QHBoxLayout()
		self.mainLayout.addLayout(self.buttonLayout)

		self.createButton = ImageButton(
			f"{IMAGE_DIR}/Create_normal.png",
			f"{IMAGE_DIR}/Create_hover.png",
			f"{IMAGE_DIR}/Create_pressed.png"
		)
		self.cancelButton = ImageButton(
			f"{IMAGE_DIR}/Cancel_normal.png",
			f"{IMAGE_DIR}/Cancel_hover.png",
			f"{IMAGE_DIR}/Cancel_pressed.png"
		)

		self.buttonLayout.addWidget(self.createButton)
		self.buttonLayout.addWidget(self.cancelButton)
		self.createButton.clicked.connect(self.onClickCreateCurveControl)
		self.cancelButton.clicked.connect(self.close)

		self.buttomLayout = QtWidgets.QVBoxLayout()
		self.mainLayout.addLayout(self.buttomLayout)
		self.freezeButton = QtWidgets.QPushButton('Freeze Transform📍')
		self.freezeButton.setEnabled(False)
		self.freezeButton.setStyleSheet(
			'''
				QPushButton{
					background-color: #006e57;
				}
			'''
		)
		self.deleteButton = QtWidgets.QPushButton('Delete Control🗑️')
		self.deleteButton.setEnabled(False)
		self.deleteButton.setStyleSheet(
			'''
				QPushButton{
					background-color: #006733;
				}
			'''
		)
		self.buttomLayout.addWidget(self.freezeButton)
		self.buttomLayout.addWidget(self.deleteButton)

		self.freezeButton.clicked.connect(self.onClickFreezeTransform)
		self.deleteButton.clicked.connect(self.onClickDelete)

		self.bottomImage = QtWidgets.QLabel()
		pixmap = QtGui.QPixmap('C:/Users/ASUS/Documents/maya/2024/scripts/curveControlCreator/icons/Bottom.png')
		self.bottomImage.setPixmap(pixmap)
		self.bottomImage.setScaledContents(True)
		self.bottomImage.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
		self.mainLayout.addWidget(self.bottomImage)

	def onScaleSlider(self, value):
		scale_value = value / 10.0
		self.scaleValueLabel.setText(f"{scale_value:.1f}")

		if hasattr(self, 'currentGrp') and cmds.objExists(self.currentGrp):
			cmds.scale(scale_value, scale_value, scale_value, self.currentGrp, absolute=True)

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
			self.deleteButton.setEnabled(True)
			self.currentCtrl = ctrl
			self.currentGrp = grp

	def onClickFreezeTransform(self):
		targets = []
		if hasattr(self, 'currentGrp') and cmds.objExists(self.currentGrp):
			targets.append(self.currentGrp)
		if hasattr(self, 'currentCtrl') and cmds.objExists(self.currentCtrl):
			targets.append(self.currentCtrl)

		for t in targets:
			ccutil.freeze_transform(t)

	def onClickDelete(self):
		if hasattr(self, 'currentGrp') and cmds.objExists(self.currentGrp):
			cmds.delete(self.currentGrp)

		elif hasattr(self, 'currentCtrl') and cmds.objExists(self.currentCtrl):
			cmds.delete(self.currentCtrl)
		
def run():
	global ui
	try:
		ui.close()
	except:
		pass
	ptr = wrapInstance(int(omui.MQtUtil.mainWindow()), QtWidgets.QWidget)
	ui = CurveControlCreator(parent=ptr)
	ui.show()