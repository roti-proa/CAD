from parameters import * 

import Part
import FreeCAD

doc = FreeCAD.ActiveDocument

# navigation marker in cabin
cabin_cam = doc.addObject("Part::Feature", "Cabin_Cam")
cabin_cam.Shape = Part.makeSphere(10)  # Small 50mm sphere
cabin_cam.Placement = FreeCAD.Placement(
    FreeCAD.Base.Vector(vaka_displacement, 0, 600),  # Center of cockpit, quite low
    FreeCAD.Rotation(FreeCAD.Base.Vector(0, 0, 0), 0))
# Make it semi-transparent so it doesn't obstruct view
cabin_cam.ViewObject.Transparency = 80
cabin_cam.ViewObject.ShapeColor = (1.0, 0.0, 0.0) 

# navigation marker on deck
deck_cam = doc.addObject("Part::Feature", "Deck_Cam")
deck_cam.Shape = Part.makeSphere(10)  # Small 50mm sphere
deck_cam.Placement = FreeCAD.Placement(
    FreeCAD.Base.Vector(vaka_displacement, 0, 1700),  # eye level standing in cockpit
    FreeCAD.Rotation(FreeCAD.Base.Vector(0, 0, 0), 0))
# Make it semi-transparent so it doesn't obstruct view
deck_cam.ViewObject.Transparency = 80
deck_cam.ViewObject.ShapeColor = (1.0, 0.0, 0.0) 

# navigation marker on deck
mast_cam = doc.addObject("Part::Feature", "Mast_Cam")
mast_cam.Shape = Part.makeSphere(10)  # Small 50mm sphere
mast_cam.Placement = FreeCAD.Placement(
    FreeCAD.Base.Vector(vaka_displacement, 0, mast_height),  # top of mast
    FreeCAD.Rotation(FreeCAD.Base.Vector(0, 0, 0), 0))
# Make it semi-transparent so it doesn't obstruct view
mast_cam.ViewObject.Transparency = 80
mast_cam.ViewObject.ShapeColor = (1.0, 0.0, 0.0) 

# navigation marker below panels
below_cam = doc.addObject("Part::Feature", "Below_Cam")
below_cam.Shape = Part.makeSphere(10)  # Small 50mm sphere
below_cam.Placement = FreeCAD.Placement(
    FreeCAD.Base.Vector(vaka_displacement - 1500, 0, 600), 
    FreeCAD.Rotation(FreeCAD.Base.Vector(0, 0, 0), 0))
# Make it semi-transparent so it doesn't obstruct view
below_cam.ViewObject.Transparency = 80
below_cam.ViewObject.ShapeColor = (1.0, 0.0, 0.0) 

def set_interior_view():
    """Set camera to interior view looking up at mast"""
    view = FreeCAD.Gui.ActiveDocument.ActiveView
    # Set the camera position and direction
    # Replace these values with what you got from Step 1
    view.setCameraType("Perspective")
    view.setViewDirection((0.26164761185646057, 0.9641122221946716, 0.04503464326262474))
    view.viewPosition(FreeCAD.Placement(
        FreeCAD.Base.Vector(vaka_displacement,-347.47,574.482),
        FreeCAD.Rotation(-15.0776,0.0,90)))

def set_cockpit_view():
    """Set camera to interior view looking up at mast"""
    view = FreeCAD.Gui.ActiveDocument.ActiveView
    # Set the camera position and direction
    # Replace these values with what you got from Step 1
    view.setCameraType("Perspective")
    view.setViewDirection((0.26164761185646057, 0.9641122221946716, 0.04503464326262474))
    view.viewPosition(FreeCAD.Placement(
        FreeCAD.Base.Vector(vaka_displacement,-347.47,1700),
        FreeCAD.Rotation(-15.0776,0.0,90)))
    
def set_mast_view():
    """Set camera to interior view looking up at mast"""
    view = FreeCAD.Gui.ActiveDocument.ActiveView
    # Set the camera position and direction
    # Replace these values with what you got from Step 1
    view.setCameraType("Perspective")
    view.setViewDirection((0.26164761185646057, 0.9641122221946716, 0.04503464326262474))
    view.viewPosition(FreeCAD.Placement(
        FreeCAD.Base.Vector(vaka_displacement,-347.47,mast_height),
        FreeCAD.Rotation(-15.0776,0.0,90)))
    
def set_below_view():
    """Set camera to interior view looking up at mast"""
    view = FreeCAD.Gui.ActiveDocument.ActiveView
    # Set the camera position and direction
    # Replace these values with what you got from Step 1
    view.setCameraType("Perspective")
    view.setViewDirection((0.26164761185646057, 0.9641122221946716, 0.04503464326262474))
    view.viewPosition(FreeCAD.Placement(
        FreeCAD.Base.Vector(vaka_displacement - 1500, -350.0, freeboard / 2),
        FreeCAD.Rotation(-15.0776,0.0,90)))
    
def set_sail_view():
    """Set camera to interior view looking up at mast"""
    view = FreeCAD.Gui.ActiveDocument.ActiveView
    # Set the camera position and direction
    # Replace these values with what you got from Step 1
    view.setCameraType("Perspective")
    view.setViewDirection((-0.778121292591095, 0.6084865927696228, -0.15579243004322052))
    view.viewPosition(FreeCAD.Placement(
        FreeCAD.Base.Vector(14120.5,-9740.7,6543.77),
        FreeCAD.Rotation(52.0205,-0.289763,81.0371)))
    
# get camera position in FreeCAD UI

# >>> import FreeCADGui
# >>> view = FreeCADGui.ActiveDocument.ActiveView
# >>> print("Camera type:", view.getCameraType())
# >>> print("View direction:", view.getViewDirection())
# >>> print("Camera position:", view.viewPosition())
