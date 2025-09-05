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
    params = {}
    try:
        for part in layer_str.split(';'):
            key, value = part.strip().split('=', 1)
            try:
                params[key.strip()] = float(value.strip())
            except ValueError:
                params[key.strip()] = value.strip()
    except ValueError:
        print(f"Error: Malformed layer definition string: '{layer_str}'")
        print("Expected format: 'key1=value1;key2=value2'")
        return None
    return params