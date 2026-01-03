#!/usr/bin/env python3
"""
Export renders from FreeCAD files.
Usage: freecadcmd export_renders.py <input.FCStd> <output_dir>
"""

import sys
import os

# Check if we're running in FreeCAD
try:
    import FreeCAD as App
    import FreeCADGui as Gui
except ImportError:
    print("ERROR: This script must be run with freecadcmd or FreeCAD")
    sys.exit(1)

def export_renders(fcstd_path, output_dir):
    """Export multiple views from an FCStd file as PNG images"""
    
    if not os.path.exists(fcstd_path):
        print(f"ERROR: File not found: {fcstd_path}")
        return False
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Import Qt for headless rendering
    from PySide import QtGui
    import platform
    
    # Initialize headless GUI (only on Linux)
    if platform.system() == 'Linux':
        try:
            QtGui.QApplication()
        except RuntimeError:
            pass
        
        Gui.showMainWindow()
        Gui.getMainWindow().destroy()
        App.ParamGet('User parameter:BaseApp/Preferences/Document').SetBool('SaveThumbnail', False)
    
    # Open the document
    print(f"Opening {fcstd_path}...")
    doc = App.openDocument(fcstd_path)
    
    # Get base name for output files
    base_name = os.path.splitext(os.path.basename(fcstd_path))[0]
    
    # Define views to export
    views = [
        ('Isometric', 'viewIsometric'),
        ('Front', 'viewFront'),
        ('Top', 'viewTop'),
        ('Right', 'viewRight'),
    ]
    
    # Get active view
    view = Gui.activeView()
    
    if not view:
        print("ERROR: No active view available")
        App.closeDocument(doc.Name)
        return False
    
    # Disable animation for faster rendering
    view.setAnimationEnabled(False)
    
    # Export each view
    for view_name, view_method in views:
        print(f"Exporting {view_name} view...")
        
        # Set the view
        getattr(view, view_method)()
        view.fitAll()
        
        # Export as PNG
        output_path = os.path.join(output_dir, f"{base_name}_{view_name}.png")
        view.saveImage(output_path, 1920, 1080, 'White')
        
        print(f"  Saved: {output_path}")
    
    # Close document
    App.closeDocument(doc.Name)
    
    print(f"Exported {len(views)} views from {fcstd_path}")
    return True

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: freecadcmd export_renders.py <input.FCStd> <output_dir>")
        sys.exit(1)
    
    fcstd_path = sys.argv[1]
    output_dir = sys.argv[2]
    
    success = export_renders(fcstd_path, output_dir)
    
    # Exit cleanly
    import os as _os
    _os._exit(0 if success else 1)
