import numpy as np
import matplotlib.pyplot as plt

def save_static_2d(args, composed_pattern_2d):
    """
    Saves the generated 2D Moiré pattern as a static image.
    """
    print("\n[+] Saving static 2D image...")
    try:
        plt.imsave(args.output, composed_pattern_2d, cmap='gray')
        print(f"\nSuccess! 2D image saved as '{args.output}'")
    except Exception as e:
        print(f"\n\nError saving 2D image: {e}")