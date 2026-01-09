#!/usr/bin/env python3
"""
Set object visibility in FreeCAD documents without GUI.
This can be called from design.FCMacro before saving.
"""

def set_all_visible(doc):
    """
    Set all objects visible except Origin helpers.
    Works in both GUI and console mode.
    
    Args:
        doc: FreeCAD document object
    """
    # Ensure FreeCADGui is imported (needed for ViewObject)
    try:
        import FreeCADGui
    except ImportError:
        print("Warning: FreeCADGui not available, cannot set visibility")
        return
    
    def make_visible(obj_list):
        """Recursively make all objects visible, except Origin helpers"""
        for obj in obj_list:
            try:
                if hasattr(obj, 'ViewObject') and obj.ViewObject:
                    # Hide Origin objects (coordinate system helpers)
                    if 'Origin' in obj.Name or obj.TypeId == 'App::Origin':
                        obj.ViewObject.Visibility = False
                    else:
                        obj.ViewObject.Visibility = True
                        # Set display mode to Shaded for better visibility
                        if hasattr(obj.ViewObject, 'DisplayMode'):
                            try:
                                obj.ViewObject.DisplayMode = "Shaded"
                            except:
                                pass  # Some objects don't support Shaded mode
            except Exception as e:
                # Some objects may not support visibility settings
                pass
            
            # Recurse into groups
            if hasattr(obj, 'Group') and obj.Group:
                make_visible(obj.Group)
    
    print("Setting object visibility...")
    make_visible(doc.Objects)
    print(f"✓ Visibility set for {len(doc.Objects)} objects")


def fix_visibility_in_file(filepath):
    """
    Open a FreeCAD file, set all objects visible, and save.
    This should be run with FreeCAD GUI (not --console mode).
    
    Args:
        filepath: Path to .FCStd file
    """
    import FreeCAD
    
    # Import FreeCADGui to ensure ViewObject is available
    try:
        import FreeCADGui
    except ImportError:
        print("Warning: FreeCADGui not available")
    
    print(f"Opening {filepath}...")
    doc = FreeCAD.openDocument(filepath)
    
    set_all_visible(doc)
    
    print("Saving...")
    doc.save()
    
    print("✓ Done!")
    FreeCAD.closeDocument(doc.Name)


if __name__ == "__main__":
    import sys
    
    # When run as a script from command line
    if len(sys.argv) >= 2:
        filepath = sys.argv[1]
    else:
        # When run by FreeCAD with the file as last argument
        filepath = sys.argv[-1] if len(sys.argv) > 1 else None
    
    if not filepath:
        print("Usage: FreeCAD visibility.py <file.FCStd>")
        sys.exit(1)
    
    fix_visibility_in_file(filepath)
    
    # Force quit FreeCAD (same as old fix_visibility_mac.sh)
    import os
    print("Done!")
    os._exit(0)
