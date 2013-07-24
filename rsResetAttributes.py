# rsResetAttributes
# @author Roberto Rubio
# @date 2013-07-22
# @file rsResetAttributes.py

import maya.OpenMayaMPx as OpenMayaMPx
import maya.cmds as cmds


##
# Reset parameter class.
# Reset animable parameters to default values or saved values
class rsReset(OpenMayaMPx.MPxCommand):

    ##
    # rsReset Constructor.
    # @param self: Object pointer.
    # @return none
    def __init__(self):
        OpenMayaMPx.MPxCommand.__init__(self)

    ##
    # rsReset doIt function.
    # @param self: Object pointer.
    # @param argList: Command arguments.
    # @return none
    def doIt(self, argList):
        l_sele = cmds.ls(selection=True)
        for o_objeto in l_sele:
            atributos = cmds.listAttr(o_objeto, k=True)
            o_resetVal = "%s.Reset_Values" % (o_objeto)
            b_rvExist = False
            if cmds.objExists(o_resetVal):
                b_rvExist = True
                d_defValues = eval(cmds.getAttr("%s.Reset_Values" % (o_objeto)))
            for element in atributos:
                ValorDefecto = cmds.attributeQuery(element, node=o_objeto, ld=True)[0]
                cadenaAttr = o_objeto + "." + element
                b_lock = cmds.getAttr(cadenaAttr, lock=True)
                valor = cmds.getAttr(cadenaAttr)
                if b_rvExist == True:
                    if element in d_defValues:
                        ValorDefecto = d_defValues[element]
                if b_lock == 0:
                    if ValorDefecto != valor:
                        cmds.setAttr(cadenaAttr, ValorDefecto)


##
# Set reset parameter class.
# If parameter is not in default value, it saved value.
class rsSetReset(OpenMayaMPx.MPxCommand):

    ##
    # rsSetReset Constructor.
    # @param self: Object pointer.
    # @return none
    def __init__(self):
        OpenMayaMPx.MPxCommand.__init__(self)

    ##
    # rsSetReset doIt function.
    # @param self: Object pointer.
    # @param argList: Command arguments.
    # @return none
    def doIt(self, argList):
        l_sele = cmds.ls(selection=True)
        for o_obj in l_sele:
            s_dict = ""
            o_resetVal = "%s.Reset_Values" % (o_obj)
            if cmds.objExists(o_resetVal):
                cmds.setAttr(o_resetVal, lock=False)
                cmds.deleteAttr(o_resetVal)
            l_attributes = cmds.listAttr(o_obj, k=True)
            for o_attr in l_attributes:
                f_defVal = cmds.attributeQuery(o_attr, node=o_obj, ld=True)
                f_val = cmds.getAttr("%s.%s" % (o_obj, o_attr))
                if f_defVal != None and f_defVal[0] != f_val:
                    if s_dict == "":
                        s_dict = "{"
                    s_temp = "\"%s\":%s}" % (o_attr, str(f_val))
                    if s_dict == "{":
                        s_dict = s_dict + s_temp
                    else:
                        s_dict = s_dict.replace("}", " ,%s" % (s_temp))
            if s_dict != "":
                cmds.select(o_obj)
                cmds.addAttr(dt="string", shortName="rv", longName="Reset_Values")
                cmds.setAttr(o_resetVal, s_dict, type="string")
                cmds.setAttr(o_resetVal, lock=True)
        cmds.select(l_sele)


##
# Creating instance event.
# @param none.
# @return rsReset instance
def creatorReset():
    return OpenMayaMPx.asMPxPtr(rsReset())


##
# Creating instance event.
# @param none.
# @return rsSetReset instance
def creatorSet():
    return OpenMayaMPx.asMPxPtr(rsSetReset())


##
# Load Plugin event.
# @param obj.
# @return none
def initializePlugin(obj):
    plugin = OpenMayaMPx.MFnPlugin(obj, 'Rig Studio - Developer: Roberto Rubio', '1.0', 'Any')
    try:
        plugin.registerCommand('rsReset', creatorReset)
        plugin.registerCommand('rsSetReset', creatorSet)
        plugin.addMenuItem("rsReset", "MayaWindow|mainModifyMenu", "rsReset()", "")
        plugin.addMenuItem("rsSetReset", "MayaWindow|mainCharactersMenu", "rsSetReset()", "")
    except:
        raise RuntimeError('Failed to register command')
    


##
# Unload Plugin event.
# @param obj.
# @return none
def uninitializePlugin(obj):
    plugin = OpenMayaMPx.MFnPlugin(obj)
    try:
        plugin.deregisterCommand('rsReset')
        plugin.deregisterCommand('rsSetReset')
        cmds.deleteUI("MayaWindow|mainModifyMenu|rsReset")
        cmds.deleteUI("MayaWindow|mainCharactersMenu|rsSetReset")
    except:
        raise RuntimeError('Failed to unregister command')