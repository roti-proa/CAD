import FreeCAD
from parameters import *

from material import *

def calculate_weight(doc):
    """Calculate weight based on material names in object labels"""
    
    material_weights = {}  # {material_name: weight_kg}
    material_volumes = {}  # {material_name: weight_kg}
    processed_labels = set()  # Track which objects we've already counted
    
    def get_all_objects(obj_list):
        """Recursively get all objects including those in groups"""
        all_objs = []
        for obj in obj_list:
            all_objs.append(obj)
            # If it's a group/part, recurse into it
            if hasattr(obj, 'Group'):
                all_objs.extend(get_all_objects(obj.Group))
        return all_objs
    
    all_objects = get_all_objects(doc.Objects)
    print(f"Searching through {len(all_objects)} objects (including grouped)...")
    
    for obj in all_objects:
        if not hasattr(obj, 'Shape'):
            continue
        
        # Skip if we've already processed this object (by its unique label)
        if obj.Label in processed_labels:
            continue
        
        # Look for material name - FreeCAD replaces () with __
        label = obj.Label
        label_lower = label.lower()
        mat_key = None
        
        # FreeCAD converts blanks and parentheses to _
        if '__' in label_lower:
            parts = label_lower.split('__')
            if len(parts) >= 2:
                # Handle cases like "Deck__plywood_001" - extract just "plywood"
                mat_key = parts[1].rstrip('_0123456789').strip()
        
        if mat_key and mat_key in material:
            mat = material[mat_key]
            volume_m3 = obj.Shape.Volume / 1e9
            weight_kg = volume_m3 * mat['Density']
            
            if mat['Name'] not in material_weights:
                material_weights[mat['Name']] = 0
            material_weights[mat['Name']] += weight_kg
            
            if mat['Name'] not in material_volumes:
                material_volumes[mat['Name']] = 0
            material_volumes[mat['Name']] += volume_m3 * 1000 # liters
            
            processed_labels.add(obj.Label)
            print(f"{obj.Label}: {weight_kg:.3f} kg ({mat['Name']})")
            print(f"{obj.Label}: {volume_m3 * 1000:.3f} liters")
    
    print(f"\n{'='*60}")
    print(f"Weight by materials:\n")
    total_weight = 0
    for mat_name, weight_kg in material_weights.items():
        total_weight += weight_kg
        print(f"{mat_name}: {weight_kg:.2f} kg")
    
    print(f"\nTotal weight: {total_weight:.2f} kg")

    print(f"{'='*60}")

    print(f"Volume by materials:\n")
    total_volume = 0
    for mat_name, volume_liters in material_volumes.items():
        total_volume += volume_liters
        print(f"{mat_name}: {volume_liters:.2f} liters")
    
    print(f"\nTotal volume: {total_volume:.2f} kg")
    print(f"\nTotal displacement in salt water: {total_volume * 1.025:.2f} kg")

    print(f"{'='*60}")

    # Calculate unsinkable displacement (parts that won't fill with water)
    unsinkable_volume = 0  # in mm³

    for obj in FreeCAD.ActiveDocument.Objects:
        # Check if object name contains "__*_" pattern (sealed/watertight parts)
        if "__" in obj.Name and obj.Name.count("_") >= 3:  # matches __*_ pattern
            if hasattr(obj, 'Shape') and obj.Shape:
                unsinkable_volume += obj.Shape.Volume

    # Convert to liters or m³
    unsinkable_volume_liters = unsinkable_volume / 1e6  # mm³ to liters
    unsinkable_volume_m3 = unsinkable_volume / 1e9  # mm³ to m³

    # Calculate displacement in kg (1 liter fresh water = 1 kg, seawater ~1.025 kg)
    unsinkable_displacement_kg = unsinkable_volume_liters * 1.025  # seawater

    print(f"Unsinkable volume: {unsinkable_volume_m3:.3f} m^3 ({unsinkable_volume_liters:.1f} liters)")
    print(f"Unsinkable displacement in salt water: {unsinkable_displacement_kg:.1f} kg")

    print(f"{'='*60}")

    print(f"Useful measurements:\n")
    print(f"cockpit length: {cockpit_length} mm")
    print(f"ama cone length: {ama_cone_length} mm")
    print(f"beam: {beam} mm")
    print(f"deck stringer separation: {(deck_width - stringer_width) / (deck_stringers - 1) - stringer_width} mm")
    print(f"sole foam volume: {FreeCAD.ActiveDocument.getObject('Foam_Below_Sole__foam_').Shape.Volume / 1000000:.1f} liters")
    print(f"ama foam volume: {FreeCAD.ActiveDocument.getObject('Ama_Body_Foam__foam_').Shape.Volume / 1000000 * 2:.1f} liters")
    print(f"sole foam displacement in salt water: {FreeCAD.ActiveDocument.getObject('Foam_Below_Sole__foam_').Shape.Volume / 1000000 * 1.025:.1f} kg")
    print(f"ama foam displacement in salt water: {FreeCAD.ActiveDocument.getObject('Ama_Body_Foam__foam_').Shape.Volume / 1000000 * 1.025 * 2 + FreeCAD.ActiveDocument.getObject('Ama_Cone_Foam__foam_').Shape.Volume / 1000000 * 1.025 * 2:.1f} kg")
    print(f"{'='*60}\n")
    
    return total_weight


