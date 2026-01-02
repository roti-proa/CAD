# all parts that are mirrored about the transversal axis

import FreeCAD
import Part
from FreeCAD import Base
import math

from colors import *
from parameters import *
from shapes import *
from material import *

def mirror(side):
    
    # akas (cross-beams) and pillars under each transversal row of panels

    for i in range(0, panels_longitudinal // 2):

        aka = side.newObject("Part::Feature", f"Aka_{i} (aluminum)")
        aka.Shape = rectangular_tube_capped(aka_height, aka_width, aka_thickness, aka_length,
                               aka_cap_diameter, aka_cap_thickness)
        aka.Placement = FreeCAD.Placement(
            Base.Vector(aka_length - pillar_width / 2,
                        panel_width * i + crossdeck_width / 2 +
                        panel_width / 2 - aka_width / 2,
                        aka_base_level),
            FreeCAD.Rotation(Base.Vector(0, -1, 0), 90))
        set_color(aka, color_aluminum)

        stanchion = side.newObject("Part::Feature",
                                   f"Stanchion_{i} (steel)")
        stanchion.Shape = pipe(stanchion_diameter,
                               stanchion_thickness,
                               stanchion_length)
        stanchion.Placement = FreeCAD.Placement(
            Base.Vector(aka_length - pillar_width / 2 - aka_width / 2,
                        panel_width * i + crossdeck_width / 2 +
                        panel_width / 2,
                        aka_base_level),
            FreeCAD.Rotation(Base.Vector(0, 0, 0), 0))
        set_color(stanchion, color_aluminum)
        
        pillar = side.newObject("Part::Feature", f"Pillar_{i} (aluminum)")
        pillar.Shape = shs(pillar_width, pillar_thickness, pillar_height)
        pillar.Placement = FreeCAD.Placement(
            Base.Vector(- pillar_width / 2,
                        panel_width * i + crossdeck_width / 2 +
                        panel_width / 2 - aka_width / 2,
                        ama_thickness),
            FreeCAD.Rotation(Base.Vector(0, 0, 0), 0))
        set_color(pillar, color_aluminum)
        
        # Pillar-to-aka diagonal braces (one on each side) at 45 degrees

        pillar_x = -pillar_width / 2
        
        # Y position of this pillar center
        pillar_y_kuning = (panel_width * i + crossdeck_width / 2 + panel_width / 2
                           - aka_width / 2 - stringer_width)
        
        # Lower attachment point on pillar
        pillar_z_lower = aka_base_level - pillar_brace_vertical_offset
        
        # Brace length (diagonal at 45°)
        brace_length = math.sqrt(2) * (pillar_brace_vertical_offset + spine_width)
        
        # Kuning brace
        point_lower_kuning = Base.Vector(pillar_x, pillar_y_kuning, pillar_z_lower)
        brace_kuning = side.newObject("Part::Feature", f"Pillar_Brace_Kuning_{i} (aluminum)")
        brace_kuning.Shape = shs(stringer_width, stringer_thickness, brace_length)
        brace_kuning.Placement = FreeCAD.Placement(
            point_lower_kuning,
            FreeCAD.Rotation(Base.Vector(0, 1, 0), 45))
        set_color(brace_kuning, color_aluminum)

        # Biru brace
        point_lower_biru = Base.Vector(pillar_x,
                                       pillar_y_kuning + pillar_width + stringer_width,
                                       pillar_z_lower)
        brace_biru = side.newObject("Part::Feature", f"Pillar_Brace_Biru_{i} (aluminum)")
        brace_biru.Shape = shs(stringer_width, stringer_thickness, brace_length)
        brace_biru.Placement = FreeCAD.Placement(
            point_lower_biru,
            FreeCAD.Rotation(Base.Vector(0, 1, 0), 45))
        set_color(brace_biru, color_aluminum)

    # Cross-bracing between neighboring pillars (X-shaped)
    # Add bracing between each pair of adjacent pillars

    for i in range(0, panels_longitudinal // 2 - 1):
        # Y positions of the two neighboring pillars  
        y1 = panel_width * i + crossdeck_width / 2 + panel_width / 2 
        y2 = panel_width * (i + 1) + crossdeck_width / 2 + panel_width / 2 
        
        # X position at center of pillars
        x_pillar = -pillar_width / 2
        
        # Upper corners (near spine)
        z_upper = spine_base_level - brace_upper_offset
        
        # Lower corners (near ama)
        z_lower = ama_thickness + brace_lower_offset
        
        # First diagonal of X: from (y1, upper) to (y2, lower)
        brace_1 = side.newObject("Part::Feature", f"Cross_Brace_1_{i} (aluminum)")
        point1 = Base.Vector(x_pillar, y1, z_upper)
        point2 = Base.Vector(x_pillar, y2, z_lower)
        length1 = point1.distanceToPoint(point2)
        
        brace_1.Shape = Part.makeCylinder(brace_diameter / 2, length1)
        
        # Calculate rotation to align with diagonal
        direction = point2.sub(point1)
        direction.normalize()
        
        z_axis = Base.Vector(0, 0, 1)
        rotation_axis = z_axis.cross(direction)
        rotation_angle = math.degrees(math.acos(z_axis.dot(direction)))
        brace_1.Placement = FreeCAD.Placement(
            point1,
            FreeCAD.Rotation(rotation_axis, rotation_angle))
        set_color(brace_1, color_aluminum)
        
        # Second diagonal of X: from (y1, lower) to (y2, upper)
        brace_2 = side.newObject("Part::Feature", f"Cross_Brace_2_{i} (aluminum)")
        point3 = Base.Vector(x_pillar, y1, z_lower)
        point4 = Base.Vector(x_pillar, y2, z_upper)
        length2 = point3.distanceToPoint(point4)
        
        brace_2.Shape = Part.makeCylinder(brace_diameter / 2, length2)
        
        direction2 = point4.sub(point3)
        direction2.normalize()
        
        rotation_axis2 = z_axis.cross(direction2)
        rotation_angle2 = math.degrees(math.acos(z_axis.dot(direction2)))
        brace_2.Placement = FreeCAD.Placement(
            point3,
            FreeCAD.Rotation(rotation_axis2, rotation_angle2))
        set_color(brace_2, color_aluminum)

    # aka_end supports the deck at the ends of the boat
    
    aka_end = side.newObject("Part::Feature", f"Aka End (aluminum)")
    aka_end.Shape = shs_capped(aka_width,
                           aka_thickness,
                           deck_width,
                           aka_cap_diameter,
                           aka_cap_thickness)

    aka_end.Placement = FreeCAD.Placement(
        Base.Vector(aka_length - pillar_width / 2,
                    vaka_length / 2 - aka_width,
                    aka_base_level),
        FreeCAD.Rotation(Base.Vector(0, -1, 0), 90))
    set_color(aka_end, color_aluminum)

    outer_stanchion = side.newObject("Part::Feature",
                                     "Outer Stanchion (aluminum)")
    outer_stanchion.Shape = pipe(stanchion_diameter,
                                  stanchion_thickness,
                                  stanchion_length)
    outer_stanchion.Placement = FreeCAD.Placement(
        Base.Vector(vaka_x_offset
                    + deck_width / 2 - aka_width / 2,
                    vaka_length / 2 - aka_width / 2,
                    aka_base_level),
        FreeCAD.Rotation(Base.Vector(0, 0, 0), 0))
    set_color(outer_stanchion, color_aluminum)

    center_stanchion = side.newObject("Part::Feature",
                                      "Center Stanchion (aluminum)")
    center_stanchion.Shape = pipe(stanchion_diameter,
                                  stanchion_thickness,
                                  stanchion_length)
    center_stanchion.Placement = FreeCAD.Placement(
        Base.Vector(vaka_x_offset,
                    vaka_length / 2 - aka_width / 2,
                    aka_base_level),
        FreeCAD.Rotation(Base.Vector(0, 0, 0), 0))
    set_color(center_stanchion, color_aluminum)

    inner_stanchion = side.newObject("Part::Feature",
                                      "Inner Stanchion (aluminum)")
    inner_stanchion.Shape = pipe(stanchion_diameter,
                                  stanchion_thickness,
                                  stanchion_length)
    inner_stanchion.Placement = FreeCAD.Placement(
        Base.Vector(vaka_x_offset
                    - deck_width / 2 + aka_width / 2,
                    vaka_length / 2 - gunwale_width / 2,
                    aka_base_level),
        FreeCAD.Rotation(Base.Vector(0, 0, 0), 0))
    set_color(inner_stanchion, color_aluminum)

    # stringers

    for i in range(0, panels_transversal):
        stringer_a = side.newObject("Part::Feature", f"Stringer_a_{i} (aluminum)")
        stringer_a.Shape = shs(stringer_width,
                           stringer_thickness,
                           panel_stringer_length / 2)
        stringer_a.Placement = FreeCAD.Placement(
            Base.Vector(- pillar_width / 2 + i * panel_length + panel_stringer_offset,
                        panel_stringer_length / 2,
                        stringer_base_level),
            FreeCAD.Rotation(Base.Vector(1, 0, 0), 90))
        set_color(stringer_a, color_aluminum)
    
        stringer_b = side.newObject("Part::Feature", f"Stringer_b_{i} (aluminum)")
        stringer_b.Shape = shs(stringer_width,
                           stringer_thickness,
                           panel_stringer_length / 2)
        stringer_b.Placement = FreeCAD.Placement(
            Base.Vector(- pillar_width / 2 + i * panel_length +
                        panel_stringer_offset + panel_length / 2,
                        panel_stringer_length / 2,
                        stringer_base_level),
            FreeCAD.Rotation(Base.Vector(1, 0, 0), 90))
        set_color(stringer_b, color_aluminum)

    # solar panels

    for i in range(0, panels_longitudinal // 2):
        for j in range(0, panels_transversal):
            panel = side.newObject("Part::Feature", f"Panel_{i}_{j} (solar)")
            panel.Shape = Part.makeBox(panel_length,
                                       panel_width,
                                       panel_height)
            panel.Placement = FreeCAD.Placement(
                Base.Vector(- pillar_width / 2 + j * panel_length,
                            crossdeck_width / 2 + i * panel_width,
                            panel_base_level),
                FreeCAD.Rotation(Base.Vector(0, 0, 0), 0))
            set_color(panel, color_solar_panel)

    # deck stringers

    for i in range(0, deck_stringers):
        deck_stringer = side.newObject("Part::Feature", f"Deck_Stringer_{i} (aluminum)")
        deck_stringer.Shape = shs(stringer_width,
                                  stringer_thickness,
                                  (vaka_length - cockpit_length) / 2)
        deck_stringer.Placement = FreeCAD.Placement(
            Base.Vector(vaka_x_offset - deck_width / 2 +
                        (deck_width - stringer_width) / (deck_stringers - 1) * i,
                        vaka_length / 2,
                        stringer_base_level),
            FreeCAD.Rotation(Base.Vector(1, 0, 0), 90))
        set_color(deck_stringer, color_aluminum)

    # cylinder to cut rudder cap hole into deck
    deck_cutter = Part.makeCylinder(rudder_aka_mount_pin_length / 2 + 12,
                                    1000)
    deck_cutter.translate(Base.Vector(
        vaka_x_offset - vaka_width / 2 - rudder_distance_from_vaka,
        cockpit_length / 2
        + (panels_longitudinal / 2 - 1) * panel_width
        + aka_width / 2,                          
        gunwale_base_level))
        
    # deck

    deck = side.newObject("Part::Feature", "Deck (plywood)")
    deck.Shape = Part.makeBox(deck_width,
                              (vaka_length - cockpit_length) / 2,
                              deck_thickness)
    deck.Placement = FreeCAD.Placement(
        Base.Vector(vaka_x_offset - deck_width / 2,
                    cockpit_length / 2,
                    deck_base_level),
        FreeCAD.Rotation(Base.Vector(0, 0, 0), 0))
    deck.Shape = deck.Shape.cut(deck_cutter)
    set_color(deck, color_deck)

    # mast partner: reinforced deck collar supporting mast laterally 
    # this must be here, not in rig.py (it will rotate otherwise)
    mast_partner = side.newObject("Part::Feature", "Mast Partner (wood)")
    mast_partner.Shape = Part.makeBox(
        mast_partner_length, mast_partner_width, mast_partner_thickness)
    mast_partner.Placement = FreeCAD.Placement(
        Base.Vector(vaka_x_offset - mast_partner_length / 2,
                    mast_distance_from_center - mast_partner_width / 2,
                    aka_base_level),
        FreeCAD.Rotation(Base.Vector(0, 0, 0), 0))
    set_color(mast_partner, color_plywood)

    # mast step: reinforced sole collar supporting mast laterally 
    # this must be here, not in rig.py (it will rotate otherwise)
    mast_step = side.newObject("Part::Feature", "Mast Step (aluminum)")
    mast_step.Shape = pipe(
        mast_step_outer_diameter,
        (mast_step_outer_diameter - mast_step_inner_diameter) / 2,
        mast_step_height)
    mast_step.Placement = FreeCAD.Placement(
        Base.Vector(vaka_x_offset,
                    mast_distance_from_center,
                    mast_base_level),
        FreeCAD.Rotation(Base.Vector(0, 0, 0), 0))
    set_color(mast_step, color_aluminum)

    # hull cylinder for cutting rudder vaka mounts
    
    hull_cylinder = elliptical_cylinder(vaka_length,
                                          vaka_width,
                                          1000)
    hull_cylinder.Placement = FreeCAD.Placement(
        Base.Vector(vaka_x_offset, 0, bottom_height),
        FreeCAD.Rotation(Base.Vector(0, 0, 1), 90))

    # rudder vaka mounts: braces to support the rudder

    # rudder vaka mount A: inner brace
    
    rudder_vaka_mount_a = side.newObject("Part::Feature", "Rudder_Vaka_Mount_A (aluminum)")
    rudder_vaka_mount_a_shape = shs(spine_width, spine_thickness, rudder_vaka_mount_length)
    # rotate shape around x axis first
    rudder_vaka_mount_a_shape.rotate(
        Base.Vector(0, 0, 0),
        Base.Vector(1, 0, 0),
        90)
    # then translate so that the origin aligns with the center where the pole goes
    rudder_vaka_mount_a_shape.translate(Base.Vector(-spine_width / 2, spine_width / 2, 0))
    # then rotate in y axis around origin
    rudder_vaka_mount_a_shape.rotate(
        Base.Vector(0, 0, 0),
        Base.Vector(0, 0, 1),
        135 - rudder_vaka_mount_angle)
    # translate to the correct position (somehow, ".Placement = ..." not working here)
    rudder_vaka_mount_a_shape.translate(Base.Vector(vaka_x_offset
                    - vaka_width / 2
                    - rudder_distance_from_vaka,
                    cockpit_length / 2
                    + (panels_longitudinal / 2 - 1) * panel_width
                    + aka_width / 2,
                    rudder_vaka_mount_base_level))
    rudder_vaka_mount_a_shape = rudder_vaka_mount_a_shape.cut(hull_cylinder)
    rudder_vaka_mount_a.Shape = rudder_vaka_mount_a_shape
    set_color(rudder_vaka_mount_a, color_aluminum)

    hull_cylinder_bigger = elliptical_cylinder(vaka_length + rudder_vaka_backing_plate_thickness,
                                          vaka_width + rudder_vaka_backing_plate_thickness,
                                          1000)
    hull_cylinder_bigger.rotate(
        Base.Vector(0, 0, 0),
        Base.Vector(0, 0, 1), 90)
    hull_cylinder_bigger.translate(Base.Vector(vaka_x_offset, 0, bottom_height))

    # hackish way to make chain plates:
    # intersect the mount with an enlarged hull, extrude it outwards,
    # take the outer wire and extrude it into the hull
    rudder_vaka_mount_a_backing_plate = side.newObject("Part::Feature", "Rudder_Vaka_Mount_a_backing_plate (aluminum)")
    rudder_vaka_mount_a_backing_plate_shape = rudder_vaka_mount_a.Shape.common(hull_cylinder_bigger)
    rudder_vaka_mount_a_center = rudder_vaka_mount_a_backing_plate_shape.BoundBox.Center
    rudder_vaka_mount_a_matrix = Base.Matrix()
    rudder_vaka_mount_a_matrix.move(Base.Vector(-rudder_vaka_mount_a_center.x, -rudder_vaka_mount_a_center.y, -rudder_vaka_mount_a_center.z))
    rudder_vaka_mount_a_matrix.scale(1.0, 2.0, 2.0)  # scale in y and z direction
    rudder_vaka_mount_a_matrix.move(Base.Vector(rudder_vaka_mount_a_center.x, rudder_vaka_mount_a_center.y, rudder_vaka_mount_a_center.z))
    rudder_vaka_mount_a_backing_plate_shape = rudder_vaka_mount_a_backing_plate_shape.transformGeometry(rudder_vaka_mount_a_matrix)
    rudder_vaka_mount_a_wires = rudder_vaka_mount_a_backing_plate_shape.Wires
    rudder_vaka_mount_a_outer_wire = max(rudder_vaka_mount_a_wires, key=lambda w: w.BoundBox.DiagonalLength)
    rudder_vaka_mount_a_face = Part.Face(rudder_vaka_mount_a_outer_wire)
    rudder_vaka_mount_a_backing_plate_shape = rudder_vaka_mount_a_face.extrude(Base.Vector(
        rudder_vaka_backing_plate_thickness * 2 + vaka_thickness,
        0, 0))
    rudder_vaka_mount_a_backing_plate.Shape = rudder_vaka_mount_a_backing_plate_shape
    
    # rudder vaka mount B: outer brace
    
    rudder_vaka_mount_b = side.newObject("Part::Feature", "Rudder_Vaka_Mount_b (aluminum)")
    rudder_vaka_mount_b_shape = shs(spine_width, spine_thickness, rudder_vaka_mount_length)
    # rotate shape around x axis first
    rudder_vaka_mount_b_shape.rotate(
        Base.Vector(0, 0, 0),
        Base.Vector(1, 0, 0),
        90)
    # then translate so that the origin aligns with the center where the pole goes
    rudder_vaka_mount_b_shape.translate(Base.Vector(-spine_width / 2, spine_width / 2, 0))
    # then rotate in y axis around origin
    rudder_vaka_mount_b_shape.rotate(
        Base.Vector(0, 0, 0),
        Base.Vector(0, 0, 1),
        45 - rudder_vaka_mount_angle)
    # translate to the correct position (somehow, ".Placement = ..." not working here)
    rudder_vaka_mount_b_shape.translate(Base.Vector(vaka_x_offset
                    - vaka_width / 2
                    - rudder_distance_from_vaka,
                    cockpit_length / 2
                    + (panels_longitudinal / 2 - 1) * panel_width
                    + aka_width / 2,
                    rudder_vaka_mount_base_level))
    rudder_vaka_mount_b_shape = rudder_vaka_mount_b_shape.cut(hull_cylinder)
    rudder_vaka_mount_b.Shape = rudder_vaka_mount_b_shape
    set_color(rudder_vaka_mount_b, color_aluminum)

    # hackish way to make chain plates:
    # intersect the mount with an enlarged hull, extrude it outwards,
    # take the outer wire and extrude it into the hull
    rudder_vaka_mount_b_backing_plate = side.newObject("Part::Feature", "rudder_vaka_mount_b_backing_plate (aluminum)")
    rudder_vaka_mount_b_backing_plate_shape = rudder_vaka_mount_b.Shape.common(hull_cylinder_bigger)
    rudder_vaka_mount_b_center = rudder_vaka_mount_b_backing_plate_shape.BoundBox.Center
    rudder_vaka_mount_b_matrix = Base.Matrix()
    rudder_vaka_mount_b_matrix.move(Base.Vector(-rudder_vaka_mount_b_center.x, -rudder_vaka_mount_b_center.y, -rudder_vaka_mount_b_center.z))
    rudder_vaka_mount_b_matrix.scale(1.0, 2.0, 2.0)  # scale in y and z direction
    rudder_vaka_mount_b_matrix.move(Base.Vector(rudder_vaka_mount_b_center.x, rudder_vaka_mount_b_center.y, rudder_vaka_mount_b_center.z))
    rudder_vaka_mount_b_backing_plate_shape = rudder_vaka_mount_b_backing_plate_shape.transformGeometry(rudder_vaka_mount_b_matrix)
    rudder_vaka_mount_b_wires = rudder_vaka_mount_b_backing_plate_shape.Wires
    rudder_vaka_mount_b_outer_wire = max(rudder_vaka_mount_b_wires, key=lambda w: w.BoundBox.DiagonalLength)
    rudder_vaka_mount_b_face = Part.Face(rudder_vaka_mount_b_outer_wire)
    rudder_vaka_mount_b_backing_plate_shape = rudder_vaka_mount_b_face.extrude(Base.Vector(
        rudder_vaka_backing_plate_thickness * 2 + vaka_thickness,
        0, 0))
    rudder_vaka_mount_b_backing_plate.Shape = rudder_vaka_mount_b_backing_plate_shape
    
    # crossdeck
    
    crossdeck = side.newObject("Part::Feature", "Crossdeck (plywood)")
    crossdeck.Shape = Part.makeBox(crossdeck_length,
                                 crossdeck_width / 2,
                                 crossdeck_thickness)
    crossdeck.Placement = FreeCAD.Placement(
        Base.Vector(- aka_width / 2,
                    0,
                    deck_base_level),
        FreeCAD.Rotation(Base.Vector(0, 0, 0), 0))
    set_color(crossdeck, color_deck)

    # trap cover

    trap_cover = side.newObject("Part::Feature", "Trap Cover (plywood)")
    trap_cover.Shape = Part.makeBox(crossdeck_length - panels_transversal * panel_length,
                                    panel_width - crossdeck_width / 2 - aka_width / 2,
                                    crossdeck_thickness)
    trap_cover.Placement = FreeCAD.Placement(
        Base.Vector(- aka_width / 2 + panels_transversal * panel_length,
                    crossdeck_width / 2,
                    deck_base_level),
        FreeCAD.Rotation(Base.Vector(0, 0, 0), 0))
    set_color(trap_cover, color_deck)

    # ama: upper and lower for color effect
    
    large = 1000000
    ama_cutter = Part.makeBox(large, large, large,
                          Base.Vector(-large/2, 0, -large/2))

    ama_body_upper = side.newObject("Part::Feature", "Ama pipe upper (pvc)")
    ama_body_upper.Shape = pipe(ama_diameter, ama_thickness,
                          ama_length / 2 - ama_cone_length)
    ama_body_upper.Shape = ama_body_upper.Shape.common(ama_cutter)
    ama_body_upper.Placement = FreeCAD.Placement(
        Base.Vector(0, ama_length / 2 - ama_cone_length, ama_diameter / 2),
        FreeCAD.Rotation(Base.Vector(1, 0, 0), 90))
    set_color(ama_body_upper, color_ama)

    ama_body_lower = side.newObject("Part::Feature", "Ama pipe lower (pvc)")
    ama_body_lower.Shape = pipe(ama_diameter, ama_thickness,
                          ama_length / 2 - ama_cone_length)
    ama_body_lower.Shape = ama_body_lower.Shape.cut(ama_cutter)
    ama_body_lower.Placement = FreeCAD.Placement(
        Base.Vector(0, ama_length / 2 - ama_cone_length, ama_diameter / 2),
        FreeCAD.Rotation(Base.Vector(1, 0, 0), 90))
    set_color(ama_body_lower, color_bottom)

    ama_body_foam = side.newObject("Part::Feature", "Ama_Body_Foam (foam)")
    ama_body_foam.Shape = Part.makeCylinder(ama_diameter / 2 - ama_thickness, ama_length / 2 - ama_cone_length)
    ama_body_foam.Placement = FreeCAD.Placement(
        Base.Vector(0, ama_length / 2 - ama_cone_length, ama_diameter / 2),
        FreeCAD.Rotation(Base.Vector(1, 0, 0), 90))
        
    ama_cone_upper = side.newObject("Part::Feature", "Ama_Cone_Upper (pvc)")
    ama_cone_upper.Shape = hollow_cone(ama_diameter,
                                       ama_thickness,
                                       ama_cone_length)
    ama_cone_upper.Shape = ama_cone_upper.Shape.cut(ama_cutter)
    ama_cone_upper.Placement = FreeCAD.Placement(
        Base.Vector(0, ama_length / 2 - ama_cone_length, ama_diameter / 2),
        FreeCAD.Rotation(Base.Vector(1, 0, 0), 270))
    set_color(ama_cone_upper, color_ama)

    ama_cone_lower = side.newObject("Part::Feature", "Ama_Cone_Lower (pvc)")
    ama_cone_lower.Shape = hollow_cone(ama_diameter,
                                       ama_thickness,
                                       ama_cone_length)
    ama_cone_lower.Shape = ama_cone_lower.Shape.common(ama_cutter)
    ama_cone_lower.Placement = FreeCAD.Placement(
        Base.Vector(0, ama_length / 2 - ama_cone_length, ama_diameter / 2),
        FreeCAD.Rotation(Base.Vector(1, 0, 0), 270))
    set_color(ama_cone_lower, color_bottom)

    ama_cone_foam = side.newObject("Part::Feature", "Ama_Cone_Foam (foam)")
    ama_cone_foam.Shape = Part.makeCone(ama_diameter / 2 - ama_thickness, 0, ama_thickness)
    ama_cone_foam.Placement = FreeCAD.Placement(
        Base.Vector(0, ama_length / 2 - ama_cone_length, ama_diameter / 2),
        FreeCAD.Rotation(Base.Vector(1, 0, 0), 270))
        
