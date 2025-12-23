import Part
from FreeCAD import Base
import math

from parameters import *

# maker functions for common shapes

# SHS: square hollow section: pipe with square profile

def shs(outer, wall, length):
    # Create outer square
    outer_square = Part.makePolygon([
        Base.Vector(0, 0, 0),
        Base.Vector(outer, 0, 0),
        Base.Vector(outer, outer, 0),
        Base.Vector(0, outer, 0),
        Base.Vector(0, 0, 0)
    ])

    # Create inner square (offset inward)
    inner = outer - 2*wall
    offset = wall
    inner_square = Part.makePolygon([
        Base.Vector(offset, offset, 0),
        Base.Vector(outer-offset, offset, 0),
        Base.Vector(outer-offset, outer-offset, 0),
        Base.Vector(offset, outer-offset, 0),
        Base.Vector(offset, offset, 0)
    ])

    # Create faces and extrude
    outer_face = Part.Face(outer_square)
    inner_face = Part.Face(inner_square)
    profile = outer_face.cut(inner_face)
    shs = profile.extrude(Base.Vector(0, 0, length))
    return shs

# SHS: square hollow section: pipe with square profile

def shs_capped(outer, wall, length, cap_diameter, cap_thickness):
    # Create outer square
    outer_square = Part.makePolygon([
        Base.Vector(0, 0, 0),
        Base.Vector(outer, 0, 0),
        Base.Vector(outer, outer, 0),
        Base.Vector(0, outer, 0),
        Base.Vector(0, 0, 0)
    ])

    # Create inner square (offset inward)
    inner = outer - 2*wall
    offset = wall
    inner_square = Part.makePolygon([
        Base.Vector(offset, offset, 0),
        Base.Vector(outer-offset, offset, 0),
        Base.Vector(outer-offset, outer-offset, 0),
        Base.Vector(offset, outer-offset, 0),
        Base.Vector(offset, offset, 0)
    ])

    # Create faces and extrude
    outer_face = Part.Face(outer_square)
    inner_face = Part.Face(inner_square)
    profile = outer_face.cut(inner_face)
    shs = profile.extrude(Base.Vector(0, 0, length))

    cap_radius = cap_diameter / 2
    cap1 = Part.makeCylinder(cap_radius, cap_thickness)
    cap1.translate(Base.Vector(outer/2, outer/2, - cap_thickness))
    cap2 = Part.makeCylinder(cap_radius, cap_thickness)
    cap2.translate(Base.Vector(outer/2, outer/2, length))
    
    return shs.fuse(cap1).fuse(cap2)

# circular pipe

def pipe(diameter, thickness, length):
    """Create a hollow cylinder (pipe)"""
    outer_radius = diameter / 2
    inner_radius = outer_radius - thickness
    
    # Create outer cylinder
    outer_cylinder = Part.makeCylinder(outer_radius, length)
    
    # Create inner cylinder (to subtract)
    inner_cylinder = Part.makeCylinder(inner_radius, length)
    
    # Subtract to make hollow
    pipe = outer_cylinder.cut(inner_cylinder)
    
    return pipe

# circular cone

def hollow_cone(diameter, thickness, length):
    radius_outer = diameter / 2
    radius_inner = radius_outer - thickness
    outer_cone = Part.makeCone(radius_outer, 0, length)
    inner_length = length * radius_inner / radius_outer
    inner_cone = Part.makeCone(radius_inner, 0, inner_length)
    hollow_cone = outer_cone.cut(inner_cone)
    return hollow_cone

# solid elliptical cylinder

def elliptical_cylinder(major_diameter, minor_diameter, length):
    """Create an elliptical cylinder"""
    major_radius = major_diameter / 2
    minor_radius = minor_diameter / 2
    
    # Create ellipse
    ellipse = Part.Ellipse(
        Base.Vector(0, 0, 0),  # center
        major_radius,
        minor_radius)
    wire = Part.Wire(ellipse.toShape())
    face = Part.Face(wire)
    
    # Extrude along Z-axis
    elliptical_cylinder = face.extrude(Base.Vector(0, 0, length))
    
    return elliptical_cylinder

# hollow elliptical cylinder

def elliptical_pipe(major_diameter, minor_diameter, thickness, length):
    """Create a hollow elliptical cylinder"""
    major_radius_outer = major_diameter / 2
    minor_radius_outer = minor_diameter / 2
    major_radius_inner = major_radius_outer - thickness
    minor_radius_inner = minor_radius_outer - thickness
    
    # Create outer ellipse
    outer_ellipse = Part.Ellipse(
        Base.Vector(0, 0, 0),  # center
        major_radius_outer,
        minor_radius_outer)
    outer_wire = Part.Wire(outer_ellipse.toShape())
    outer_face = Part.Face(outer_wire)
    
    # Create inner ellipse
    inner_ellipse = Part.Ellipse(
        Base.Vector(0, 0, 0),  # center
        major_radius_inner,
        minor_radius_inner)
    inner_wire = Part.Wire(inner_ellipse.toShape())
    inner_face = Part.Face(inner_wire)
    
    # Subtract inner from outer to get hollow profile
    profile = outer_face.cut(inner_face)
    
    # Extrude along Z-axis
    elliptical_pipe = profile.extrude(Base.Vector(0, 0, length))
    
    return elliptical_pipe


# ellipsoid

def ellipsoid(x_diameter, y_diameter, z_diameter):
    """Create an ellipsoid (3D ellipse)"""
    # Create a sphere and then scale it to make an ellipsoid
    sphere = Part.makeSphere(1.0)
    
    # Scale to the desired dimensions
    # FreeCAD sphere has radius 1, so we scale to get the desired radii
    x_scale = x_diameter / 2
    y_scale = y_diameter / 2
    z_scale = z_diameter / 2
    
    # Create scaling matrix
    matrix = Base.Matrix()
    matrix.scale(Base.Vector(x_scale, y_scale, z_scale))
    
    # Apply scaling
    ellipsoid_shape = sphere.transformGeometry(matrix)
    
    return ellipsoid_shape
