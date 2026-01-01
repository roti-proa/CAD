# Colors (RGB values from 0.0 to 1.0)
color_deck = (0.68, 0.85, 0.90)  # light blue
color_solar_panel = (0.3, 0.3, 0.3)  # dark grey
color_aluminum = (0.75, 0.75, 0.78)  # aluminum
color_hull_interior = (0.5, 0.5, 0.5)  # grey
color_hull_exterior = (1.0, 1.0, 1.0)  # white
color_bottom = (0.9, 0.1, 0.1)  # spinnaker red
color_sole = (0.76, 0.60, 0.42)  # light brown (plywood)
color_plywood = (0.76, 0.60, 0.42)  # light brown (plywood)
color_bamboo = (0.86, 0.70, 0.52)  # light brown (bamboo)
color_sail = (0.95, 0.95, 0.88)  # off-white/cream for sail
color_ama = (1.0, 1.0, 1.0)  # white

# TODO: update all shapes so that the material is included in the
# shape name; then the following colors will be used
material_colors = {
    'Plywood': (0.76, 0.60, 0.42),
    'Bamboo': (0.86, 0.70, 0.52),
    'Aluminum': (0.75, 0.75, 0.78),
    'PVC': (1.0, 1.0, 1.0)
}

def set_color(obj, color):
    """Set color on a FreeCAD object"""
    if hasattr(obj, 'ViewObject') and obj.ViewObject:
        obj.ViewObject.ShapeColor = color
