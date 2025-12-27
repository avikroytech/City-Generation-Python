# City Generation Python

A procedural city generator that creates realistic urban layouts with residential, commercial, and industrial zones connected by roads and populated with buildings.

## Features

- **Procedural Grid Generation**: Creates a customizable grid-based city map
- **Zone Distribution**: Automatically generates residential, commercial, and industrial zones with random sizing
- **Road Generation**: Intelligently creates roads between different zones
- **Shape Detection**: Identifies connected regions of the same zone type
- **Building Placement**: Places various building sizes within zones to populate the city

## Project Structure

- [`road_generator.py`](road_generator.py) - Main city generation engine
- [`test.py`](test.py) - Testing and debugging utilities for shape detection
- `__pycache__/` - Python cache directory

## How It Works

### 1. Grid Initialization
The generator creates an empty grid and populates it with zones:
- **Residential** (40% probability) - Green zones
- **Commercial** (30% probability) - Blue zones  
- **Industrial** (5% probability) - Red zones

### 2. Road Generation
Roads are automatically created at boundaries between different zones to connect them.

### 3. Shape Detection
The `find_shape()` method traces connected regions of the same zone type, building a 2D map of each district.

### 4. Building Placement
Various building sizes are randomly placed within each zone:
- 1x1 buildings
- 1x2 buildings
- 1x3 buildings
- 2x2 buildings

Buildings can rotate to fit the available space in each zone.

## Usage

```python
from road_generator import CityGenerator

# Create a 30x30 city
city_generator = CityGenerator(30)
city_generator.generate_empty_grid()
city_map = city_generator.populate_grid()

# Display the city
city_generator.print_map(city_map)

# Detect zones and place buildings
sections = city_generator.detect_shapes()
city_generator.place_buildings_in_map(buildings, sections)

# Show final city with buildings
city_generator.print_colored_id(city_map)
```

## Display Colors

- 🟢 **Green** - Residential zones
- 🔵 **Blue** - Commercial zones
- 🔴 **Red** - Industrial zones
- ⬜ **Light Grey** - Roads
- 1 **Various Numbers** - Building IDs

## Dependencies

- `termcolor` - For colored terminal output
- `colorama` - For cross-platform color support
- Python 3.x

Install dependencies with:
```bash
pip install termcolor colorama
```

## Classes

- **`Cell`** - Individual grid cell with position, type, and building ID
- **`Building`** - Represents a building structure with rotations
- **`CityGenerator`** - Main class for generating and managing the city

## Notes

- Grid size should be even numbers for optimal zone generation
- The algorithm uses a random shuffle for varied results
- Building placement prioritizes fitting buildings to available space