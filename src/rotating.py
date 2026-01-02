import FreeCAD
import Part
from FreeCAD import Base
import math

from colors import *
from parameters import *
from shapes import *

# rig: masts and sails

def rig(the_rig, sail_angle=0, sail_camber=10000):
    """
    Build a rig with rotatable sail
    sail_angle: rotation angle in degrees around the yard spar axis
    """

    # mast
    
    mast = the_rig.newObject("Part::Feature", "Mast (aluminum)")
    mast.Shape = pipe(mast_diameter, mast_thickness, mast_height)
    mast.Placement = FreeCAD.Placement(
        Base.Vector(0, 0, mast_base_level),
        FreeCAD.Rotation(Base.Vector(0, 0, 0), 0))
    set_color(mast, color_aluminum)

    mast_cap = the_rig.newObject("Part::Feature", "Mast Cap (aluminum)")
    mast_cap.Shape = Part.makeCylinder(mast_cap_diameter / 2, mast_cap_thickness)    
    mast_cap.Placement = FreeCAD.Placement(
        Base.Vector(0, 0, mast_height + mast_base_level),
        FreeCAD.Rotation(Base.Vector(0, 0, 0), 0))
    set_color(mast_cap, color_aluminum)
    
    # yard spar - attachment point for the sail yard

    yard_spar = the_rig.newObject("Part::Feature",
                                  "Yard Spar (aluminum)")
    yard_spar.Shape = Part.makeBox(yard_spar_length,
                                    yard_spar_width,
                                    yard_spar_thickness)
    yard_spar.Placement = FreeCAD.Placement(
        Base.Vector(mast_diameter / 2, 
                    - yard_spar_width / 2,
                    yard_spar_height),
        FreeCAD.Rotation(Base.Vector(0, 0, 0), 0))
    set_color(yard_spar, color_aluminum)

    # yard spar brace - 45 degree brace for yard spar
    yard_spar_brace = the_rig.newObject("Part::Feature",
                                        "Yard Spar Brace (aluminum)")
    yard_spar_brace.Shape = Part.makeBox(yard_spar_length * math.sqrt(2),
                                         yard_spar_width,
                                         yard_spar_thickness)
    yard_spar_brace.Placement = FreeCAD.Placement(
        Base.Vector(mast_diameter / 2,
                    - yard_spar_width / 2,
                    mast_height),
        FreeCAD.Rotation(Base.Vector(0, 1, 0), 45))
    set_color(yard_spar, color_aluminum)
    
    # mast handle
    mast_handle = the_rig.newObject("Part::Feature", "Mast Handle (aluminum)")
    mast_handle.Shape = pipe(mast_handle_diameter,
                             mast_handle_thickness,
                             mast_handle_length)
    mast_handle.Placement = FreeCAD.Placement(
        Base.Vector(0,
                    mast_handle_length / 2,
                    deck_level + mast_handle_height_above_deck),
        FreeCAD.Rotation(Base.Vector(1, 0, 0), 90))
    set_color(yard_spar, color_aluminum)
    
    # Pivot point for sail rotation (at the yard centerline, end of yard spar)
    pivot_x = yard_spar_length + mast_diameter / 2
    pivot_y = 0
    pivot_z = yard_spar_height + yard_spar_thickness / 2
    
    # Yard - rotates around pivot point
    yard = the_rig.newObject("Part::Feature", "Yard (aluminum)")
    yard.Shape = pipe(yard_diameter, yard_thickness, yard_length)
    
    # Calculate yard position with rotation
    # Yard extends along Y in unrotated position
    angle_rad = math.radians(sail_angle)
    
    # Yard center in rotated position
    yard_offset_y = yard_length / 2 * math.cos(angle_rad)
    yard_offset_z = yard_length / 2 * math.sin(angle_rad)
    
    yard.Placement = FreeCAD.Placement(
        Base.Vector(pivot_x, pivot_y + yard_offset_y, pivot_z + yard_offset_z),
        FreeCAD.Rotation(Base.Vector(1, 0, 0), 90 + sail_angle))  # Rotate around X axis
    set_color(yard, color_bamboo)
    
    # Boom - parallel to yard, offset by sail_height VERTICALLY from the pivot
    boom = the_rig.newObject("Part::Feature", "Boom (aluminum)")
    boom.Shape = pipe(boom_diameter, boom_thickness, boom_length)
    
    # Boom rotates around the SAME pivot point as yard
    # But its unrotated position is sail_height below the pivot
    # So we need to rotate the point (0, boom_length/2, -sail_height) around the pivot
    
    # In unrotated position: boom center is at (0, boom_length/2, -sail_height) relative to pivot
    # After rotation by angle around X axis:
    boom_local_y = boom_length / 2
    boom_local_z = -sail_height
    
    # Rotate this point around X axis (pivot is origin)
    boom_offset_y = boom_local_y * math.cos(angle_rad) - boom_local_z * math.sin(angle_rad)
    boom_offset_z = boom_local_y * math.sin(angle_rad) + boom_local_z * math.cos(angle_rad)
    
    boom.Placement = FreeCAD.Placement(
        Base.Vector(pivot_x, pivot_y + boom_offset_y, pivot_z + boom_offset_z),
        FreeCAD.Rotation(Base.Vector(1, 0, 0), 90 + sail_angle))
    set_color(boom, color_bamboo)
    
    # Sail surface - hollow cylinder (thin membrane)
    
    cylinder_center_z = -sail_height / 2
    vertical_offset = sail_height / 2
    cylinder_center_x = -math.sqrt(sail_camber**2 - vertical_offset**2)
    
    # hollow cylinder
    outer_cylinder = Part.makeCylinder(sail_camber, yard_length, 
                                       Base.Vector(cylinder_center_x, -yard_length/2, cylinder_center_z),
                                       Base.Vector(0, 1, 0))
    inner_cylinder = Part.makeCylinder(sail_camber - sail_thickness, yard_length, 
                                       Base.Vector(cylinder_center_x, -yard_length/2, cylinder_center_z),
                                       Base.Vector(0, 1, 0))
    cylinder = outer_cylinder.cut(inner_cylinder)
    
    box_width = sail_camber * 2
    sail_box = Part.makeBox(box_width, yard_length, sail_height,
                            Base.Vector(0, -yard_length/2, -sail_height))
    
    sail_section = cylinder.common(sail_box)
    
    sail_section = sail_section.rotate(Base.Vector(0, 0, 0), 
                                        Base.Vector(1, 0, 0), 
                                        sail_angle)
    
    sail_section = sail_section.translate(Base.Vector(pivot_x, pivot_y, pivot_z))
    
    sail = the_rig.newObject("Part::Feature", "Sail (nylon)")
    sail.Shape = sail_section
    set_color(sail, color_sail)

# rudder: post and blade

def rudder(the_rudder, raised):

    z_offset = rudder_vaka_mount_base_level if raised else 0

    # post
    
    post = the_rudder.newObject("Part::Feature", "Rudder_Post (steel)")
    post.Shape = Part.makeCylinder(rudder_post_diameter / 2,
                                   deck_base_level + rudder_blade_height)
    post.Placement = FreeCAD.Placement(
        Base.Vector(0, 0, z_offset - rudder_blade_height),
        FreeCAD.Rotation(Base.Vector(0, 0, 0), 0))
    set_color(post, color_aluminum)

    bearing_block = the_rudder.newObject("Part::Feature", "Rudder_Bearing_Block (plastic)")
    bearing_block.Shape = Part.makeCylinder(rudder_bearing_block_diameter / 2,
                                            rudder_bearing_block_height)
    bearing_block.Placement = FreeCAD.Placement(
        Base.Vector(0, 0, stringer_base_level + z_offset),
        FreeCAD.Rotation(Base.Vector(0, 0, 0), 0))
    set_color(bearing_block, color_aluminum)

    aka_mount_pin = the_rudder.newObject("Part::Feature", "Rudder_Mount_Pin (aluminum)")
    aka_mount_pin.Shape = Part.makeCylinder(rudder_aka_mount_pin_diameter / 2,
                                            rudder_aka_mount_pin_length)
    aka_mount_pin.Placement = FreeCAD.Placement(
        Base.Vector(0,
                    rudder_aka_mount_pin_length / 2,
                    stringer_base_level + z_offset + stringer_width / 2),
        FreeCAD.Rotation(Base.Vector(1, 0, 0), 90))
    set_color(aka_mount_pin, color_aluminum)

    cap = the_rudder.newObject("Part::Feature", "Rudder_Cap (steel)")
    cap.Shape = Part.makeCylinder(rudder_aka_mount_pin_length / 2 + 10, # 10mm space
                                  deck_thickness)
    cap.Placement = FreeCAD.Placement(
        Base.Vector(0, 0, z_offset + deck_base_level),
        FreeCAD.Rotation(Base.Vector(0, 0, 0), 0))
    set_color(cap, color_aluminum)

    # cutting into tillers
    
    tiller_cutter_cylinder_shape = Part.makeCylinder(rudder_aka_mount_pin_diameter / 2,
                                            rudder_aka_mount_pin_length)
    tiller_cutter_cylinder_shape.rotate(
        Base.Vector(0,0,0),
        Base.Vector(1, 0, 0), 90)
    tiller_cutter_cylinder_shape.translate(
        Base.Vector(0,
                    rudder_aka_mount_pin_length / 2,
                    stringer_base_level + stringer_width / 2))
    tiller_cutter_box_shape = Part.makeBox(rudder_aka_mount_pin_diameter,
                                           rudder_aka_mount_pin_length,
                                           rudder_aka_mount_pin_length)
    tiller_cutter_box_shape.translate(
        Base.Vector(-rudder_aka_mount_pin_diameter / 2,
                    -rudder_aka_mount_pin_length / 2,
                    stringer_base_level + stringer_width / 2))
    # tillers (A and B): SHS rods that come from aka mount pin and go to vaka
    
    tiller_a = the_rudder.newObject("Part::Feature", "Tiller_A (aluminum)")
    tiller_a.Shape = shs(tiller_width, tiller_thickness, tiller_length)
    tiller_rot1 = FreeCAD.Rotation(Base.Vector(-1, 0, 0), 90)
    tiller_a_rot2 = FreeCAD.Rotation(Base.Vector(0, 1, 0), 90 + tiller_angle)
    tiller_a_rotation = tiller_rot1.multiply(tiller_a_rot2)    
    tiller_a.Placement = FreeCAD.Placement(
        Base.Vector(- tiller_width,
                    rudder_aka_mount_pin_length / 2,
                    stringer_base_level + tiller_width),
        tiller_a_rotation)
    tiller_a.Shape = tiller_a.Shape.cut(tiller_cutter_cylinder_shape)
    tiller_a.Shape = tiller_a.Shape.cut(tiller_cutter_box_shape)
    set_color(tiller_a, color_aluminum)
    
    tiller_b = the_rudder.newObject("Part::Feature", "Tiller_B (aluminum)")
    tiller_b.Shape = shs(tiller_width, tiller_thickness, tiller_length)
    tiller_b_rot2 = FreeCAD.Rotation(Base.Vector(0, 1, 0), 90 - tiller_angle)
    tiller_b_rotation = tiller_rot1.multiply(tiller_b_rot2)    
    tiller_b.Placement = FreeCAD.Placement(
        Base.Vector(- tiller_width,
                    - rudder_aka_mount_pin_length / 2 + tiller_width,
                    stringer_base_level + tiller_width),
        tiller_b_rotation)
    tiller_b.Shape = tiller_b.Shape.cut(tiller_cutter_cylinder_shape)
    tiller_b.Shape = tiller_b.Shape.cut(tiller_cutter_box_shape)
    set_color(tiller_b, color_aluminum)

    # steel ribs (rods) for rudder
    rib_spacing = (rudder_blade_height - 2 * rudder_rim) / (rudder_ribs - 1)
    for i in range(0, rudder_ribs):
        rib = the_rudder.newObject("Part::Feature", f"Rudder_Rib_{i} (steel)")
        rib.Shape = Part.makeCylinder(rudder_rib_diameter / 2,
                                      rudder_rib_length)
        rib.Placement = FreeCAD.Placement(
            Base.Vector(0,
                        rudder_rib_length / 2,
                        rudder_rim + i * rib_spacing +
                        z_offset - rudder_blade_height),
            FreeCAD.Rotation(Base.Vector(1, 0, 0), 90))
        set_color(rib, color_aluminum)

    # blade: thin sheet to indicate the shape of rudder
    blade = the_rudder.newObject("Part::Feature", "Rudder_Blade (plywood)")
    blade.Shape = Part.makeBox(rudder_blade_thickness,
                               rudder_blade_length,
                               rudder_blade_height)
    blade.Placement = FreeCAD.Placement(
        Base.Vector(- rudder_blade_thickness / 2,
                    - rudder_blade_length / 2,
                    z_offset - rudder_blade_height),
        FreeCAD.Rotation(Base.Vector(0, 0, 0), 0))
    set_color(blade, color_plywood)

    
