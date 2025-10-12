import maya.cmds as cmds
import importlib
from . import curveClass
importlib.reload(curveClass)

def createCurveControl(base_name, shape='Circle', scale=1.0, createGroup=True):
	from .curveClass import Curve
	if not base_name:
		QtWidgets.QMessageBox.warning(None, 'Missing Name', 'Please enter a name.')
		return

	ctrl_name = f'{base_name}_ctrl'
	grp_name = f'{base_name}_grp'

	curve_obj = Curve(ctrl_name, shape)
	ctrl = curve_obj.name

	grp = None
	if createGroup:
		grp = cmds.group(ctrl, name=grp_name)
	else:
		grp = ctrl

	sel = cmds.ls(selection=True, type='joint')
	if sel:
		cmds.delete(cmds.parentConstraint(sel[0], grp, mo=False))
		cmds.delete(cmds.scaleConstraint(sel[0], grp, mo=False))
	else:
		cmds.warning('No joint selected.')

	cmds.select(ctrl, r=True)
	print(f'✅ Created control: {ctrl_name} (Group: {grp_name})')

	return grp, ctrl