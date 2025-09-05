import argparse
from .engine import generate_pattern
from .utils import SPLASH_SCREEN

def main():
    """
    Main function to parse arguments and delegate to the engine.
    """
    parser = argparse.ArgumentParser(
        description="A CLI tool to generate 2D and 3D Moiré pattern images.",
        formatter_class=argparse.RawTextHelpFormatter
    )

    # --- Unified Arguments ---
    parser.add_argument('--no-splash', action='store_true', help='Disable the splash screen.')
    parser.add_argument('--layer', action='append', required=True, help='Define a pattern layer. Can be used multiple times.\nFormat: "type=<type>;param1=val1;param2=val2"\nExample: --layer "type=lines;pitch=12;angle=15" --layer "type=hex;const=30"')
    parser.add_argument('-o', '--output', type=str, default='moire_pattern.png', help='Output filename (e.g., pattern.png).')
    parser.add_argument('--resolution', type=int, default=1024, help='Resolution of the base pattern (e.g., 1024 for 1024x1024).')
    parser.add_argument('--dimension', type=str, default='3d', choices=['2d', '3d'], help='Output a 2D or 3D static image.')
    
    # --- 3D Specific Arguments ---
    parser.add_argument('--num-points', type=int, default=50000, help='(3D only) Total number of points in the scatter cloud.')
    parser.add_argument('--depth', type=int, default=100, help='(3D only) Depth of the 3D extrusion.')
    parser.add_argument('--z-layers', type=int, default=10, help='(3D only) Number of stacked layers in the Z-dimension.')
    parser.add_argument('--marker-size', type=int, default=5, help='(3D only) Size of the individual points.')
    parser.add_argument('--alpha', type=float, default=0.7, help='(3D only) Transparency of points (0.0 to 1.0).')

    args = parser.parse_args()

    if not args.no_splash:
        print(SPLASH_SCREEN)

    # Call the unified engine function
    generate_pattern(args)

if __name__ == "__main__":
    main()