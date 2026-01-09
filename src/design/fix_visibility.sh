#!/bin/bash
# Fix visibility in a FreeCAD file by opening and saving in GUI mode

if [ $# -lt 1 ]; then
    echo "Usage: $0 <file.FCStd>"
    exit 1
fi

FCSTD_FILE="$1"
FREECAD="${2:-/Applications/FreeCAD.app/Contents/MacOS/FreeCAD}"

# Create a temporary Python script
TEMP_SCRIPT=$(mktemp /tmp/freecad_fix_XXXXXX.py)

cat > "$TEMP_SCRIPT" << 'EOF'
import FreeCAD
import FreeCADGui
import sys
import os

filepath = sys.argv[-1]
print(f"Opening {filepath}...")

doc = FreeCAD.openDocument(filepath)

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
        except:
            pass
        # Recurse into groups
        if hasattr(obj, 'Group') and obj.Group:
            make_visible(obj.Group)

print("Setting visibility...")
make_visible(doc.Objects)

print("Saving...")
doc.save()

print("Done!")
FreeCAD.closeDocument(doc.Name)

# Force quit FreeCAD
os._exit(0)
EOF

# Run FreeCAD with the script (in background with timeout)
"$FREECAD" "$TEMP_SCRIPT" "$FCSTD_FILE" &
FREECAD_PID=$!

# Wait up to 10 seconds for it to finish
for i in {1..20}; do
    if ! kill -0 $FREECAD_PID 2>/dev/null; then
        break
    fi
    sleep 0.5
done

# Force kill if still running
if kill -0 $FREECAD_PID 2>/dev/null; then
    kill -9 $FREECAD_PID 2>/dev/null
fi

# Clean up
rm -f "$TEMP_SCRIPT"
