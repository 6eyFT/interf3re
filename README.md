# Interf3re: A Moiré Pattern Generator

**Interf3re** is a command-line interface (CLI) and graphical user interface (GUI) tool for generating 2D Moiré pattern images in Python.  
Its architecture is based on the principles of **wave interference** and **superlattice generation**.

The tool uses a modular, layer-based engine: fundamental 2D patterns (lines, hexagonal lattices, etc.) are generated and then composed to create complex Moiré effects.

---

## Features

- **Modular Architecture**  
  Core logic is decoupled into separate modules for pattern generation, engine orchestration, and rendering.

- **Layer-Based Composition**  
  Build complex visuals by overlaying multiple simple layers.

- **Extensible Pattern Library**  
  Currently supports line gratings and hexagonal lattices.

- **Dual Interface**  
  Usable both as an interactive GUI and a scriptable CLI tool.

---

## Installation

Interf3re uses Python’s standard virtual environment system.

Clone the repository:

```bash
git clone <your-repository-url>
cd interf3re
```

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

For development, install in editable mode (makes the `moire` package importable when running scripts):

```bash
pip install -e .
```

---

## Usage

### GUI Mode

Run the interactive graphical interface:

```bash
python -m moire.gui
```

### CLI Mode

Run directly from the command line as a module.

**Example – Classic Rotated Line Pattern:**

```bash
python -m moire.cli \
  --layer "type=lines;pitch=10;angle=0" \
  --layer "type=lines;pitch=10;angle=3" \
  --output "cli_lines.png" \
  --resolution 1024
```

---

## Roadmap

1. **Extend Pattern Library**  
   Add new base patterns beyond lines and hexagonal lattices to expand creative possibilities.

2. **Hall of Fame**  
   Showcase example Moiré images created by the author and highlight notable user submissions.

3. **3D Functionality**  
   Support generation and rendering of Moiré effects in three dimensions.

4. **Animation System**  
   Instead of saving a single image, users will be able to save *render states*.  
   By selecting two or more states (A → B), the app will generate animations of transformations over a chosen time duration.

5. **Steganography & Password Encoding**  
   Explore embedding hidden messages or password data within Moiré images as a form of visual encryption.

---

## Further Reading
Interf3re is based on original research into Moiré pattern generation.  
For a deeper dive into the theory, see the full paper:  
[Generating Moiré Patterns – Research Paper](https://6eyft.github.io/interf3re/)  
