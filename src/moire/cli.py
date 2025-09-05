import argparse
from .engine import generate_pattern
from .utils import SPLASH_SCREEN

def main():
    """
    Main function to parse arguments and delegate to the engine.
    """
    parser = argparse.ArgumentParser(
        description="A CLI tool to generate 2D Moiré pattern images.",
        formatter_class=argparse.RawTextHelpFormatter
    )

    # --- Unified Arguments ---
    parser.add_argument('--no-splash', action='store_true', help='Disable the splash screen.')
    parser.add_argument('--layer', action='append', required=True, help='Define a pattern layer. Can be used multiple times.\nFormat: "type=<type>;param1=val1;param2=val2"\nExample: --layer "type=lines;pitch=12;angle=15" --layer "type=hex;const=30"')
    parser.add_argument('-o', '--output', type=str, default='moire_pattern.png', help='Output filename (e.g., pattern.png).')
    parser.add_argument('--resolution', type=int, default=1024, help='Resolution of the base pattern (e.g., 1024 for 1024x1024).')
    
    args = parser.parse_args()

    if not args.no_splash:
        print(SPLASH_SCREEN)

    # Call the unified engine function
    generate_pattern(args)

if __name__ == "__main__":
    main()