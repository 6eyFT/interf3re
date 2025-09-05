import dearpygui.dearpygui as dpg
import numpy as np
import threading
import time
import os

# Import our existing backend logic
from .patterns import generate_line_pattern, generate_hex_pattern
from .rendering import save_static_2d, save_static_3d

# --- HELPERS TEXT ---
# A central dictionary for all tooltip text
helper_text = {
    "enable_helpers": "Toggles these informational popups on or off.",
    "mode_tabs": "Choose the primary mode of pattern generation.\nArtistic: Freely combine multiple layers.\nScientific: Simulate a specific physical system.",
    "add_remove_layer": "Add or remove pattern layers that will be combined to create the final effect.",
    "layer_type": "Select the fundamental pattern for this layer.",
    "pitch_const": "For Lines: Controls the distance between lines (Pitch).\nFor Hexagonal: Controls the distance between points (Lattice Constant).",
    "layer_angle": "Controls the rotation of this specific layer in degrees.",
    "sci_const": "Controls the base distance between points in the hexagonal lattice.",
    "sci_angle": "Controls the twist angle in degrees between the two hexagonal layers.",
    "output_dim": "Choose whether to generate a flat 2D image or a 3D point cloud image.",
    "output_filename": "The name of the output file. Should end in .png.",
    "final_resolution": "The resolution (width and height) of the generated image in pixels. Higher values take longer to render.",
    "3d_points": "(3D Only) The total number of points to use in the 3D cloud. More points create a denser, more detailed cloud.",
    "3d_depth": "(3D Only) The depth of the point cloud along the Z-axis.",
    "3d_zlayers": "(3D Only) How many times the 2D pattern is stacked along the Z-axis.",
    "3d_markersize": "(3D Only) The size of each individual point in the 3D scatter plot.",
    "3d_alpha": "(3D Only) The transparency of the points. 0.0 is fully transparent, 1.0 is fully opaque.",
    "generate_button": "Generate the final static image with the current settings. This may take a moment."
}

# --- CONFIG & STATE ---
app_state = {
    "layers": [],
    "preview_dirty": True,
    "status_text": "Idle.",
    "preview_resolution": 512,
}

# --- AESTHETICS & THEME ---
def setup_y2k_theme():
    """Applies the custom retro Y2K / unixporn theme."""
    with dpg.theme() as global_theme:
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (20, 20, 30, 255))
            dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (25, 25, 35, 255))
            dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (40, 40, 50, 255))
            dpg.add_theme_color(dpg.mvThemeCol_Button, (60, 80, 120, 255))
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (80, 100, 150, 255))
            dpg.add_theme_color(dpg.mvThemeCol_Header, (60, 80, 120, 255))
            dpg.add_theme_color(dpg.mvThemeCol_HeaderHovered, (80, 100, 150, 255))
            dpg.add_theme_color(dpg.mvThemeCol_Tab, (40, 40, 50, 255))
            dpg.add_theme_color(dpg.mvThemeCol_TabActive, (60, 80, 120, 255))
            dpg.add_theme_color(dpg.mvThemeCol_TitleBgActive, (0, 180, 255, 255))
            dpg.add_theme_color(dpg.mvThemeCol_CheckMark, (0, 255, 150, 255))
            dpg.add_theme_color(dpg.mvThemeCol_SliderGrab, (0, 255, 150, 255))
            dpg.add_theme_color(dpg.mvThemeCol_SliderGrabActive, (50, 255, 200, 255))
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 3)
            dpg.add_theme_style(dpg.mvStyleVar_WindowBorderSize, 0)
    dpg.bind_theme(global_theme)

    try:
        font_path = os.path.join("src", "moire", "assets", "fonts", "Inconsolata-Regular.ttf")
        with dpg.font_registry():
            default_font = dpg.add_font(font_path, 16)
        dpg.bind_font(default_font)
    except Exception as e:
        print(f"Could not load custom font, using default. Error: {e}")

# --- CORE LOGIC & CALLBACKS ---
def add_helper(widget_tag, help_key):
    """Adds a conditional tooltip to a widget."""
    with dpg.tooltip(widget_tag):
        dpg.add_text(helper_text[help_key], wrap=300)
    dpg.bind_item_handler_registry(widget_tag, "tooltip_handler")

def mark_dirty(sender, app_data, user_data):
    app_state["preview_dirty"] = True

def update_preview():
    if not app_state["preview_dirty"]: return
    res = app_state["preview_resolution"]
    shape = (res, res)
    active_mode = dpg.get_value("main_tab_bar")
    composed_pattern = np.ones(shape, dtype=np.float32)

    if active_mode == "artistic_tab":
        for layer_id in app_state["layers"]:
            layer_type = dpg.get_value(f"type_{layer_id}")
            angle = dpg.get_value(f"angle_{layer_id}")
            if layer_type == "Lines":
                pitch = dpg.get_value(f"pitch_{layer_id}")
                pattern = generate_line_pattern(shape, pitch, angle)
            elif layer_type == "Hexagonal":
                const = dpg.get_value(f"pitch_{layer_id}")
                pattern = generate_hex_pattern(shape, const, angle)
            composed_pattern *= pattern.astype(np.float32)

    elif active_mode == "scientific_tab":
        const = dpg.get_value("sci_const")
        angle = dpg.get_value("sci_angle")
        layer1 = generate_hex_pattern(shape, const, 0)
        layer2 = generate_hex_pattern(shape, const, angle)
        composed_pattern = layer1.astype(np.float32) * layer2.astype(np.float32)

    rgba_pattern = np.zeros((res, res, 4), dtype=np.float32)
    rgba_pattern[..., :3] = composed_pattern[..., np.newaxis]
    rgba_pattern[..., 3] = 1.0
    
    dpg.set_value("preview_texture", rgba_pattern)
    app_state["preview_dirty"] = False
    app_state["status_text"] = f"Preview updated [{res}x{res}]."
    dpg.set_value("status_bar_text", app_state["status_text"])

def add_layer():
    layer_id = dpg.generate_uuid()
    app_state["layers"].append(layer_id)
    
    with dpg.collapsing_header(label=f"✧ Layer {len(app_state['layers'])}", default_open=True, parent="artistic_layers", tag=f"header_{layer_id}"):
        
        # Layer Type
        dpg.add_combo(["Lines", "Hexagonal"], label="Type", width=-1, default_value="Lines", tag=f"type_{layer_id}", callback=mark_dirty)
        add_helper(dpg.last_item(), "layer_type")
        
        # Pitch / Constant
        dpg.add_drag_float(label="Pitch / Const", tag=f"pitch_{layer_id}", default_value=10.0, speed=0.1, callback=mark_dirty)
        add_helper(dpg.last_item(), "pitch_const")

        # Angle
        dpg.add_drag_float(label="Angle", tag=f"angle_{layer_id}", default_value=0.0, speed=0.1, callback=mark_dirty)
        add_helper(dpg.last_item(), "layer_angle")
        
    mark_dirty(None, None, None)

def remove_layer():
    if app_state["layers"]:
        layer_id = app_state["layers"].pop()
        dpg.delete_item(f"header_{layer_id}", children_only=False)
        mark_dirty(None, None, None)

def generate_final_image():
    app_state["status_text"] = "Generating final image... GUI may be unresponsive."
    dpg.set_value("status_bar_text", app_state["status_text"])
    
    class Args: pass
    args = Args()
    args.output = dpg.get_value("output_filename")
    args.resolution = dpg.get_value("final_resolution")
    args.dimension = dpg.get_value("output_dim")
    args.num_points = dpg.get_value("anim_points")
    args.depth = dpg.get_value("anim_depth")
    args.z_layers = dpg.get_value("anim_zlayers")
    args.marker_size = dpg.get_value("anim_markersize")
    args.alpha = dpg.get_value("anim_alpha")

    shape = (args.resolution, args.resolution)
    composed_pattern = np.ones(shape, dtype=float)
    active_mode = dpg.get_value("main_tab_bar")

    if active_mode == "artistic_tab":
        for layer_id in app_state["layers"]:
            layer_type = dpg.get_value(f"type_{layer_id}")
            angle = dpg.get_value(f"angle_{layer_id}")
            if layer_type == "Lines":
                pitch = dpg.get_value(f"pitch_{layer_id}")
                pattern = generate_line_pattern(shape, pitch, angle)
            elif layer_type == "Hexagonal":
                const = dpg.get_value(f"pitch_{layer_id}")
                pattern = generate_hex_pattern(shape, const, angle)
            composed_pattern *= pattern
    elif active_mode == "scientific_tab":
        const = dpg.get_value("sci_const")
        angle = dpg.get_value("sci_angle")
        layer1 = generate_hex_pattern(shape, const, 0)
        layer2 = generate_hex_pattern(shape, const, angle)
        composed_pattern = layer1 * layer2

    if args.dimension == '2D':
        save_static_2d(args, composed_pattern)
    else: # 3D
        save_static_3d(args, composed_pattern)
        
    app_state["status_text"] = f"Success! Image saved as '{args.output}'"
    dpg.set_value("status_bar_text", app_state["status_text"])

def run_generation_threaded():
    thread = threading.Thread(target=generate_final_image)
    thread.start()

# --- UI LAYOUT ---
dpg.create_context()

with dpg.item_handler_registry(tag="tooltip_handler"):
    dpg.add_item_hover_handler(delay=1.0, callback=lambda s, a, u: dpg.configure_item(u, show=True), user_data=dpg.last_container())

with dpg.texture_registry():
    blank_preview = np.zeros((app_state["preview_resolution"], app_state["preview_resolution"], 4), dtype=np.float32)
    dpg.add_raw_texture(width=app_state["preview_resolution"], height=app_state["preview_resolution"], default_value=blank_preview, format=dpg.mvFormat_Float_rgba, tag="preview_texture")

with dpg.window(label="Main", tag="primary_window"):
    setup_y2k_theme()
    
    with dpg.group(horizontal=True):
        with dpg.child_window(width=400):
            dpg.add_text("◆ MOIRÉ CONTROLS ◆", color=(0, 255, 150, 255))
            dpg.add_separator()
            dpg.add_checkbox(label="Enable Helpers", tag="enable_helpers_checkbox", default_value=True)
            add_helper(dpg.last_item(), "enable_helpers")
            dpg.add_separator()
            
            with dpg.tab_bar(tag="main_tab_bar", callback=mark_dirty):
                with dpg.tab(label="Artistic", tag="artistic_tab"):
                    with dpg.group(horizontal=True):
                        dpg.add_button(label="[+] Add Layer", callback=add_layer, width=180)
                        dpg.add_button(label="[-] Remove Layer", callback=remove_layer, width=180)
                    add_helper(dpg.last_item(), "add_remove_layer")
                    dpg.add_separator()
                    dpg.add_child_window(tag="artistic_layers")
                    dpg.end() # End artistic_layers child window

                with dpg.tab(label="Scientific", tag="scientific_tab"):
                    dpg.add_text("Twisted Bilayer Hexagonal Lattice")
                    dpg.add_drag_float(label="Lattice Constant", tag="sci_const", default_value=25.0, speed=0.1, callback=mark_dirty)
                    add_helper(dpg.last_item(), "sci_const")
                    dpg.add_drag_float(label="Twist Angle", tag="sci_angle", default_value=5.0, speed=0.1, callback=mark_dirty, max_value=90.0)
                    add_helper(dpg.last_item(), "sci_angle")
            add_helper("main_tab_bar", "mode_tabs")

            dpg.add_spacer(height=10)
            dpg.add_text("◆ FINAL RENDER SETTINGS ◆", color=(0, 255, 150, 255))
            dpg.add_separator()
            
            with dpg.collapsing_header(label="✧ Output Settings", default_open=True):
                dpg.add_radio_button(["2D", "3D"], horizontal=True, default_value="3D", tag="output_dim")
                add_helper(dpg.last_item(), "output_dim")
                dpg.add_input_text(label="Output Filename", default_value="moire_output.png", tag="output_filename")
                add_helper(dpg.last_item(), "output_filename")
                dpg.add_drag_int(label="Final Resolution", default_value=1024, tag="final_resolution", speed=16, min_value=128)
                add_helper(dpg.last_item(), "final_resolution")
            
            with dpg.collapsing_header(label="✧ 3D Point Cloud Settings"):
                dpg.add_drag_int(label="Number of Points", default_value=50000, tag="anim_points", speed=1000)
                add_helper(dpg.last_item(), "3d_points")
                dpg.add_drag_int(label="Cloud Depth", default_value=100, tag="anim_depth", speed=5)
                add_helper(dpg.last_item(), "3d_depth")
                dpg.add_drag_int(label="Z-Layers", default_value=10, tag="anim_zlayers", speed=1)
                add_helper(dpg.last_item(), "3d_zlayers")
                dpg.add_drag_int(label="Marker Size", default_value=5, tag="anim_markersize", min_value=1)
                add_helper(dpg.last_item(), "3d_markersize")
                dpg.add_drag_float(label="Marker Alpha", default_value=0.7, tag="anim_alpha", min_value=0.0, max_value=1.0, speed=0.01)
                add_helper(dpg.last_item(), "3d_alpha")

            dpg.add_spacer(height=10)
            dpg.add_button(label="✨ G E N E R A T E ✨", width=-1, height=40, callback=run_generation_threaded)
            add_helper(dpg.last_item(), "generate_button")

        with dpg.child_window():
            dpg.add_text("◆ LIVE PREVIEW ◆", color=(0, 255, 150, 255))
            dpg.add_separator()
            dpg.add_image("preview_texture")

    with dpg.child_window(height=40, menubar=True):
        with dpg.menu_bar():
            dpg.add_text(app_state["status_text"], tag="status_bar_text")

# --- MAIN RENDER LOOP ---
dpg.create_viewport(title='// MOIRÉ STATIC GENERATOR v2.2 //', width=1280, height=720)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("primary_window", True)

add_layer() # Start with one default layer for the user

while dpg.is_dearpygui_running():
    update_preview()
    # Show/hide tooltips based on the checkbox
    # This is a bit of a hacky way to do it in DPG, but effective.
    if dpg.get_value("enable_helpers_checkbox"):
        dpg.enable_item("tooltip_handler")
    else:
        dpg.disable_item("tooltip_handler")

    dpg.render_dearpygui_frame()

dpg.destroy_context()