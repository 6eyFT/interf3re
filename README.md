# Moiré Pattern Generator (V2)

This is a command-line interface (CLI) tool for generating 2D and 3D Moiré pattern animations in Python. The architecture is based on the principles of wave interference, superlattice generation, and computational physics, designed to be extensible for scientific, artistic, and industrial applications.

The tool operates on a modular, layer-based engine where fundamental 2D patterns are generated and then composed to create complex Moiré effects. The resulting 2D pattern is then extruded into a 3D point cloud and animated.

## Features

- **Modular Architecture:** Core logic is decoupled into separate modules for pattern generation, engine orchestration, and 3D rendering.
- **Dual Operation Modes:**
    - `artistic`: For creative expression, allowing the composition of multiple, arbitrary layers.
    - `scientific`: For physically-based simulations, starting with twisted hexagonal lattices ("Twistronics").
- **Extensible Pattern Library:** Currently supports generating line gratings and hexagonal lattices.
- **3D Animation:** Renders the final 2D pattern as a 3D point cloud and creates a rotating camera animation, saved as a GIF.

## Installation

The tool requires Python 3 and the following libraries. You can install them using pip:

```bash
pip install numpy matplotlib
```

## Usage

The application is run from the command line via `moire_cli.py`. All parameters are controlled with command-line flags.

### 1. General Help

To see all available commands and options, run:

```bash
python moire_cli.py --help
```

### 2. Artistic Mode Examples

The artistic mode builds a Moiré pattern by composing one or more `--layer` definitions.

**Example: Classic Rotated Line Pattern**

This creates a Moiré pattern by overlaying two line gratings with a slight difference in rotation.

```bash
python moire_cli.py artistic \
--layer "type=lines;pitch=10;angle=0" \
--layer "type=lines;pitch=10;angle=3" \
--output "artistic_lines.gif" \
--resolution 1024 \
--marker-size 2
```

**Example: Hexagonal Lattice over Lines**

This example composes a hexagonal lattice layer with a line grating.

```bash
python moire_cli.py artistic \
--layer "type=hex;const=30;angle=0" \
--layer "type=lines;pitch=8;angle=15" \
--output "artistic_hex_lines.gif"
```

### 3. Scientific Mode Example

The scientific mode is for simulating specific physical systems. Currently, it models a twisted bilayer hexagonal lattice.

**Example: Simulating Twisted Graphene**

This generates the Moiré superlattice from two hexagonal grids with a 2.5-degree twist angle.

```bash
python moire_cli.py scientific \
--lattice-constant 25 \
--twist-angle 2.5 \
--output "scientific_twisted_hex.gif" \
--resolution 1024 \
--speed 0.4
```

## Project Structure

The project is organized into several modules to ensure maintainability and separation of concerns:

- `moire_cli.py`: The main entry point. Handles all command-line argument parsing and delegates tasks to the engine.
- `engine.py`: The core orchestrator. Contains the main logic for the artistic and scientific modes.
- `patterns.py`: A library of functions for generating the fundamental 2D patterns (lines, hexagons, etc.).
- `rendering.py`: Handles all matplotlib-based 3D visualization and animation rendering.
- `utils.py`: Contains helper functions (e.g., string parsing) and shared constants.
- `README.md`: This documentation file.

## Future Roadmap

This tool is designed for expansion. Based on the foundational research, future development will focus on:

- **Metrology Mode:** For simulating strain and displacement analysis.
- **Security Mode:** For generating anti-counterfeiting patterns and implementing shape Moiré for steganography.
- **Expanded Pattern Library:** Adding support for circles, square lattices, and other 2D Bravais lattices.
- **Data Export:** In scientific mode, adding functionality to export atomic coordinates for use in physics simulation software.


- update based on no longer using mize and venv
- You simply document these steps in your README.md file. A new user would:

git clone ...

cd moire

python3.11 -m venv .venv

source .venv/bin/activate

pip install -r requirements.txt