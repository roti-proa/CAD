# Makefile for Solar Proa FreeCAD project

# Detect operating system
UNAME := $(shell uname)

# Detect FreeCAD command (different on different systems)
FREECAD_APP := /Applications/FreeCAD.app/Contents/MacOS/FreeCAD
FREECAD := $(shell which freecad 2>/dev/null || \
                   which freecadcmd 2>/dev/null || \
                   (test -f $(FREECAD_APP) && echo $(FREECAD_APP)) || \
                   echo "freecad")

# On macOS use GUI app, on Linux use headless
ifeq ($(UNAME),Darwin)
	FREECAD_CMD := $(FREECAD_APP) --console
else
	FREECAD_CMD := xvfb-run -a freecadcmd
endif

# Directories
SRC_DIR := src
DESIGN_DIR := output_designs
RENDER_DIR := output_renders
EXPORT_DIR := output_exports
DOCS_DIR := docs

# Discover all boats and configurations dynamically
BOATS := $(basename $(notdir $(wildcard $(SRC_DIR)/boats/*.py)))
CONFIGS := $(basename $(notdir $(wildcard $(SRC_DIR)/configurations/*.py)))

# Filter out __pycache__ and backup files
BOATS := $(filter-out __pycache__,$(BOATS))
CONFIGS := $(filter-out __pycache__ default,$(CONFIGS))

# Which boat to build (RP2 or RP3)
BOAT ?= RP2
PARAMS := boats.$(BOAT)

# What configuration to use (CloseHaul etc)
CONFIG ?= CloseHaul
CONFIG_PARAM := configurations.$(CONFIG)

DESIGN_NAME := SolarProa_$(BOAT)_$(CONFIG)

# Main macro
MACRO := $(SRC_DIR)/SolarProa.FCMacro

# Design files
FCSTD := $(DESIGN_DIR)/$(DESIGN_NAME).FCStd
STEP := $(EXPORT_DIR)/$(DESIGN_NAME).step

# Default target - build all boats with all configurations
.PHONY: all
all:
	@echo "Building all boats with all configurations..."
	@echo "Boats: $(BOATS)"
	@echo "Configs: $(CONFIGS)"
	@$(foreach boat,$(BOATS),$(foreach config,$(CONFIGS),$(MAKE) build BOAT=$(boat) CONFIG=$(config);))
	@echo "All builds complete!"

# Create output directories
$(DESIGN_DIR) $(RENDER_DIR) $(EXPORT_DIR):
	mkdir -p $@

.PHONY: build
build: $(DESIGN_DIR)
	@echo "Building $(BOAT) with $(CONFIG) configuration..."
	@$(FREECAD_CMD) $(MACRO) $(PARAMS) $(CONFIG_PARAM) || true
	@if [ -f "$(FCSTD)" ]; then \
		echo "FCStd file created: $(FCSTD)"; \
		if [ "$(UNAME)" = "Darwin" ]; then \
			echo "Running fix_visibility.sh on macOS..."; \
			$(SRC_DIR)/fix_visibility.sh "$(FCSTD)" "$(FREECAD_APP)"; \
		fi; \
		echo "Build complete!"; \
	else \
		echo "ERROR: Build failed - no design file created"; \
		exit 1; \
	fi

# Export to various formats (requires adding export commands to macro)
.PHONY: export
export: build $(EXPORT_DIR)
	@echo "Exporting model..."
# Add export commands here once you modify the macro
	@echo "Export complete!"

# Render images from FCStd files
.PHONY: render
render: build $(RENDER_DIR)
	@echo "Rendering images from $(FCSTD)..."
	@if [ "$(UNAME)" = "Darwin" ]; then \
		$(SRC_DIR)/export_renders_mac.sh "$(FCSTD)" "$(RENDER_DIR)" "$(FREECAD_APP)"; \
	else \
		$(FREECAD_CMD) $(SRC_DIR)/export_renders.py "$(FCSTD)" "$(RENDER_DIR)"; \
	fi
	@echo "Render complete!"

# Render all generated FCStd files
# Generate YAML stats files for Jekyll
.PHONY: stats-yaml
stats-yaml: $(DESIGN_DIR)
	@echo "Generating YAML statistics for Jekyll..."
	@mkdir -p $(DOCS_DIR)/_data
	@for fcstd in $(DESIGN_DIR)/*.FCStd; do \
		if [ -f "$$fcstd" ]; then \
			base=$$(basename "$$fcstd" .FCStd); \
			yaml_name=$$(echo "$$base" | tr '[:upper:]' '[:lower:]' | sed 's/solarproa_//'); \
			echo "Generating stats for $$base..."; \
			if [ "$(UNAME)" = "Darwin" ]; then \
				PYTHONPATH=/Applications/FreeCAD.app/Contents/Resources/lib:/Applications/FreeCAD.app/Contents/Resources/Mod \
				DYLD_LIBRARY_PATH=/Applications/FreeCAD.app/Contents/Frameworks:/Applications/FreeCAD.app/Contents/Resources/lib \
				/Applications/FreeCAD.app/Contents/Resources/bin/python $(SRC_DIR)/generate_stats_yaml.py "$$fcstd" $(DOCS_DIR)/"_data/$${yaml_name}.yml" || true; \
			else \
				FCSTD_FILE="$$fcstd" OUTPUT_YAML=$(DOCS_DIR)/"_data/$${yaml_name}.yml" freecad-python $(SRC_DIR)/generate_stats_yaml.py || true; \
			fi \
		fi \
	done
	@echo "Stats YAML generation complete!"

.PHONY: render-all
render-all: $(RENDER_DIR)
	@echo "Rendering images from all FCStd files..."
	@for fcstd in $(DESIGN_DIR)/*.FCStd; do \
		if [ -f "$$fcstd" ]; then \
			echo "Rendering $$fcstd..."; \
			if [ "$(UNAME)" = "Darwin" ]; then \
				$(SRC_DIR)/export_renders_mac.sh "$$fcstd" "$(RENDER_DIR)" "$(FREECAD_APP)" || true; \
			else \
				FCSTD_FILE="$$fcstd" DESIGN_DIR="$(RENDER_DIR)" freecad-python $(SRC_DIR)/export_renders.py || true; \
			fi \
		fi \
	done
	@echo "All renders complete!"
	@echo "Cropping images with ImageMagick..."
	@if command -v convert >/dev/null 2>&1; then \
		for img in $(RENDER_DIR)/*.png; do \
			if [ -f "$$img" ]; then \
				echo "Cropping $$img..."; \
				convert "$$img" -fuzz 1% -trim +repage -bordercolor white -border 20 "$$img" || true; \
			fi \
		done; \
		echo "Cropping complete!"; \
	else \
		echo "ImageMagick not found, skipping crop"; \
	fi

# Clean generated files
.PHONY: clean
clean:
	@echo "Cleaning design files..."
	rm -rf $(DESIGN_DIR)
	@echo "Cleaning render files..."
	rm -rf $(RENDER_DIR)
	@echo "Cleaning export files..."
	rm -rf $(EXPORT_DIR)
	@echo "Cleaning data files..."
	rm -rf $(DOCS_DIR)/_data
	@echo "Cleaning jekyll site files..."
	rm -rf $(DOCS_DIR)/_site
	@echo "Removing backup files..."
	find . -name '*~' -delete
	@echo "Removing Python cache..."
	find . -type d -name '__pycache__' -exec rm -rf {} + 2>/dev/null || true
	find . -name '*.pyc' -delete
	find . -name '*.pyo' -delete
	@echo "Clean complete!"

# Build specific boats with all configurations
.PHONY: rp2 rp3
rp2:
	@$(foreach config,$(CONFIGS),$(MAKE) build BOAT=RP2 CONFIG=$(config);)

rp3:
	@$(foreach config,$(CONFIGS),$(MAKE) build BOAT=RP3 CONFIG=$(config);)

# Build all boats (all configurations)
.PHONY: both boats
both boats: all

# Build specific configuration with all boats
.PHONY: closehaul beamreach broadreach goosewing
closehaul:
	@$(foreach boat,$(BOATS),$(MAKE) build BOAT=$(boat) CONFIG=CloseHaul;)

beamreach:
	@$(foreach boat,$(BOATS),$(MAKE) build BOAT=$(boat) CONFIG=BeamReach;)

broadreach:
	@$(foreach boat,$(BOATS),$(MAKE) build BOAT=$(boat) CONFIG=BroadReach;)

goosewing:
	@$(foreach boat,$(BOATS),$(MAKE) build BOAT=$(boat) CONFIG=GooseWing;)

# Show statistics
.PHONY: stats
stats: build
	@echo "Model statistics:"
	@python3 $(SRC_DIR)/stats.py 2>/dev/null || echo "Run build first"

# Help
.PHONY: help
help:
	@echo "Solar Proa Makefile"
	@echo ""
	@echo "Platform: $(UNAME)"
	@echo "Discovered boats: $(BOATS)"
	@echo "Discovered configurations: $(CONFIGS)"
	@echo ""
	@echo "Main targets:"
	@echo "  make             - Build ALL boats with ALL configurations"
	@echo "  make all         - Same as above"
	@echo "  make build       - Build single boat+config (BOAT=$(BOAT) CONFIG=$(CONFIG))"
	@echo "  make render      - Export render images from current build"
	@echo "  make render-all  - Export render images from ALL FCStd files"
	@echo ""
	@echo "Boat-specific targets:"
	@echo "  make rp2         - Build RP2 with all configurations"
	@echo "  make rp3         - Build RP3 with all configurations"
	@echo ""
	@echo "Configuration-specific targets:"
	@echo "  make closehaul   - Build all boats in CloseHaul configuration"
	@echo "  make beamreach   - Build all boats in BeamReach configuration"
	@echo "  make broadreach  - Build all boats in BroadReach configuration"
	@echo "  make goosewing   - Build all boats in GooseWing configuration"
	@echo ""
	@echo "Utility targets:"
	@echo "  make clean       - Remove all generated files"
	@echo "  make stats       - Show model statistics"
	@echo "  make check       - Check FreeCAD installation"
	@echo "  make help        - Show this help message"
	@echo ""
	@echo "Examples:"
	@echo "  make build BOAT=RP2 CONFIG=BeamReach"
	@echo "  make rp2"
	@echo "  make closehaul"
	@echo ""
	@echo "FreeCAD: $(FREECAD)"

# Check if FreeCAD is installed
.PHONY: check
check:
	@echo "Checking for FreeCAD..."
	@$(FREECAD) --version || (echo "FreeCAD not found!" && exit 1)
	@echo "FreeCAD found: $(FREECAD)"

# Serve website locally
.PHONY: localhost
localhost:
	@echo "Serving website in localhost..."
	cd docs; bundle exec jekyll serve

# Make zip file with just the git files
.PHONY: zip
zip: 
	@echo "Make zip file with just the git files"
	git archive -o ../CAD-clean.zip HEAD



