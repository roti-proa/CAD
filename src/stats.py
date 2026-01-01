from parameters import *

from material import *

def calculate_weight(doc):
    """Calculate weight based on material names in object labels"""
    
    material_weights = {}  # {material_name: weight_kg}
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
        
        # Try underscores format first (FreeCAD's conversion)
        if '__' in label_lower:
            parts = label_lower.split('__')
            if len(parts) >= 2:
                # Handle cases like "Deck__plywood_001" - extract just "plywood"
                mat_key = parts[1].rstrip('_0123456789').strip()
        
        # Fall back to parentheses format
        elif '(' in label_lower and ')' in label_lower:
            mat_key = label_lower.split('(')[1].split(')')[0].strip()
        
        if mat_key and mat_key in material:
            mat = material[mat_key]
            volume_m3 = obj.Shape.Volume / 1e9
            weight_kg = volume_m3 * mat['Density']
            
            if mat['Name'] not in material_weights:
                material_weights[mat['Name']] = 0
            material_weights[mat['Name']] += weight_kg
            
            processed_labels.add(obj.Label)
            print(f"{obj.Label}: {weight_kg:.3f} kg ({mat['Name']})")
    
    print(f"\n{'='*60}")
    total_weight = 0
    for mat_name, weight_kg in material_weights.items():
        total_weight += weight_kg
        print(f"{mat_name}: {weight_kg:.2f} kg")
    
    print(f"\nTotal weight: {total_weight:.2f} kg")
    print(f"{'='*60}\n")

    print(f"\nUseful measurements:")
    print(f"\ncockpit length: {cockpit_length} mm")
    print(f"ama cone length: {ama_cone_length} mm")
    print(f"beam: {beam} mm")
    print(f"{'='*60}\n")
    
    return total_weight


