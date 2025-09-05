# Moiré Pattern Generator (V2)

This is a command-line interface (CLI) and graphical user interface (GUI) tool for generating 2D Moiré pattern images in Python. The architecture is based on the principles of wave interference and superlattice generation, designed for both creative and scientific applications.

The tool operates on a modular, layer-based engine where fundamental 2D patterns (like lines and hexagonal lattices) are generated and then composed to create complex Moiré effects.

## Features

- **Modular Architecture:** Core logic is decoupled into separate modules for pattern generation, engine orchestration, and rendering.
- **Layer-Based Composition:** Build complex patterns by overlaying multiple simple layers.
- **Extensible Pattern Library:** Currently supports generating line gratings and hexagonal lattices.
- **Dual Interface:** Usable as both an interactive GUI and a scriptable command-line tool.

## Installation

This tool uses Python's standard virtual environment system.

1.  **Clone the repository:**
    ```bash
    git clone <your-repository-url>
    cd interf3re
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **(Development) Install the package in editable mode:**
    ```bash
    pip install -e .
    ```

## Usage

### GUI Mode
To run the interactive graphical interface, run the following command from the project root:
```bash
python -m moire.gui
```

## CLI Mode
The application can also be run from the command line via `cli.py`.

**Example: Classic Rotated Line Pattern
**
```python
python -m moire.cli \
--layer "type=lines;pitch=10;angle=0" \
--layer "type=lines;pitch=10;angle=3" \
--output "cli_lines.png" \
--resolution 1024
```