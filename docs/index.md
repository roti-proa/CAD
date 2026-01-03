---
layout: default
title: Roti Proa Designs
---

# Roti Proa - Solar-Electric Proa Designs

A parametric design system for solar-electric proas, built with FreeCAD and Python.

## Design Variants

This site showcases automatically generated CAD models and renders for the Roti Proa project.

### Boats
- **RP1** - 4.2m prototype (tested May 2025)
- **RP2** - 9m day tourism vessel
- **RP3** - Future variant

### Configurations
- **Close Haul** - Upwind sailing
- **Beam Reach** - Cross-wind sailing
- **Broad Reach** - Downwind sailing
- **Goose Wing** - Running downwind
- **Beaching** - Beached configuration
- **Close Haul Reefed** - Reefed for heavy weather

## Latest Renders

*Renders are automatically generated from the CAD models on every commit.*

{% assign render_files = site.static_files | where_exp: "file", "file.path contains 'renders'" | where_exp: "file", "file.extname == '.png'" %}

{% if render_files.size > 0 %}
  {% for file in render_files %}
### {{ file.basename | replace: "_", " " }}
![{{ file.basename }}]({{ file.path }})
  {% endfor %}
{% else %}
  <p><em>No renders available yet. Renders will appear after the first successful build.</em></p>
{% endif %}

---

*This site is automatically built and deployed via GitHub Actions.*
