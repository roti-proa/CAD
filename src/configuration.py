import sys
import os

# FreeCAD puts its own arguments first, macro arguments come after the macro filename
# Find where the macro name is and take arguments after that
macro_args = []
for i, arg in enumerate(sys.argv):
    if arg.endswith('.FCMacro'):
        macro_args = sys.argv[i+1:]
        break

print(f"DEBUG: sys.argv = {sys.argv}")
print(f"DEBUG: macro_args = {macro_args}")

# Get parameter file from command line, default to default
configuration_file = macro_args[1] if macro_args else 'configurations.default'

print(f"DEBUG: param_file = {configuration_file}")

# Import the specified parameters
if configuration_file in sys.modules:
    del sys.modules[param_file]

# Create an alias so other modules can import 'parameters'
import importlib
try:
    configuration_module = importlib.import_module(configuration_file)
    sys.modules['configuration'] = configuration_module
    print(f"DEBUG: Successfully imported {configuration_file}")
except Exception as e:
    print(f"ERROR importing {configuration_file}: {e}")
    raise

# Now import into global namespace
exec(f"from {configuration_file} import *")

