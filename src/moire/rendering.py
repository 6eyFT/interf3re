import numpy as np
import matplotlib.pyplot as plt
import sys

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

def save_static_3d(args, composed_pattern_2d):
    """
    Generates and saves a static 3D view of the extruded pattern.
    """
    print("\n[+] Initializing 3D environment for static render...")
    
    # 1. Create a 3D grid of points for scattering
    num_xy_points = args.num_points // args.z_layers
    grid_res = int(np.sqrt(num_xy_points))

    points_x_flat = np.linspace(0, composed_pattern_2d.shape[1], grid_res)
    points_y_flat = np.linspace(0, composed_pattern_2d.shape[0], grid_res)
    points_z_flat = np.linspace(-args.depth / 2, args.depth / 2, args.z_layers)

    xx, yy, zz = np.meshgrid(points_x_flat, points_y_flat, points_z_flat)
    points_x, points_y, points_z = xx.flatten(), yy.flatten(), zz.flatten()

    # 2. Map the 2D pattern intensity to the points' color
    x_indices = points_x.astype(int)
    y_indices = points_y.astype(int)
    x_indices = np.clip(x_indices, 0, composed_pattern_2d.shape[1] - 1)
    y_indices = np.clip(y_indices, 0, composed_pattern_2d.shape[0] - 1)
    
    colors = composed_pattern_2d[y_indices, x_indices]

    # 3. Set up the 3D plot
    fig = plt.figure(figsize=(10, 10), dpi=150)
    ax = fig.add_subplot(111, projection='3d')
    
    ax.scatter(
        points_x, points_y, points_z,
        s=args.marker_size,
        c=colors,
        cmap='gray_r',
        alpha=args.alpha
    )

    # Configure plot appearance
    ax.set_facecolor('black')
    ax.grid(False)
    ax.set_xticks([]); ax.set_yticks([]); ax.set_zticks([])
    ax.w_xaxis.pane.fill = False
    ax.w_yaxis.pane.fill = False
    ax.w_zaxis.pane.fill = False
    ax.set_xlabel('X'); ax.set_ylabel('Y'); ax.set_zlabel('Z')
    ax.xaxis.label.set_color('white'); ax.yaxis.label.set_color('white'); ax.zaxis.label.set_color('white')
    ax.tick_params(axis='x', colors='white'); ax.tick_params(axis='y', colors='white'); ax.tick_params(axis='z', colors='white')
    ax.view_init(elev=30., azim=45) # Set a fixed, pleasing camera angle

    # 4. Save the static 3D figure
    try:
        print("[+] Saving 3D render...")
        fig.savefig(args.output, dpi=150, bbox_inches='tight', pad_inches=0.1, facecolor='black')
        plt.close(fig) # Close the figure to free memory
        print(f"\nSuccess! 3D image saved as '{args.output}'")
    except Exception as e:
        print(f"\n\nError saving 3D image: {e}")