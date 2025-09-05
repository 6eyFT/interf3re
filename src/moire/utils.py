# ASCII Art for the splash screen
SPLASH_SCREEN = r"""
  __  __  ____   ___  _  _    __    ____  ____  ____  ____
 (  \/  )(_  _) / __)( \/ )  /__\  (  _ \( ___)(_  _)(  _ \
  )    (  _)(_ ( (__  )  (  /(__)\  )   / )__)   )(   )   /
 (_/\/\_)(____) \___)(_/\_)(__)(__)(_)\_)(____) (__) (_)\_)
 ____   ___  ____    __   ____  _  _  ____  ____  ____  ____
( ___)/ __)(_  _)  /__\ (_  _)( \( )( ___)(  _ \(  __)(  _ \
 )__) \__ \  )(   /(__)\  )(   )  (  )__)  )   / ) _)  )   /
(____)(___/ (__) (__)(__)(__) (_)\_)(____)(_)\_)(____)(_)\_)

      -- A 3D Moiré Pattern CLI Generator --
      --     (Version 2.0 - Research Adapted)     --
"""

def parse_layer_def(layer_str):
    """
    Parses a layer definition string (e.g., "type=lines;pitch=10") into a dictionary.
    """
    if not layer_str or not layer_str.strip():
        return {}
        
    params = {}
    try:
        # Split by semicolon and filter out any empty parts from trailing semicolons
        parts = [part.strip() for part in layer_str.split(';') if part.strip()]
        if not parts and layer_str: # Handle cases like a single malformed part with no semicolon
             raise ValueError("Invalid format")

        for part in parts:
            # Each part must contain exactly one '='
            if part.count('=') != 1:
                raise ValueError("Each segment must be a key=value pair.")
                
            key, value = part.split('=', 1)
            key = key.strip()
            value = value.strip()
            
            # Key and value must not be empty
            if not key or not value:
                raise ValueError("Key or value cannot be empty.")

            try:
                params[key] = float(value)
            except ValueError:
                params[key] = value
    except (ValueError, IndexError):
        print(f"Error: Malformed layer definition string: '{layer_str}'")
        print("Expected format: 'key1=value1;key2=value2'")
        return None
    return params