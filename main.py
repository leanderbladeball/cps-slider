import sys
import os
import time
import threading
import subprocess
import requests
import tkinter as tk
from pynput import mouse, keyboard

CURRENT_VERSION = "1.0.3"
GITHUB_API = "https://api.github.com/repos/leanderbladeball/cps-slider/releases/latest"

running = False
holding = False
exit_program = False
cps = 20
mouse_controller = mouse.Controller()

def check_update():
    try:
        data = requests.get(GITHUB_API, timeout=5).json()

        latest = data.get("tag_name", "").replace("v", "")

        if not latest:
            print("Couldn't get latest version.")
            return

        if latest == CURRENT_VERSION:
            return

        print(f"Updating to {latest}...")

        if not data.get("assets"):
            print("No release asset found.")
            return

        asset_url = data["assets"][0]["browser_download_url"]

        base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))

        new_file = os.path.join(base_dir, "new_version.exe")

        with open(new_file, "wb") as f:
            f.write(requests.get(asset_url, timeout=30).content)

        updater = os.path.join(base_dir, "update.exe")
        current = os.path.abspath(sys.argv[0])

        subprocess.Popen([updater, new_file, current])

        os._exit(0)

    except Exception as e:
        print("Update check failed:", e)

def click_loop():
    global exit_program
    while not exit_program:
        if running and holding:
            mouse_controller.click(mouse.Button.left)
            time.sleep(1/max(cps,1))
        else:
            time.sleep(0.01)

def on_click(x,y,button,pressed):
    global holding
    if button == mouse.Button.x1:
        holding = pressed

def on_press(key):
    global exit_program
    if key == keyboard.Key.f8:
        exit_program = True
        root.after(0, root.destroy)
        return False

def toggle():
    global running
    running = not running
    status.config(text=f"Status: {'ARMED' if running else 'OFF'}")
    button.config(text="Stop" if running else "Start")

def update_cps(val):
    global cps
    cps = int(val)

check_update()

root = tk.Tk()
root.title("CPS Slider")
root.geometry("320x220")
root.resizable(False, False)

status = tk.Label(root,text="Status: OFF")
status.pack(pady=10)

tk.Label(root,text="Clicks Per Second").pack()

slider = tk.Scale(root,from_=1,to=1000,orient="horizontal",command=update_cps)
slider.set(20)
slider.pack(fill="x",padx=10)

button = tk.Button(root,text="Start",command=toggle,width=15)
button.pack(pady=10)

threading.Thread(target=click_loop,daemon=True).start()
mouse.Listener(on_click=on_click).start()
keyboard.Listener(on_press=on_press).start()

root.mainloop()
exit_program=True
