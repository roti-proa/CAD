# all parts that are mirrored about the transversal axis

import FreeCAD
import Part
from FreeCAD import Base
import math

from parameters import *
from shapes import *
from material import *

def mirror(side):
    
    # akas (cross-beams) and pillars under each transversal row of panels

    for i in range(0, panels_longitudinal // 2):

        aka = side.newObject("Part::Feature", f"Aka_{i} (aluminum)")
        aka.Shape = shs_capped(aka_width, aka_thickness, aka_length,
                               aka_cap_diameter, aka_cap_thickness)
        aka.Placement = FreeCAD.Placement(
            Base.Vector(aka_length - pillar_width / 2,
                        panel_width * i + crossdeck_width / 2 +
                        panel_width / 2 - aka_width / 2,
                        aka_base_level),
            FreeCAD.Rotation(Base.Vector(0, -1, 0), 90))
        set_color(aka, color_aluminum)

        stanchion = side.newObject("Part::Feature",
                                   f"Stanchion_{i} (aluminum)")
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

    """
    # aka_rudder may be needed to provide rudder mount,
    # depending on panels_longitudinal and vaka_length

    aka_rudder = side.newObject("Part::Feature", f"Aka Rudder (aluminum)")
    aka_rudder.Shape = shs_capped(aka_width,
                                  aka_thickness,
                                  deck_width,
                                  aka_cap_diameter,
                                  aka_cap_thickness)
    aka_rudder.Placement = FreeCAD.Placement(
        Base.Vector(aka_length - pillar_width / 2,
                    panel_width * panels_longitudinal // 2 +
                    crossdeck_width / 2 +
                    panel_width / 2 - aka_width / 2,
                    aka_base_level),
        FreeCAD.Rotation(Base.Vector(0, -1, 0), 90))
    set_color(aka_rudder, color_aluminum)
    """

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
        Base.Vector(vaka_displacement
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
        Base.Vector(vaka_displacement,
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
        Base.Vector(vaka_displacement
                    - deck_width / 2 + aka_width / 2,
                    vaka_length / 2 - aka_width / 2,
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
            panel = side.newObject("Part::Feature", f"Panel_{i}_{j}")
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
                              vaka_length / 2 + aka_width / 2 - panel_width)
        deck_stringer.Placement = FreeCAD.Placement(
            Base.Vector(vaka_displacement - deck_width / 2 +
                        (deck_width - stringer_width) / (deck_stringers - 1) * i,
                        vaka_length / 2,
                        stringer_base_level),
            FreeCAD.Rotation(Base.Vector(1, 0, 0), 90))
        set_color(deck_stringer, color_aluminum)

    # trap cover stringer
    """
    trap_cover_stringer = side.newObject("Part::Feature", "Trap Cover Stringer (aluminum)")
    trap_cover_stringer.Shape = shs(stringer_width, stringer_thickness,
                                panel_width + aka_width / 2)
    trap_cover_stringer.Placement = FreeCAD.Placement(
        Base.Vector(crossdeck_length - spine_width / 2 - stringer_width,
                    0,
                    deck_base_level - spine_width / 4),
        FreeCAD.Rotation(Base.Vector(1, 0, 0), 90))
    set_color(trap_cover_stringer, color_aluminum)
    """
    
    # deck

    deck = side.newObject("Part::Feature", "Deck (plywood)")
    deck.Shape = Part.makeBox(deck_width,
                              vaka_length / 2 + aka_width / 2 - panel_width,
                              deck_thickness)
    deck.Placement = FreeCAD.Placement(
        Base.Vector(vaka_displacement - deck_width / 2,
                    cockpit_length / 2,
                    deck_base_level),
        FreeCAD.Rotation(Base.Vector(0, 0, 0), 0))
    set_color(deck, color_deck)

    # mast partner: reinforced deck collar supporting mast laterally 
    # this must be here, not in rig.py (it will rotate otherwise)
    mast_partner = side.newObject("Part::Feature", "Mast Partner (plywood)")
    mast_partner.Shape = Part.makeBox(
        mast_partner_length, mast_partner_width, mast_partner_thickness)
    mast_partner.Placement = FreeCAD.Placement(
        Base.Vector(vaka_displacement - mast_partner_length / 2,
                    mast_distance_from_center - mast_partner_width / 2,
                    freeboard + overhead_thickness),
        FreeCAD.Rotation(Base.Vector(0, 0, 0), 0))
    set_color(mast_partner, color_plywood)

    # mast step: reinforced sole collar supporting mast laterally 
    # this must be here, not in rig.py (it will rotate otherwise)
    mast_step = side.newObject("Part::Feature", "Mast Step (aluminum)")
    mast_step.Shape = pipe(
        mast_step_outer_diameter,
        mast_step_outer_diameter - mast_step_inner_diameter,
        mast_step_thickness)
    mast_step.Placement = FreeCAD.Placement(
        Base.Vector(vaka_displacement,
                    mast_distance_from_center,
                    sole_thickness),
        FreeCAD.Rotation(Base.Vector(0, 0, 0), 0))
    set_color(mast_step, color_aluminum)

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

    # ama
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
    set_color(ama_body_lower, color_sole)

    ama_cone_upper = side.newObject("Part::Feature", "Ama cone (pvc)")
    ama_cone_upper.Shape = hollow_cone(ama_diameter,
                                       ama_thickness,
                                       ama_cone_length)
    ama_cone_upper.Shape = ama_cone_upper.Shape.cut(ama_cutter)
    ama_cone_upper.Placement = FreeCAD.Placement(
        Base.Vector(0, ama_length / 2 - ama_cone_length, ama_diameter / 2),
        FreeCAD.Rotation(Base.Vector(1, 0, 0), 270))
    set_color(ama_cone_upper, color_ama)

    ama_cone_lower = side.newObject("Part::Feature", "Ama cone (pvc)")
    ama_cone_lower.Shape = hollow_cone(ama_diameter,
                                       ama_thickness,
                                       ama_cone_length)
    ama_cone_lower.Shape = ama_cone_lower.Shape.common(ama_cutter)
    ama_cone_lower.Placement = FreeCAD.Placement(
        Base.Vector(0, ama_length / 2 - ama_cone_length, ama_diameter / 2),
        FreeCAD.Rotation(Base.Vector(1, 0, 0), 270))
    set_color(ama_cone_lower, color_sole)

