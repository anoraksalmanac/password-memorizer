import dearpygui.dearpygui as dpg
import multiprocessing
import time
import os
import subprocess
import shutil
import asyncio
import sys
import json
from pathlib import Path
from cryptography.fernet import Fernet
import keyring, json
import tempfile
import sys

if sys.platform == "darwin" or sys.platform == "linux" or sys.platform == "linux2":
    print("Running on macOS")
    key_file_location = Path.home() / ".config" / "key_for_memorizer.key"

if os.name == 'nt':
    temp_dir = tempfile.gettempdir()
    file_name = "key_for_memorizer.key"
    key_file_location = os.path.join(temp_dir, file_name)


json_file = "preset.json"

state = {
    "preset":"NA",
    "preset_selected":False,
    "failed":0,
    "key":0,
    "preset_count":0
}

SERVICE = "password_mem_take4"
KEY_ID  = "json_encryption_key_take4"

def get_fernet():
    key = keyring.get_password(SERVICE, KEY_ID)
    if key is None:
        key = Fernet.generate_key().decode()
        keyring.set_password(SERVICE, KEY_ID, key)
    return Fernet(key.encode())


def load_preset_json():
    f = get_fernet()
    print(f)
    if not os.path.exists(key_file_location):
        print("no key.key")
        return {}
    with open(key_file_location, "rb") as file:
        data = file.read()
        print(data)
    if not data:
        print("not data")
        return {}
    try:
        return json.loads(f.decrypt(data))
    except Exception:
        print("Warning: could not decrypt. Starting fresh.")
        return {}

def save_preset_json(data):
    f = get_fernet()
    encrypted = f.encrypt(json.dumps(data, indent=4).encode())
    with open(key_file_location, "wb") as file:  # wb, not w
        file.write(encrypted)

def add_preset(key, password):
    #data = {}
    data = load_preset_json()
    data[str(key)] = password
    save_preset_json(data)

def add_preset_callback():
    key = state["key"] + 1
    password = get_new_preset()
    add_preset(key, password)
    count = state["preset_count"]
    reset_presets(count)

def delete_preset_callback(sender, app_data, user_data):
    data = load_preset_json()
    print(data)
    del data[user_data]
    print(data)
    save_preset_json(data)
    count = state["preset_count"]
    reset_presets(count)

def reset_presets(count):
    for i in range(1, count +1):
        tag = 1000+i
        try:
            dpg.delete_item(tag)
        except:
            print("tried to delete smthing that didnt exitst")

    for i in range(1, count +1):
        tag = 2000+i
        try:
            dpg.delete_item(tag)
        except:
            print("tried to delete smthing that didnt exitst")

    i = 1000 # magic number, offset for tag ids of preset buttons
    preset_count = 0
    json_data = load_preset_json()
    for key, pswd in json_data.items():
        i += 1
        preset_count += 1
        dpg.add_button(label=pswd, callback=delete_preset_callback, user_data=key, tag=i, parent="presets_window_edit")
    state["preset_count"] = preset_count
    state["key"] = int(list(json_data)[-1])

    iiii = 2000 ##magic number, offset for tag ids of preset buttons
    preset_count = 0
    for key, pswd in json_data.items():
        iiii += 1
        preset_count += 1
        dpg.add_button(label=pswd, callback=practice_with_preset, user_data=pswd, tag=iiii, parent="presets_window_show")



# save_preset_json({"1": "testpassword"})

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.dirname(__file__), relative_path)

def get_failed(new=0):
    global failed

    if new == "clear":
        state["failed"] = 0
    else:
        state["failed"] += new
    return state["failed"]

def delete_preset(key, filename="presets.txt"):
    file_path = os.path.join(os.path.dirname(__file__), filename)
    
    with open(file_path, "r") as file:
        lines = file.readlines()
    
    with open(file_path, "w") as file:
        for line in lines:
            if not line.startswith(f"{key}:"): 
                file.write(line)

def get_file_path(filename="preset.json"):
    # Save the file in the same directory as the script
    return os.path.join(os.path.dirname(__file__), filename)

def load_presets(filename='preset.json'):
    file_path = get_file_path(filename)
    presets = {} 
    try:
        with open(file_path, "r") as file:
            for line in file:
                key, password = line.strip().split(":")
                presets[key] = password
    except FileNotFoundError:
        print(f"Warning: {filename} not found. Starting with no presets.")
    return presets

def save_preset(key, password, filename="presets.txt"):
    file_path = get_file_path(filename)
    with open(file_path, "a") as file:
        file.write(f"{key}:{password}\n")

# add_preset(2, "1234")


## dpg

def update(item="back"):
    vp_width = dpg.get_viewport_width()
    btn_width = dpg.get_item_width(item)
    
    # btn_width may still be 0 on first show — fallback to a reasonable estimate
    if btn_width == 0:
        btn_width = 60  # rough pixel width for a short label like "back"
    
    dpg.set_item_pos(item, [vp_width - btn_width - 10, 10])    

def save_preset_button(sender, app_data, user_data):
    global preset
    state["preset"] = dpg.get_value(user_data)
    dpg.hide_item("preset")
    dpg.hide_item("save_temp_pswd")
    dpg.show_item("password_attempt")
    dpg.show_item("submit_attempt")
    dpg.show_item("reset")


def get_preset_json():
    try:
        with open (json_file) as f:
            json_data = json.load(f)

        return json_data
    except FileNotFoundError:
        print("file not found - check if mem/'filename' needs to be included or not" )

def get_attempt():
    attempt = dpg.get_value("password_attempt")
    print("password attempt",dpg.get_value("password_attempt"))
    return attempt

def get_new_preset():
    password = dpg.get_value("new_password_text")
    print("password attempt",dpg.get_value("new_password_text"))
    return password

def get_preset():
    return state["preset"]

def reset():
    dpg.hide_item("password_attempt")
    dpg.hide_item("submit_attempt")
    dpg.show_item("save_temp_pswd")

    dpg.show_item("preset")

def practice_with_preset(sender, app_data, user_data):
    print(user_data)
    state["preset"] = user_data
    state["preset_selected"] = True
    dpg.hide_item("preset")
    dpg.hide_item("save_temp_pswd")
    dpg.show_item("password_attempt")
    dpg.show_item("submit_attempt")
    dpg.show_item("reset")
    dpg.hide_item("presets_window_show")
    dpg.show_item("practice_manual")
    

def is_attempt_correct():
    preset = get_preset()
    attempt = get_attempt()

    print(f"is correct? preset:{preset}, attempt:{attempt}")

    if attempt == preset:
        get_failed("clear")
        dpg.set_value("congrats_text", "you did it!")

        dpg.set_value("password_attempt", "")
    else:
        get_failed(1)
        failed = get_failed()
        dpg.set_value("congrats_text",f"try again({failed})")
        dpg.set_value("password_attempt", "")
        if failed == 5:
            dpg.set_value("congrats_text", preset)
            dpg.configure_item("password_attempt", readonly=True)
            for i in range(5, -2, -1):
                time.sleep(1)
                dpg.set_value("password_attempt", i)
            dpg.set_value("congrats_text", "")
            get_failed("clear")
            dpg.configure_item("password_attempt", readonly=False)
            dpg.set_value("password_attempt", "")



def back():

    dpg.hide_item("presets_window_show")
    dpg.hide_item("presets_window_edit")
    # dpg.hide_item("practice")
    dpg.hide_item("practice_manual")
    dpg.show_item("menu_window")
    dpg.set_primary_window("menu_window", True)


def open_presets_window_show():
    dpg.hide_item("menu_window")
    dpg.show_item("presets_window_show")
    dpg.set_primary_window("presets_window_show", True)
    count = state["preset_count"]
    reset_presets(count)


def open_presets_window_edit():
    dpg.hide_item("menu_window")
    dpg.show_item("presets_window_edit")
    dpg.set_primary_window("presets_window_edit", True)

def practice():
    dpg.hide_item("menu_window")
    dpg.show_item("practice_manual")
    dpg.set_primary_window("practice_manual", True)


