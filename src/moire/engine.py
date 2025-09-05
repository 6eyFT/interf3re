import numpy as np
from .patterns import generate_line_pattern, generate_hex_pattern
from .rendering import save_static_2d, save_static_3d
from .utils import parse_layer_def

def run_artistic_mode(args):
    """
    Generates a pattern from a list of user-defined layers and renders it.
    """
    print("[+] Running in ARTISTIC mode.")
    shape = (args.resolution, args.resolution)
    # Start with a neutral base (1.0 for multiplicative blending)
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
        
        # Combine layers using multiplication
        composed_pattern *= pattern

    # Pass the final 2D pattern to the appropriate rendering function
    if args.dimension == '2d':
        save_static_2d(args, composed_pattern)
    else:
        save_static_3d(args, composed_pattern)

def run_scientific_mode(args):
    """
    Generates a twisted bilayer hexagonal lattice and renders it.
    """
    print("[+] Running in SCIENTIFIC mode (Twisted Bilayer Hexagonal).")
    shape = (args.resolution, args.resolution)
    
    print(f"[+] Generating base layer with lattice constant: {args.lattice_constant}...")
    layer1 = generate_hex_pattern(shape, args.lattice_constant, 0)
    
    print(f"[+] Generating second layer twisted by {args.twist_angle} degrees...")
    layer2 = generate_hex_pattern(shape, args.lattice_constant, args.twist_angle)
    
    # Combine layers using multiplication to simulate superposition
    composed_pattern = layer1 * layer2

    # Pass the final 2D pattern to the appropriate rendering function
    if args.dimension == '2d':
        save_static_2d(args, composed_pattern)
    else:
        save_static_3d(args, composed_pattern)