import numpy as np

def generate_line_pattern(shape, pitch=10.0, angle=0.0):
    """
    Generates a 2D sinusoidal line grating.
    """
    h, w = shape
    angle_rad = np.deg2rad(angle)
    x = np.linspace(-w/2, w/2, w)
    y = np.linspace(-h/2, h/2, h)
    xx, yy = np.meshgrid(x, y)
    
    # Rotate coordinates
    x_rot = xx * np.cos(angle_rad) + yy * np.sin(angle_rad)
    
    # Create sinusoidal pattern (values between 0 and 1)
    pattern = (np.cos(2 * np.pi * x_rot / pitch) + 1) / 2
    return pattern

def generate_hex_pattern(shape, lattice_constant=20.0, angle=0.0):
    """
    Generates a 2D hexagonal lattice pattern.
    """
    h, w = shape
    angle_rad = np.deg2rad(angle)
    
    # Hexagonal lattice basis vectors
    a1 = lattice_constant * np.array([1, 0])
    a2 = lattice_constant * np.array([0.5, np.sqrt(3)/2])

    # Create a coordinate grid larger than the canvas to handle rotation
    x_vals = np.linspace(-w, w, 2*w)
    y_vals = np.linspace(-h, h, 2*h)
    xx, yy = np.meshgrid(x_vals, y_vals)

    # Rotate coordinates
    xx_rot = xx * np.cos(angle_rad) + yy * np.sin(angle_rad)
    yy_rot = -xx * np.sin(angle_rad) + yy * np.cos(angle_rad)
    coords = np.stack((xx_rot, yy_rot), axis=-1)

    # Use linear algebra to find the distance of each pixel to the nearest lattice point
    inv_basis = np.linalg.inv(np.stack((a1, a2), axis=1))
    frac_coords = np.einsum('ij,klj->kli', inv_basis, coords)
    
    nearest_lattice_frac = np.round(frac_coords)
    dist_vector = coords - np.einsum('ij,klj->kli', np.stack((a1, a2), axis=1), nearest_lattice_frac)
    dist = np.linalg.norm(dist_vector, axis=-1)

    # Create pattern using a Gaussian function around each lattice point
    sigma = lattice_constant / 4.0
    pattern = np.exp(-dist**2 / (2 * sigma**2))
    
    # Crop the oversized grid back to the requested shape
    return pattern[:h, :w]