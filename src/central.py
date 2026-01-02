# all parts that are central (symmetric along the transversal axis)
# vaka, ama spine, sole, overhead, central stanchions

import FreeCAD
import Part
from FreeCAD import Base
import math

from colors import *
from parameters import *
from shapes import *
from material import *

def central(vessel):

    # spine (longitudinal beam to support the akas)

    spine = vessel.newObject("Part::Feature", "Spine (aluminum)")
    spine.Shape = shs_capped(spine_width,
                             spine_thickness,
                             spine_length,
                             aka_cap_diameter,
                             aka_cap_thickness)
                             
    spine.Placement = FreeCAD.Placement(
        Base.Vector(- spine_width / 2, spine_length / 2, spine_base_level),
        FreeCAD.Rotation(Base.Vector(1, 0, 0), 90))
    set_color(spine, color_aluminum)

    # make a box for the cockpit to cut
    
    cockpit_cutter = Part.makeBox(
        vaka_width + 1000, 
        cockpit_length,
        overhead_thickness + 100)
    cockpit_cutter_placement = FreeCAD.Placement(
        Base.Vector(vaka_x_offset - vaka_width - 500,
                    - cockpit_length / 2,
                    overhead_base_level - 50), 
        FreeCAD.Rotation(Base.Vector(0, 0, 0), 0))
    cockpit_cutter_transformed = cockpit_cutter.transformGeometry(
        cockpit_cutter_placement.toMatrix())
    
    # overhead (ceiling of cabin)
    
    overhead = vessel.newObject("Part::Feature", "Overhead (plywood)")
    overhead.Shape = elliptical_cylinder(vaka_length,
                                         vaka_width,
                                         overhead_thickness)
    overhead.Placement = FreeCAD.Placement(
        Base.Vector(vaka_x_offset, 0, overhead_base_level),
        FreeCAD.Rotation(Base.Vector(0, 0, 1), 90))
    overhead.Shape = overhead.Shape.cut(cockpit_cutter_transformed)
    set_color(overhead, color_plywood)

    # bottom: part of the hull below the sole
    bottom = vessel.newObject("Part::Feature", "Bottom (fiberglass)")
    # Create the flat bottom cylinder to cut from bottom
    bottom_cylinder = elliptical_cylinder(vaka_length + 5,
                                          vaka_width + 5,
                                          bottom_height + 5)
    # Create an ellipsoid for bottom, height = 2 * bottom_thickness
    # This will create a curved bottom shape
    bottom_ellipsoid = ellipsoid(vaka_length, 
                                 vaka_width, 
                                 bottom_height * 2)
    bottom_ellipsoid_inner = ellipsoid(
        vaka_length - 2 * bottom_thickness, 
        vaka_width - 2 * bottom_thickness, 
        bottom_height * 2 - 2 * bottom_thickness)
    # Intersect the cylinder with the ellipsoid to get the curved bottom
    bottom.Shape = (bottom_ellipsoid.cut(bottom_cylinder)
                    .cut(bottom_ellipsoid_inner))
    bottom.Placement = FreeCAD.Placement(
        Base.Vector(vaka_x_offset, 0, bottom_height),
        FreeCAD.Rotation(Base.Vector(0, 0, 1), 90))
    set_color(bottom, color_bottom)

    # foam_below_sole 
    foam_below_sole = vessel.newObject("Part::Feature", "Foam_Below_Sole (foam)")
    foam_below_sole.Shape = bottom_ellipsoid_inner.cut(bottom_cylinder)
    foam_below_sole.Placement = FreeCAD.Placement(
        Base.Vector(vaka_x_offset, 0, bottom_height),
        FreeCAD.Rotation(Base.Vector(0, 0, 1), 90))
    
    # sole: floor of cabin
    sole = vessel.newObject("Part::Feature", "Sole (plywood)")
    # Create the flat bottom cylinder to cut from bottom
    sole.Shape = elliptical_cylinder(vaka_length - 2 * vaka_thickness,
                                          vaka_width - 2 * vaka_thickness,
                                          sole_thickness)
    sole.Placement = FreeCAD.Placement(
        Base.Vector(vaka_x_offset, 0, bottom_height),
        FreeCAD.Rotation(Base.Vector(0, 0, 1), 90))
    set_color(sole, color_sole)
    
    # hull: exterior from sole base level (bottom height) upwards
    #       to gunwale base level
    hull = vessel.newObject("Part::Feature", "Hull (fiberglass)")
    hull.Shape = elliptical_pipe(vaka_length,
                                 vaka_width,
                                 vaka_thickness,
                                 freeboard)
    hull.Placement = FreeCAD.Placement(
        Base.Vector(vaka_x_offset, 0, bottom_height),
        FreeCAD.Rotation(Base.Vector(0, 0, 1), 90))
    set_color(hull, color_hull_exterior)

    gunwale = vessel.newObject("Part::Feature", "Gunwale (wood)")
    gunwale.Shape = elliptical_pipe(vaka_length, vaka_width,
                                    gunwale_width, gunwale_height)
    gunwale.Placement = FreeCAD.Placement(
        Base.Vector(vaka_x_offset, 0, gunwale_base_level),
        FreeCAD.Rotation(Base.Vector(0, 0, 1), 90))
    set_color(gunwale, color_hull_exterior)

    outer_crossdeck_stanchion = vessel.newObject("Part::Feature",
                                              "Outer_Crossdeck_Stanchion (steel)")
    outer_crossdeck_stanchion.Shape = pipe(stanchion_diameter,
                                           stanchion_thickness,
                                           stanchion_length)
    outer_crossdeck_stanchion.Placement = FreeCAD.Placement(
        Base.Vector(0,
                    0,
                    aka_base_level),
        FreeCAD.Rotation(Base.Vector(0, 0, 0), 0))
    set_color(outer_crossdeck_stanchion, color_aluminum)

    center_crossdeck_stanchion = (
        vessel.newObject("Part::Feature",
                         "Center_Crossdeck_Stanchion (aluminum)"))
    center_crossdeck_stanchion.Shape = pipe(stanchion_diameter,
                                            stanchion_thickness,
                                            stanchion_length)
    center_crossdeck_stanchion.Placement = FreeCAD.Placement(
        Base.Vector(crossdeck_length / 2,
                    0,
                    aka_base_level),
        FreeCAD.Rotation(Base.Vector(0, 0, 0), 0))
    set_color(center_crossdeck_stanchion, color_aluminum)

    motor_backing_plate = (
        vessel.newObject("Part::Feature",
                         "Motor_Backing_Plate (aluminum)"))
    motor_backing_plate.Shape = Part.makeBox(
        motor_backing_plate_thickness * 2 + vaka_thickness,
        motor_backing_plate_length,
        motor_backing_plate_height)
    motor_backing_plate.Placement = FreeCAD.Placement(
        Base.Vector(vaka_x_offset - vaka_width / 2 - motor_backing_plate_thickness,
                    - motor_backing_plate_length / 2,
                    motor_backing_plate_above_sole),
        FreeCAD.Rotation(Base.Vector(0, 0, 0), 0))
    set_color(center_crossdeck_stanchion, color_aluminum)

    side_board_plate = (
        vessel.newObject("Part::Feature",
                         "Side_Board_Plate (aluminum)"))
    side_board_plate.Shape = Part.makeBox(
        side_board_plate_thickness * 2 + vaka_thickness,
        side_board_plate_length,
        side_board_plate_height)
    side_board_plate.Placement = FreeCAD.Placement(
        Base.Vector(vaka_x_offset + vaka_width / 2
                    - side_board_plate_thickness - vaka_thickness,
                    - side_board_plate_length / 2,
                    side_board_plate_above_sole),
        FreeCAD.Rotation(Base.Vector(0, 0, 0), 0))
    set_color(center_crossdeck_stanchion, color_aluminum)

