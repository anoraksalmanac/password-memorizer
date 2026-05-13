import dearpygui.dearpygui as dpg
import multiprocessing
import time
import os
from functions import*

    

preset = "NA"

width = 500
height = 350

current_working_directory = os.getcwd()
####

dpg.create_context()



dpg.create_viewport(title="memorize", width=width, height=height, resizable=False)



with dpg.font_registry():
    default_font = dpg.add_font(resource_path("OpenDyslexic-Regular.otf"), 30)
    title_font = dpg.add_font(resource_path("OpenDyslexic-Regular.otf"), 60)


dpg.bind_font(default_font)


with dpg.window(tag="menu_window", show=True, no_title_bar=True):
    title = dpg.add_text("Menu")
    dpg.add_button(label="open presets", callback=open_presets_window_show)
    dpg.add_button(label="edit presets", callback=open_presets_window_edit)
    dpg.add_button(label="practice", callback=practice)
    dpg.bind_item_font(title, title_font)



with dpg.window(tag="presets_window_show", show=False, no_title_bar=True, width=width, height=height):
    title = dpg.add_text("Select Presets")
    dpg.add_button(label="back", callback=back)
    dpg.add_spacer(height=20)

    json_data = load_preset_json()
    iii = 2000 ##magic number, offset for tag ids of preset buttons
    preset_count = 0
    for key, pswd in json_data.items():
        iii += 1
        preset_count += 1
        dpg.add_button(label=pswd, callback=practice_with_preset, user_data=pswd, tag=iii)
    try:
        state["key"] = int(list(json_data)[-1])
        # this line takes the last key in the data and saves it. this is to find where it is safe to start asigning keys to not overwrite anything
    except:
        state["key"] = 0
        print("its empty... or is it???")
    dpg.bind_item_font(title, title_font)


with dpg.window(tag="presets_window_edit", show=False, no_title_bar=True, width=width, height=height):
    title = dpg.add_text("Edit Presets")
    dpg.add_button(label="back", callback=back)
    dpg.add_spacer(height=20)
    dpg.add_input_text(label="enter new password here", tag="new_password_text", )
    dpg.set_item_width("new_password_text", 200)
    dpg.add_button(tag="add_password_button", label="add", callback=add_preset_callback)

    dpg.add_text("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    # please dont leave this in the final version
    # i beg of you, me
    # dont

    ii = 1000 ##magic number, offset for tag ids of preset buttons
    preset_count = 0
    for key, pswd in json_data.items():
        ii += 1
        preset_count += 1
        dpg.add_button(label=pswd, callback=delete_preset_callback, user_data=key, tag=ii)
        
    state["preset_count"] = preset_count

    


    dpg.bind_item_font(title, title_font)


with dpg.window(tag="practice_manual", show=False, no_title_bar=True, width=width, height=height):
    title = dpg.add_text("Practice -M")
    dpg.add_button(label="back", callback=back)
    dpg.add_spacer(height=20)

    if state["preset_selected"] == False:
        dpg.add_input_text(label="enter correct password", tag="preset")
        dpg.set_item_width("preset", 200)
        dpg.add_button(label="save", tag="save_temp_pswd", callback=save_preset_button, user_data="preset")

    dpg.add_input_text(label="enter password", tag="password_attempt")
    dpg.set_item_width("password_attempt", 200)
    dpg.add_button(label="save", tag="submit_attempt", parent="man_group", callback=is_attempt_correct)
    dpg.add_button(label="reset", tag="reset", callback=reset)
    dpg.add_text(tag="congrats_text", default_value="")
    dpg.hide_item("password_attempt")
    dpg.hide_item("submit_attempt")
    dpg.hide_item("reset")
    dpg.hide_item

    dpg.bind_item_font(title, title_font)


dpg.set_primary_window("menu_window", True)
dpg.setup_dearpygui()
dpg.show_viewport()

while dpg.is_dearpygui_running():
    dpg.render_dearpygui_frame()
    time.sleep(0.016)





dpg.destroy_context()