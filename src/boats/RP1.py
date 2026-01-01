# number of solar panels
panels_longitudinal = 2
panels_transversal =  1

# number of deck stringers
deck_stringers = 2

# parameters; all in mm

mm_in_one_inch = 25.4

panel_length = 1762
panel_width = 1134
panel_height = 30

deck_width = 1000
deck_thickness = 9

ama_diameter = 200
ama_thickness = 10
ama_length = 4000

stringer_width = 25
stringer_thickness = 3

aka_width = 50.8
aka_height = 76.2
aka_thickness = 4.5
aka_length = panel_length * panels_transversal + deck_width

aka_cap_thickness = 5
aka_cap_diameter = 80

vaka_length = 4200
vaka_width = 500
vaka_thickness = 5

overhead_thickness = 3
sole_thickness = 7
bottom_height = 10
bottom_thickness = vaka_thickness

crossdeck_width = 650
crossdeck_thickness = deck_thickness
crossdeck_length = (panels_transversal * panel_length +
                  (deck_width - vaka_width) / 2 +
                  stringer_width)

cockpit_length = panel_width + crossdeck_width - aka_width


panel_stringer_offset = panel_length / 4 - stringer_width / 2
panel_stringer_length = crossdeck_width + panels_longitudinal * panel_width

gunwale_width = 3 * mm_in_one_inch
gunwale_height = 2 * mm_in_one_inch
freeboard = 600 - gunwale_height
gunwale_base_level = bottom_height + freeboard
overhead_base_level = gunwale_base_level + gunwale_height
aka_base_level = overhead_base_level + overhead_thickness
stringer_base_level = aka_base_level + aka_height
panel_base_level = stringer_base_level + stringer_width
deck_base_level = panel_base_level
deck_level = deck_base_level + deck_thickness

stanchion_diameter = 20
stanchion_length = 600
stanchion_thickness = 3

# in this design, spine and pillars are all made
# from the same SHS sizes

spine_thickness = aka_thickness
spine_width = aka_width
spine_base_level = aka_base_level - spine_width
spine_length = panel_width * panels_longitudinal + crossdeck_width

beam = aka_length + aka_cap_thickness - spine_width + ama_diameter / 2

pillar_thickness = aka_thickness
pillar_width = aka_width
pillar_height = spine_base_level - ama_thickness

# cone starts at outer edge of outermost pillar
ama_cone_length = (ama_length -
                   (panel_width * (panels_longitudinal - 1) +
                    pillar_width + crossdeck_width)) / 2

# Cross-bracing between pillars (X-shaped reinforcements)
brace_diameter = 5  # thin aluminum rod/wire
brace_upper_offset = 100  # distance from spine to upper corners of X
brace_lower_offset = 400  # distance from ama to lower corners of X

# Pillar-to-aka diagonal braces (triangulation)
pillar_brace_vertical_offset = 500  # vertical distance down pillar from aka base level

# distance from x=0 (center line of ama) to center line of vaka
vaka_displacement = (- pillar_width / 2
                     + panel_length * panels_transversal
                     + deck_width / 2)

mast_diameter = 80
mast_thickness = 5
mast_height = 5000
mast_distance_from_center = vaka_length / 4 + 0
# adjustment to not cut into aka
mast_base_level = bottom_height + sole_thickness

mast_partner_length = vaka_width - 110
mast_partner_width = mast_diameter + 200
mast_partner_thickness = 50

mast_step_outer_diameter = mast_diameter + 100
mast_step_inner_diameter = mast_diameter
mast_step_height = 100

mast_handle_diameter = 25
mast_handle_thickness = 3
mast_handle_length = 600
mast_handle_height_above_deck = 600

mast_cap_thickness = 3
mast_cap_diameter = 100

yard_spar_length = 500
yard_spar_width = 50
yard_spar_thickness = 10
yard_spar_distance_from_top = 500
yard_spar_height = mast_height - yard_spar_distance_from_top

# Sail parameters (tanja sail)
yard_diameter = 25
yard_thickness = 2.8
yard_length = 3000

boom_diameter = yard_diameter
boom_thickness = yard_thickness
boom_length = yard_length

sail_height = 3000  # vertical distance between yard and boom
sail_width  = yard_length
sail_thickness = 2  # thin membrane

# rudder

rudder_post_diameter = 50
rudder_head_length = 200
rudder_blade_length = 400
rudder_blade_height = 400
rudder_distance_from_vaka = 100
rudder_below_bottom = 400

