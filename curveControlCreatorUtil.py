import maya.cmds as cmds
import importlib
from . import curveClass
importlib.reload(curveClass)

COLOR_INDEX = {
	'Default': 5,
	'LightBlue': 18,
	'Yellow': 17,
	'Red': 13,
	'Pink': 9
}

def createCurveControl(base_name, shape, scale=1.0, createGroup=True, color=None):
	sel = cmds.ls(selection=True, type='joint')
	if not sel:
		cmds.warning('⚠ No joint selected. Please select a joint to snap the control.')
		return None, None
	target_joint = sel[0]

	base_ctrl_name = f'{base_name}_ctrl'
	base_grp_name = f'{base_name}_ctrl_grp'

	ctrl_name = base_ctrl_name
	grp_name = base_grp_name

	index = 1
	while cmds.objExists(ctrl_name) or cmds.objExists(grp_name):
		ctrl_name = f'{base_ctrl_name}{index}'
		grp_name = f'{base_grp_name}{index}'
		index += 1

	curve_obj = curveClass.Curve(ctrl_name, shape)
	ctrl = curve_obj.name
	ctrl = cmds.ls(ctrl, long=True)[0]

	setCurveColor(ctrl, color)

	grp = None
	if createGroup:
		grp = cmds.group(ctrl, name=grp_name)

	if grp and target_joint:
		try:
			cmds.delete(cmds.parentConstraint(target_joint, grp, mo=False))
			cmds.delete(cmds.scaleConstraint(target_joint, grp, mo=False))
			cmds.xform(grp, cp=True)

		except Exception as e:
			cmds.warning(f'⚠ Failed to snap group: {e}')

	if cmds.objExists(grp):
		cmds.select(grp, r=True)

	if grp and scale != 1.0:
		cmds.scale(scale, scale, scale, grp, absolute=True)
	
	return grp, ctrl

def setCurveColor(ctrl, color):
	color_id = COLOR_INDEX.get(color, 5)
	shapes = cmds.listRelatives(ctrl, shapes=True, fullPath=True) or []
	for shape in shapes:
		cmds.setAttr(shape + ".overrideEnabled", 1)
		cmds.setAttr(shape + ".overrideColor", color_id)
