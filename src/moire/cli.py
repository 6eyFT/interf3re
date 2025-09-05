import argparse
from .engine import run_artistic_mode, run_scientific_mode
from .utils import SPLASH_SCREEN

def main():
    """
    Main function to parse arguments and delegate to the engine.
    """
    parser = argparse.ArgumentParser(
        description="A CLI tool to generate 3D moiré pattern images, adapted from Moiré research.",
        formatter_class=argparse.RawTextHelpFormatter
    )

    # Global arguments
    parser.add_argument('--no-splash', action='store_true', help='Disable the splash screen.')
    subparsers = parser.add_subparsers(dest='mode', required=True, help='Select generation mode')

    # --- ARTISTIC MODE ---
    parser_art = subparsers.add_parser('artistic', help='Compose multiple custom layers for creative effects.')
    parser_art.add_argument('--layer', action='append', required=True, help='Define a pattern layer. Can be used multiple times.\nFormat: "type=<type>;param1=val1;param2=val2"\nExample: --layer "type=lines;pitch=12;angle=15" --layer "type=hex;const=30"')
    parser_art.set_defaults(func=run_artistic_mode)

    # --- SCIENTIFIC MODE ---
    parser_sci = subparsers.add_parser('scientific', help='Simulate physically-based Moiré superlattices.')
    parser_sci.add_argument('--lattice-type', default='hexagonal', help='Type of lattice (currently only "hexagonal" is supported).')
    parser_sci.add_argument('--lattice-constant', type=float, default=25.0, help='Lattice constant (spacing) in pixels.')
    parser_sci.add_argument('--twist-angle', type=float, default=5.0, help='Twist angle between the two layers in degrees.')
    parser_sci.set_defaults(func=run_scientific_mode)

    # --- Common arguments for all modes ---
    for p in [parser_art, parser_sci]:
        p.add_argument('-o', '--output', type=str, default='moiré_pattern.png', help='Output filename (e.g., pattern.png).')
        p.add_argument('--resolution', type=int, default=1024, help='Resolution of the base pattern (e.g., 1024 for 1024x1024).')
        p.add_argument('--dimension', type=str, default='3d', choices=['2d', '3d'], help='Output a 2D or 3D static image.')
        
        # 3D specific arguments
        p.add_argument('--num-points', type=int, default=50000, help='(3D only) Total number of points in the scatter cloud.')
        p.add_argument('--depth', type=int, default=100, help='(3D only) Depth of the 3D extrusion.')
        p.add_argument('--z-layers', type=int, default=10, help='(3D only) Number of stacked layers in the Z-dimension.')
        p.add_argument('--marker-size', type=int, default=5, help='(3D only) Size of the individual points.')
        p.add_argument('--alpha', type=float, default=0.7, help='(3D only) Transparency of points (0.0 to 1.0).')

    args = parser.parse_args()

    if not args.no_splash:
        print(SPLASH_SCREEN)

    # Call the appropriate function from the engine
    args.func(args)

if __name__ == "__main__":
    main()