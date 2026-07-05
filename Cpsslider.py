from pynput import mouse, keyboard
import threading
import time
import tkinter as tk

running = False
holding = False
exit_program = False
cps = 20

mouse_controller = mouse.Controller()

# ---------------- CLICK LOOP ----------------
def click_loop():
    global running, holding, exit_program, cps

    next_click = 0

    while not exit_program:
        if running and holding:
            now = time.perf_counter()

            if now >= next_click:
                mouse_controller.click(mouse.Button.left)
                next_click = now + (1 / max(cps, 1))
        else:
            next_click = 0
            time.sleep(0.01)


# ---------------- MOUSE ----------------
def on_click(x, y, button, pressed):
    global holding

    if button == mouse.Button.x1:  # ✅ YOUR REAL BUTTON
        holding = pressed


# ---------------- KEYBOARD ----------------
def on_press(key):
    global exit_program
    if key == keyboard.Key.f8:
        exit_program = True
        root.destroy()
        return False


# ---------------- GUI ----------------
def toggle():
    global running
    running = not running
    status.config(text=f"Status: {'ARMED' if running else 'OFF'}")
    button.config(text="Stop" if running else "Start")


def update_cps(val):
    global cps
    cps = int(val)


def close():
    global exit_program
    exit_program = True
    root.destroy()


# ---------------- UI ----------------
root = tk.Tk()
root.title("Auto Clicker")
root.geometry("300x180")
root.resizable(False, False)

status = tk.Label(root, text="Status: OFF")
status.pack(pady=10)

tk.Label(root, text="Clicks Per Second").pack()

slider = tk.Scale(root, from_=1, to=1000, orient="horizontal", command=update_cps)
slider.set(20)
slider.pack()

button = tk.Button(root, text="Start", command=toggle, width=15)
button.pack(pady=10)

root.protocol("WM_DELETE_WINDOW", close)

# ---------------- THREADS ----------------
threading.Thread(target=click_loop, daemon=True).start()

mouse.Listener(on_click=on_click).start()
keyboard.Listener(on_press=on_press).start()

root.mainloop()