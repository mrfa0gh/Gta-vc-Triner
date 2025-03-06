import tkinter as tk
from tkinter import simpledialog
import pyautogui
import pygetwindow as gw
import keyboard
import json
import threading
import atexit
from PIL import Image, ImageTk

SETTINGS_FILE = "settings.json"

def load_settings():
    try:
        with open(SETTINGS_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {str(i): "" for i in range(10)} | {f"F{i}": "" for i in range(2, 13)}

def save_settings():
    with open(SETTINGS_FILE, "w") as file:
        json.dump(cheats, file, indent=4)

def is_game_active():
    windows = gw.getWindowsWithTitle("GTA")
    return len(windows) > 0 and windows[0].isActive

def bring_game_to_foreground():
    windows = gw.getWindowsWithTitle("GTA")
    if len(windows) > 0:
        windows[0].activate()

def send_cheat(cheat):
    bring_game_to_foreground()
    if is_game_active():
        pyautogui.write(cheat)
        pyautogui.press('enter')

def on_key_press(event):
    if is_game_active() and event.name in cheats:
        send_cheat(cheats[event.name])

def setup_hotkeys():
    keyboard.unhook_all()
    keyboard.hook(on_key_press)
    threading.Thread(target=monitor_game_status, daemon=True).start()

def monitor_game_status():
    while True:
        if not is_game_active():
            keyboard.unhook_all()
            break

def open_settings():
    settings_window = tk.Toplevel(root)
    settings_window.title("الإعدادات")
    settings_window.geometry("500x500")
    settings_window.configure(bg="#222")
    
    tk.Label(settings_window, text="تعديل الأزرار والشفرات:", font=("Arial", 14, "bold"), fg="white", bg="#222").pack(pady=10)
    
    canvas = tk.Canvas(settings_window, bg="#222")
    scrollbar = tk.Scrollbar(settings_window, orient="vertical", command=canvas.yview)
    scroll_frame = tk.Frame(canvas, bg="#222")
    
    scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    def on_mouse_scroll(event):
        canvas.yview_scroll(-1 * (event.delta // 120), "units")
    
    settings_window.bind_all("<MouseWheel>", on_mouse_scroll)
    
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    def update_cheat(key, entry):
        cheats[key] = entry.get()
        save_settings()
        setup_hotkeys()
    
    for key in cheats.keys():
        row = tk.Frame(scroll_frame, bg="#222")
        row.pack(fill="x", pady=2)
        tk.Label(row, text=key, width=5, fg="white", bg="#444", font=("Arial", 10)).pack(side="left", padx=5)
        entry = tk.Entry(row, width=20, fg="white", bg="#333", font=("Arial", 10))
        entry.insert(0, cheats[key])
        entry.pack(side="left", padx=5)
        entry.bind("<FocusOut>", lambda e, k=key, en=entry: update_cheat(k, en))

def open_about():
    about_window = tk.Toplevel(root)
    about_window.title("حول البرنامج")
    about_window.geometry("400x300")
    about_window.configure(bg="#222")
    
    tk.Label(about_window, text="GTA Vice City Trainer", font=("Arial", 16, "bold"), fg="#FFD700", bg="#222").pack(pady=20)
    tk.Label(about_window, text="By Ghalwash @mrfa0gh", font=("Arial", 12), fg="white", bg="#222").pack(pady=10)

root = tk.Tk()
root.title("GTA Vice City Trainer By Ghalwash")
root.geometry("600x400")
root.configure(bg="#111")

try:
    bg_image = Image.open("back.png")
    bg_image = bg_image.resize((600, 400), Image.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)
    bg_label = tk.Label(root, image=bg_photo)
    bg_label.place(relwidth=1, relheight=1)
except:
    pass

tk.Label(root, text="GTA Vice City Trainer", font=("Arial", 18, "bold"), fg="#FFD700", bg="#111").pack(pady=10)
tk.Button(root, text="⚙️ الإعدادات", font=("Arial", 12, "bold"), bg="#555", fg="white", relief="flat", command=open_settings).pack(pady=10, padx=20, fill="x")
tk.Button(root, text="ℹ️ حول", font=("Arial", 12, "bold"), bg="#555", fg="white", relief="flat", command=open_about).pack(pady=10, padx=20, fill="x")

cheats = load_settings()
setup_hotkeys()

atexit.register(keyboard.unhook_all)  # فك جميع الاختصارات عند إغلاق البرنامج

root.mainloop()
