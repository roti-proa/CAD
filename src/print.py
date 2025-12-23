import FreeCADGui
view = FreeCADGui.ActiveDocument.ActiveView
print("Camera type:", view.getCameraType())
print("View direction:", view.getViewDirection())
print("Camera position:", view.viewPosition())
