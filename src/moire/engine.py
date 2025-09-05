import numpy as np
from .patterns import generate_line_pattern, generate_hex_pattern
from .rendering import save_static_2d
from .utils import parse_layer_def

def normalize_pattern(pattern):
    """Scales a pattern's values to the full 0.0 to 1.0 range."""
    min_val = np.min(pattern)
    max_val = np.max(pattern)
    if max_val > min_val:
        return (pattern - min_val) / (max_val - min_val)
    return pattern

def generate_pattern(args):
    """
    Generates a pattern from a list of user-defined layers and renders it.
    """
    print("[+] Running Moiré Generator.")
    shape = (args.resolution, args.resolution)
    composed_pattern = np.ones(shape, dtype=float)

    print(f"[+] Composing {len(args.layer)} layers...")
    for i, layer_str in enumerate(args.layer):
        params = parse_layer_def(layer_str)
        if params is None: continue
        
        layer_type = params.get('type', 'lines')
        print(f"  - Layer {i+1}: type={layer_type}, params={params}")

        if layer_type == 'lines':
            pattern = generate_line_pattern(shape, params.get('pitch', 10), params.get('angle', 0))
        elif layer_type == 'hex':
            pattern = generate_hex_pattern(shape, params.get('const', 20), params.get('angle', 0))
        else:
            print(f"Warning: Unknown layer type '{layer_type}'. Skipping.")
            continue
        
        composed_pattern *= pattern

    final_pattern = normalize_pattern(composed_pattern)

    save_static_2d(args, final_pattern)