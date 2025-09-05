import dearpygui.dearpygui as dpg
import numpy as np
import os

# Import our existing backend logic
from .patterns import generate_line_pattern, generate_hex_pattern
from .rendering import save_static_2d, save_static_3d
from .engine import normalize_pattern

# --- HELPERS TEXT ---
helper_text = {
    "enable_helpers": "Toggles these informational popups on or off.",
    "add_remove_layer": "Add or remove pattern layers that will be combined to create the final effect.",
    "layer_type": "Select the fundamental pattern for this layer.",
    "pitch_const": "For Lines: Controls the distance between lines (Pitch).\nFor Hexagonal: Controls the distance between points (Lattice Constant).",
    "layer_angle": "Controls the rotation of this specific layer in degrees.",
    "output_dim": "Choose whether to generate a flat 2D image or a 3D point cloud image.",
    "output_filename": "The name of the output file. Should end in .png.",
    "final_resolution": "The resolution (width and height) of the generated image in pixels. Higher values take longer to render.",
    "3d_points": "(3D Only) The total number of points to use in the 3D cloud. More points create a denser, more detailed cloud.",
    "3d_depth": "(3D Only) The depth of the point cloud along the Z-axis.",
    "3d_zlayers": "(3D Only) How many times the 2D pattern is stacked along the Z-axis.",
    "3d_markersize": "(3D Only) The size of each individual point in the 3D scatter plot.",
    "3d_alpha": "(3D Only) The transparency of the points. 0.0 is fully transparent, 1.0 is fully opaque.",
    "generate_button": "Generate the final static image with the current settings. This may take a moment.",
    "update_preview": "Manually update the live preview panel with the current settings."
}

# --- CONFIG & STATE ---
app_state = { "layers": [], "tooltips": [], "status_text": "Idle.", "preview_resolution": 512 }

# --- THEME & SETUP ---
def setup_theme_and_font():
    with dpg.theme() as global_theme:
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (20, 20, 30, 255))
            dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (25, 25, 35, 255))
            dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (40, 40, 50, 255))
            dpg.add_theme_color(dpg.mvThemeCol_Button, (60, 80, 120, 255))
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (80, 100, 150, 255))
            dpg.add_theme_color(dpg.mvThemeCol_Header, (60, 80, 120, 255))
            dpg.add_theme_color(dpg.mvThemeCol_HeaderHovered, (80, 100, 150, 255))
            dpg.add_theme_color(dpg.mvThemeCol_CheckMark, (0, 255, 150, 255))
            dpg.add_theme_color(dpg.mvThemeCol_SliderGrab, (0, 255, 150, 255))
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 3)
    dpg.bind_theme(global_theme)

    try:
        font_path = os.path.join("src", "moire", "assets", "fonts", "Inconsolata-Regular.ttf")
        with dpg.font_registry():
            default_font = dpg.add_font(font_path, 16)
        dpg.bind_font(default_font)
    except Exception as e:
        print(f"Could not load custom font: {e}")

# --- CORE LOGIC ---
def add_helper(widget_tag, help_key):
    tooltip_tag = dpg.generate_uuid()
    app_state["tooltips"].append(tooltip_tag)
    with dpg.tooltip(widget_tag, tag=tooltip_tag):
        dpg.add_text(helper_text[help_key], wrap=300)

def update_preview():
    res = app_state["preview_resolution"]
    shape = (res, res)
    composed_pattern = np.ones(shape, dtype=np.float32)

    for layer_id in app_state["layers"]:
        layer_type = dpg.get_value(f"type_{layer_id}")
        angle = dpg.get_value(f"angle_{layer_id}")
        pitch = dpg.get_value(f"pitch_{layer_id}")
        if layer_type == "Lines":
            pattern = generate_line_pattern(shape, pitch, angle)
        elif layer_type == "Hexagonal":
            pattern = generate_hex_pattern(shape, pitch, angle)
        composed_pattern *= pattern.astype(np.float32)
    
    normalized_pattern = normalize_pattern(composed_pattern)
    rgba_pattern = np.zeros((res, res, 4), dtype=np.float32)
    rgba_pattern[..., :3] = normalized_pattern[..., np.newaxis]
    rgba_pattern[..., 3] = 1.0
    
    dpg.set_value("preview_texture", rgba_pattern)
    dpg.set_value("status_bar_text", f"Preview updated [{res}x{res}].")

def add_layer():
    layer_id = dpg.generate_uuid()
    app_state["layers"].append(layer_id)
    with dpg.collapsing_header(label=f"Layer {len(app_state['layers'])}", default_open=True, parent="layer_controls", tag=f"header_{layer_id}"):
        dpg.add_combo(["Lines", "Hexagonal"], label="Type", width=-1, default_value="Lines", tag=f"type_{layer_id}")
        add_helper(dpg.last_item(), "layer_type")
        dpg.add_drag_float(label="Pitch / Const", tag=f"pitch_{layer_id}", default_value=10.0, speed=0.1)
        add_helper(dpg.last_item(), "pitch_const")
        dpg.add_drag_float(label="Angle", tag=f"angle_{layer_id}", default_value=0.0, speed=0.1)
        add_helper(dpg.last_item(), "layer_angle")

def remove_layer():
    if app_state["layers"]:
        layer_id = app_state["layers"].pop()
        dpg.delete_item(f"header_{layer_id}")

def generate_final_image():
    dpg.set_value("status_bar_text", "Generating final image...")
    
    class Args: pass
    args = Args()
    args.output = dpg.get_value("output_filename")
    args.resolution = dpg.get_value("final_resolution")
    args.dimension = dpg.get_value("output_dim").lower()
    args.num_points = dpg.get_value("3d_points")
    args.depth = dpg.get_value("3d_depth")
    args.z_layers = dpg.get_value("3d_zlayers")
    args.marker_size = dpg.get_value("3d_markersize")
    args.alpha = dpg.get_value("3d_alpha")
    
    args.layer = []
    for layer_id in app_state["layers"]:
        layer_type = dpg.get_value(f"type_{layer_id}").lower()
        angle = dpg.get_value(f"angle_{layer_id}")
        pitch = dpg.get_value(f"pitch_{layer_id}")
        args.layer.append(f"type={layer_type};angle={angle};pitch={pitch};const={pitch}")

    generate_pattern(args)
    dpg.set_value("status_bar_text", f"Success! Image saved as '{args.output}'")

def toggle_helpers(sender, app_data, user_data):
    """Robustly toggles helper visibility by reading the checkbox value directly."""
    is_enabled = dpg.get_value("enable_helpers_checkbox")
    for tooltip_tag in app_state["tooltips"]:
        if dpg.does_item_exist(tooltip_tag):
            dpg.configure_item(tooltip_tag, show=is_enabled)

# --- UI LAYOUT ---
dpg.create_context()
with dpg.texture_registry():
    blank = np.zeros((512, 512, 4), dtype=np.float32)
    dpg.add_raw_texture(512, 512, blank, tag="preview_texture", format=dpg.mvFormat_Float_rgba)

with dpg.window(tag="primary_window"):
    setup_theme_and_font()
    with dpg.group(horizontal=True):
        with dpg.child_window(width=400):
            dpg.add_text("MOIRÉ CONTROLS", color=(0, 255, 150, 255))
            dpg.add_separator()
            dpg.add_checkbox(label="Enable Helpers", default_value=True, callback=toggle_helpers, tag="enable_helpers_checkbox")
            add_helper(dpg.last_item(), "enable_helpers")
            dpg.add_separator()
            
            with dpg.group(horizontal=True):
                dpg.add_button(label="[+] Add Layer", callback=add_layer, width=180)
                dpg.add_button(label="[-] Remove Layer", callback=remove_layer, width=180)
            add_helper(dpg.last_item(), "add_remove_layer")
            dpg.add_separator()
            
            with dpg.child_window(tag="layer_controls"): pass
            
            dpg.add_spacer(height=10)
            dpg.add_text("FINAL RENDER SETTINGS", color=(0, 255, 150, 255))
            dpg.add_separator()
            
            with dpg.collapsing_header(label="Output Settings", default_open=True):
                dpg.add_button(label="Update Preview", width=-1, callback=update_preview)
                add_helper(dpg.last_item(), "update_preview")
                dpg.add_radio_button(["2D", "3D"], horizontal=True, default_value="3D", tag="output_dim")
                add_helper(dpg.last_item(), "output_dim")
                dpg.add_input_text(label="Output Filename", default_value="moire_output.png", tag="output_filename")
                add_helper(dpg.last_item(), "output_filename")
                dpg.add_drag_int(label="Final Resolution", default_value=1024, tag="final_resolution", speed=16)
                add_helper(dpg.last_item(), "final_resolution")
            
            with dpg.collapsing_header(label="3D Point Cloud Settings", default_open=True):
                dpg.add_drag_int(label="Number of Points", default_value=50000, tag="3d_points", speed=1000)
                add_helper(dpg.last_item(), "3d_points")
                dpg.add_drag_int(label="Cloud Depth", default_value=100, tag="3d_depth", speed=5)
                add_helper(dpg.last_item(), "3d_depth")
                dpg.add_drag_int(label="Z-Layers", default_value=10, tag="3d_zlayers", speed=1)
                add_helper(dpg.last_item(), "3d_zlayers")
                dpg.add_drag_int(label="Marker Size", default_value=5, tag="3d_markersize", min_value=1)
                add_helper(dpg.last_item(), "3d_markersize")
                dpg.add_drag_float(label="Marker Alpha", default_value=0.7, tag="3d_alpha", min_value=0.0, max_value=1.0, speed=0.01)
                add_helper(dpg.last_item(), "3d_alpha")

            dpg.add_spacer(height=10)
            dpg.add_button(label="GENERATE", width=-1, height=40, callback=generate_final_image)
            add_helper(dpg.last_item(), "generate_button")

        with dpg.child_window():
            dpg.add_text("LIVE PREVIEW", color=(0, 255, 150, 255))
            dpg.add_separator()
            dpg.add_image("preview_texture")

    with dpg.child_window(height=40, menubar=True):
        with dpg.menu_bar():
            dpg.add_text(app_state["status_text"], tag="status_bar_text")

# --- MAIN RENDER LOOP ---
dpg.create_viewport(title='MOIRÉ STATIC GENERATOR', width=1280, height=720)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("primary_window", True)

add_layer()
toggle_helpers(None, None, None) # Set initial tooltip visibility
update_preview()

while dpg.is_dearpygui_running():
    dpg.render_dearpygui_frame()

dpg.destroy_context()