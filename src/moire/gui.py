import dearpygui.dearpygui as dpg
import numpy as np
import threading
import time

# Import our existing backend logic
from .patterns import generate_line_pattern, generate_hex_pattern
from .rendering import run_animation # We will call this for the final render

# --- CONFIG & STATE ---
# A dictionary to hold the state of our application
app_state = {
    "layers": [],
    "preview_dirty": True, # Flag to check if the preview needs updating
    "status_text": "Idle.",
    "preview_resolution": 512,
}

# --- AESTHETICS & THEME ---

def setup_y2k_theme():
    """Applies the custom retro Y2K / unixporn theme."""
    with dpg.theme() as global_theme:
        with dpg.theme_component(dpg.mvAll):
            # Colors
            dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (20, 20, 30, 255))
            dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (25, 25, 35, 255))
            dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (40, 40, 50, 255))
            dpg.add_theme_color(dpg.mvThemeCol_Button, (60, 80, 120, 255))
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (80, 100, 150, 255))
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (100, 120, 180, 255))
            dpg.add_theme_color(dpg.mvThemeCol_Header, (60, 80, 120, 255))
            dpg.add_theme_color(dpg.mvThemeCol_HeaderHovered, (80, 100, 150, 255))
            dpg.add_theme_color(dpg.mvThemeCol_Tab, (40, 40, 50, 255))
            dpg.add_theme_color(dpg.mvThemeCol_TabActive, (60, 80, 120, 255))
            dpg.add_theme_color(dpg.mvThemeCol_TitleBgActive, (0, 180, 255, 255))
            dpg.add_theme_color(dpg.mvThemeCol_CheckMark, (0, 255, 150, 255))
            dpg.add_theme_color(dpg.mvThemeCol_SliderGrab, (0, 255, 150, 255))
            dpg.add_theme_color(dpg.mvThemeCol_SliderGrabActive, (50, 255, 200, 255))

            # Styling
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 3)
            dpg.add_theme_style(dpg.mvStyleVar_WindowRounding, 0)
            dpg.add_theme_style(dpg.mvStyleVar_ChildRounding, 0)
            dpg.add_theme_style(dpg.mvStyleVar_WindowBorderSize, 0)
            dpg.add_theme_style(dpg.mvStyleVar_FrameBorderSize, 1)
            dpg.add_theme_style(dpg.mvStyleVar_ChildBorderSize, 1)

    dpg.bind_theme(global_theme)

    # Font - You can replace this with a custom .ttf file for more flair
    try:
        with dpg.font_registry():
            # Correct, relative path to the bundled font
            default_font = dpg.add_font("src/moire/assets/fonts/Inconsolata-Regular.ttf", 16)
        dpg.bind_font(default_font)
    except Exception as e:
        print(f"Could not load custom font, using default. Error: {e}")


# --- CORE LOGIC & CALLBACKS ---

def mark_dirty(sender, app_data, user_data):
    """Callback to flag that the preview needs to be regenerated."""
    app_state["preview_dirty"] = True

def update_preview():
    """Generates and displays the 2D Moiré pattern preview."""
    res = app_state["preview_resolution"]
    shape = (res, res)

    # Determine which mode is active
    active_mode = dpg.get_value("main_tab_bar")

    # Start with a neutral base (1.0 for multiplicative blending)
    composed_pattern = np.ones(shape, dtype=np.float32)

    if active_mode == "artistic_tab":
        for layer in app_state["layers"]:
            layer_type = dpg.get_value(f"type_{layer}")
            if layer_type == "Lines":
                pitch = dpg.get_value(f"pitch_{layer}")
                angle = dpg.get_value(f"angle_{layer}")
                pattern = generate_line_pattern(shape, pitch, angle)
            elif layer_type == "Hexagonal":
                const = dpg.get_value(f"const_{layer}")
                angle = dpg.get_value(f"angle_hex_{layer}")
                pattern = generate_hex_pattern(shape, const, angle)
            composed_pattern *= pattern.astype(np.float32)

    elif active_mode == "scientific_tab":
        const = dpg.get_value("sci_const")
        angle = dpg.get_value("sci_angle")
        layer1 = generate_hex_pattern(shape, const, 0)
        layer2 = generate_hex_pattern(shape, const, angle)
        composed_pattern = layer1.astype(np.float32) * layer2.astype(np.float32)

    # Convert the grayscale numpy array to an RGBA format for DPG
    # We map intensity to all R, G, and B channels, and keep Alpha at max
    rgba_pattern = np.zeros((res, res, 4), dtype=np.float32)
    rgba_pattern[..., 0] = composed_pattern # Red
    rgba_pattern[..., 1] = composed_pattern # Green
    rgba_pattern[..., 2] = composed_pattern # Blue
    rgba_pattern[..., 3] = 1.0              # Alpha

    # Update the texture
    dpg.set_value("preview_texture", rgba_pattern)
    app_state["preview_dirty"] = False
    app_state["status_text"] = f"Preview updated [{res}x{res}]."

def add_layer():
    """Adds a new layer control group to the artistic tab."""
    layer_id = dpg.generate_uuid()
    app_state["layers"].append(layer_id)

    with dpg.collapsing_header(label=f"✧ Layer {len(app_state['layers'])}", default_open=True, parent="artistic_tab", tag=f"header_{layer_id}"):
        dpg.add_combo(["Lines", "Hexagonal"], label="Type", width=-1, default_value="Lines", tag=f"type_{layer_id}", callback=mark_dirty)
        dpg.add_drag_float(label="Pitch / Const", tag=f"pitch_{layer_id}", default_value=10.0, speed=0.1, callback=mark_dirty)
        dpg.add_drag_float(label="Angle", tag=f"angle_{layer_id}", default_value=0.0, speed=0.1, callback=mark_dirty)

        # This is a simple way to show/hide controls based on type, more complex logic can be added
        dpg.configure_item(f"pitch_{layer_id}", show=True)
        dpg.configure_item(f"angle_{layer_id}", show=True)

    mark_dirty(None, None, None)

def remove_layer():
    """Removes the last layer."""
    if app_state["layers"]:
        layer_id = app_state["layers"].pop()
        dpg.delete_item(f"header_{layer_id}")
        mark_dirty(None, None, None)

def generate_final_animation():
    """Calls the backend animation renderer in a separate thread."""
    app_state["status_text"] = "Generating final animation... GUI may be unresponsive."
    dpg.set_value("status_bar_text", app_state["status_text"])

    # Create a simple args object to pass to the backend
    class Args:
        pass
    args = Args()
    args.output = dpg.get_value("output_filename")
    args.resolution = dpg.get_value("final_resolution")
    args.speed = dpg.get_value("anim_speed")
    args.frames = dpg.get_value("anim_frames")
    args.num_points = dpg.get_value("anim_points")
    args.depth = dpg.get_value("anim_depth")
    args.z_layers = dpg.get_value("anim_zlayers")
    args.marker_size = dpg.get_value("anim_markersize")
    args.alpha = dpg.get_value("anim_alpha")

    # Generate the final high-res 2D pattern
    shape = (args.resolution, args.resolution)
    composed_pattern = np.ones(shape, dtype=float)
    active_mode = dpg.get_value("main_tab_bar")

    if active_mode == "artistic_tab":
        for layer in app_state["layers"]:
            layer_type = dpg.get_value(f"type_{layer}")
            if layer_type == "Lines":
                pitch = dpg.get_value(f"pitch_{layer}")
                angle = dpg.get_value(f"angle_{layer}")
                pattern = generate_line_pattern(shape, pitch, angle)
            elif layer_type == "Hexagonal":
                const = dpg.get_value(f"pitch_{layer}") # Use the same slider for const
                angle = dpg.get_value(f"angle_{layer}")
                pattern = generate_hex_pattern(shape, const, angle)
            composed_pattern *= pattern

    elif active_mode == "scientific_tab":
        const = dpg.get_value("sci_const")
        angle = dpg.get_value("sci_angle")
        layer1 = generate_hex_pattern(shape, const, 0)
        layer2 = generate_hex_pattern(shape, const, angle)
        composed_pattern = layer1 * layer2

    # Run the animation function from rendering.py
    run_animation(args, composed_pattern)
    app_state["status_text"] = f"Success! Animation saved as '{args.output}'"
    dpg.set_value("status_bar_text", app_state["status_text"])

def run_generation_threaded():
    """Wrapper to run the generation in a thread to avoid freezing the GUI."""
    thread = threading.Thread(target=generate_final_animation)
    thread.start()

# --- UI LAYOUT ---

dpg.create_context()

# Texture Registry for the live preview
with dpg.texture_registry():
    # Create a blank texture
    blank_preview = np.zeros((app_state["preview_resolution"], app_state["preview_resolution"], 4), dtype=np.float32)
    dpg.add_raw_texture(
        width=app_state["preview_resolution"],
        height=app_state["preview_resolution"],
        default_value=blank_preview,
        format=dpg.mvFormat_Float_rgba,
        tag="preview_texture"
    )

# Main Window
with dpg.window(label="Main", tag="primary_window"):
    setup_y2k_theme()

    with dpg.group(horizontal=True):
        # --- LEFT PANEL: CONTROLS ---
        with dpg.child_window(width=400):
            dpg.add_text("◆ CONTROLS ◆", color=(0, 255, 150, 255))
            dpg.add_separator()

            with dpg.tab_bar(tag="main_tab_bar", callback=mark_dirty):
                # -- ARTISTIC MODE --
                with dpg.tab(label="Artistic", tag="artistic_tab"):
                    with dpg.group(horizontal=True):
                        dpg.add_button(label="[+] Add Layer", callback=add_layer, width=180)
                        dpg.add_button(label="[-] Remove Layer", callback=remove_layer, width=180)
                    dpg.add_separator()

                # -- SCIENTIFIC MODE --
                with dpg.tab(label="Scientific", tag="scientific_tab"):
                    dpg.add_text("Twisted Bilayer Hexagonal Lattice")
                    dpg.add_drag_float(label="Lattice Constant", tag="sci_const", default_value=25.0, speed=0.1, callback=mark_dirty)
                    dpg.add_drag_float(label="Twist Angle", tag="sci_angle", default_value=5.0, speed=0.1, callback=mark_dirty, max_value=90.0)

                # -- PLACEHOLDERS FOR ROADMAP --
                with dpg.tab(label="Metrology"):
                    dpg.add_text("Metrology features planned for a future version.", wrap=380)
                with dpg.tab(label="Security"):
                    dpg.add_text("Shape Moiré and security features planned for a future version.", wrap=380)

            dpg.add_spacer(height=20)
            dpg.add_text("◆ FINAL RENDER SETTINGS ◆", color=(0, 255, 150, 255))
            dpg.add_separator()

            with dpg.collapsing_header(label="Output & Animation", default_open=True):
                dpg.add_input_text(label="Output Filename", default_value="gui_output.gif", tag="output_filename")
                dpg.add_drag_int(label="Final Resolution", default_value=1024, tag="final_resolution", speed=16)
                dpg.add_drag_float(label="Animation Speed", default_value=0.5, tag="anim_speed", speed=0.01)
                dpg.add_drag_int(label="Animation Frames", default_value=720, tag="anim_frames", speed=10)

            with dpg.collapsing_header(label="3D Point Cloud"):
                dpg.add_drag_int(label="Number of Points", default_value=40000, tag="anim_points", speed=1000)
                dpg.add_drag_int(label="Cloud Depth", default_value=100, tag="anim_depth", speed=5)
                dpg.add_drag_int(label="Z-Layers", default_value=10, tag="anim_zlayers", speed=1)
                dpg.add_drag_int(label="Marker Size", default_value=5, tag="anim_markersize", min_value=1)
                dpg.add_drag_float(label="Marker Alpha", default_value=0.7, tag="anim_alpha", min_value=0.0, max_value=1.0, speed=0.01)

            dpg.add_spacer(height=20)
            dpg.add_button(label="✨ G E N E R A T E ✨", width=-1, height=40, callback=run_generation_threaded)


        # --- RIGHT PANEL: PREVIEW ---
        with dpg.child_window():
            dpg.add_text("◆ LIVE PREVIEW ◆", color=(0, 255, 150, 255))
            dpg.add_separator()
            # The preview image will be drawn here
            dpg.add_image("preview_texture")

    # --- BOTTOM PANEL: STATUS BAR ---
    with dpg.child_window(height=40, menubar=True):
        with dpg.menu_bar():
            dpg.add_text(app_state["status_text"], tag="status_bar_text")

# --- MAIN RENDER LOOP ---
dpg.create_viewport(title='// MOIRÉ_GENERATOR_v2.1 //', width=1280, height=720)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("primary_window", True)

# Initialize with one layer for the user
add_layer()

while dpg.is_dearpygui_running():
    # Only update the preview if a control has been changed
    if app_state["preview_dirty"]:
        update_preview()
        dpg.set_value("status_bar_text", app_state["status_text"])

    dpg.render_dearpygui_frame()

dpg.destroy_context()