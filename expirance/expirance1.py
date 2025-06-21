import tkinter as tk
from tkinter import ttk, Toplevel
from PIL import Image, ImageTk
import subprocess
import time
import os
import json

CONFIG_FILE = "config.json"
open_windows = {}

programs = {
    "Firefox": "/usr/bin/firefox",
    "Terminal": "/usr/bin/xfce4-terminal",
    "Pliki": "/usr/bin/thunar",
    "Wi-Fi": "python3 wifi_manager.py"
}
def create_app_window(name):
    if name in open_windows and open_windows[name].winfo_exists():
        win = open_windows[name]
        win.deiconify()
        win.lift()
        win.state("zoomed")
        return

    win = Toplevel(root)
    win.title(name)
    win.geometry("500x300")
    win.config(bg="#1e1e1e")
    win.resizable(True, True)
    open_windows[name] = win

    title_bar = tk.Frame(win, bg="#333", height=30)
    title_bar.pack(fill="x", side="top")
    tk.Label(title_bar, text=f"🪟 {name}", bg="#333", fg="white").pack(side="left", padx=8)

    def minimize(): win.iconify()
    def toggle_size(): win.state("zoomed" if win.state() == "normal" else "normal")
    def close():
        win.destroy()
        if name in open_windows:
            del open_windows[name]

    for text, cmd in [("❌", close), ("🗖", toggle_size), ("➖", minimize)]:
        tk.Button(title_bar, text=text, bg="#333", fg="white", bd=0, command=cmd).pack(side="right")

    content = tk.Frame(win, bg="#1e1e1e")
    content.pack(expand=True, fill="both")
    tk.Label(content, text=f"{name} działa!", fg="white", bg="#1e1e1e", font=("Arial", 16)).pack(pady=30)

    if name in programs:
        try:
            subprocess.Popen(programs[name].split())
        except Exception as e:
            tk.Label(content, text=f"Błąd: {e}", fg="red", bg="#1e1e1e").pack()
def apply_wallpaper(fname):
    path = os.path.join("wallpaper", fname)
    if os.path.exists(path):
        img = Image.open(path).resize((root.winfo_width(), root.winfo_height()), Image.LANCZOS)
        bg = ImageTk.PhotoImage(img)
        wallpaper_label.config(image=bg)
        wallpaper_label.image = bg

def open_audio_panel():
    win = Toplevel(root)
    win.title("Audio")
    win.geometry("200x100")
    tk.Scale(win, from_=0, to=100, orient="horizontal").pack(pady=20)

def open_power_menu():
    win = Toplevel(root)
    win.title("Zasilanie")
    win.geometry("200x120")
    tk.Button(win, text="🔁 Restart", command=lambda: subprocess.run(["pkexec", "reboot"])).pack(pady=5)
    tk.Button(win, text="⏻ Wyłącz", command=lambda: subprocess.run(["pkexec", "poweroff"])).pack(pady=5)

def open_task_manager():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "taskmanager.py")
    if os.path.exists(path):
        subprocess.Popen(["python3", path])
    else:
        print("Nie znaleziono taskmanager.py")

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_config(data):
    with open(CONFIG_FILE, "w") as f:
        json.dump(data, f)
def open_settings():
    win = Toplevel(root)
    win.title("Ustawienia")
    win.geometry("500x400")

    res = tk.StringVar(value="1000x600")
    wall = tk.StringVar()
    notebook = ttk.Notebook(win)
    notebook.pack(expand=True, fill="both", padx=10, pady=10)

    res_frame = tk.Frame(notebook)
    notebook.add(res_frame, text="Ekran")
    tk.Label(res_frame, text="Rozdzielczość:").pack(pady=10)
    tk.OptionMenu(res_frame, res, "800x600", "1024x768", "1280x720", "1000x600").pack()

    wall_frame = tk.Frame(notebook)
    notebook.add(wall_frame, text="Tapeta")
    tk.Label(wall_frame, text="Tapeta z folderu wallpaper/:").pack(pady=10)
    files = [f for f in os.listdir("wallpaper") if f.endswith((".jpg", ".png"))]
    wall.set(files[0] if files else "")
    tk.OptionMenu(wall_frame, wall, *files).pack()

    time_frame = tk.Frame(notebook)
    notebook.add(time_frame, text="Czas")
    tk.Label(time_frame, text="Data (RRRR-MM-DD):").pack()
    date_entry = tk.Entry(time_frame)
    date_entry.pack()
    tk.Label(time_frame, text="Godzina (HH:MM):").pack()
    time_entry = tk.Entry(time_frame)
    time_entry.pack()

    def set_datetime():
        d, t = date_entry.get().strip(), time_entry.get().strip()
        if d:
            subprocess.run(["pkexec", "date", "-s", d])
        if t:
            subprocess.run(["pkexec", "date", "-s", t])
    tk.Button(time_frame, text="Zastosuj czas", command=set_datetime).pack(pady=10)

    power_frame = tk.Frame(notebook)
    notebook.add(power_frame, text="Zasilanie")
    battery_label = tk.Label(power_frame, text="Sprawdzam poziom baterii...")
    battery_label.pack(pady=20)

    def get_battery_level():
        base = "/sys/class/power_supply"
        if not os.path.exists(base):
            return "Brak informacji o zasilaniu"
        for item in os.listdir(base):
            if item.startswith("BAT"):
                cap = os.path.join(base, item, "capacity")
                try:
                    with open(cap, "r") as f:
                        return f"Poziom baterii: {f.read().strip()}%"
                except:
                    return "Nie udało się odczytać"
        return "Brak baterii wykrytej"

    def update_battery():
        battery_label.config(text=get_battery_level())
    update_battery()
    tk.Button(power_frame, text="Odśwież", command=update_battery).pack()

    def apply():
        try:
            w, h = map(int, res.get().split("x"))
            root.geometry(f"{w}x{h}")
        except:
            pass
        apply_wallpaper(wall.get())
        save_config({"resolution": res.get(), "wallpaper": wall.get()})
    tk.Button(win, text="Zastosuj", command=apply).pack(pady=10)
root = tk.Tk()
root.title("Expirance UI")
root.geometry("1000x600")

# Pasek górny
top_bar = tk.Frame(root, bg="#2c2c2c", height=30)
top_bar.pack(side="top", fill="x")
tk.Button(top_bar, text="⚙", bg="#2c2c2c", fg="white", command=open_settings).pack(side="left")
tk.Button(top_bar, text="🧠", bg="#2c2c2c", fg="white", command=open_task_manager).pack(side="left")
tk.Button(top_bar, text="⏻", bg="#2c2c2c", fg="white", command=open_power_menu).pack(side="right")

clock_label = tk.Label(top_bar, bg="#2c2c2c", fg="white")
clock_label.pack(side="right", padx=10)
def update_clock():
    clock_label.config(text=time.strftime("%H:%M:%S"))
    root.after(1000, update_clock)
update_clock()

# Pulpit i tapeta
workspace = tk.Frame(root)
workspace.pack(expand=True, fill="both")
wallpaper_label = tk.Label(workspace)
wallpaper_label.place(x=0, y=0, relwidth=1, relheight=1)
wallpaper_label.lower()

# Pasek dolny
bottom_bar = tk.Frame(root, bg="#2c2c2c", height=40)
bottom_bar.pack(side="bottom", fill="x")

left_frame = tk.Frame(bottom_bar, bg="#2c2c2c")
left_frame.pack(side="left", padx=10)

tk.Button(left_frame, text="🟦 Start", bg="#333", fg="white",
          command=lambda: subprocess.Popen(["python3", "start_menu.py"])).pack(side="left", padx=4)

for label in ["📁 Pliki", "🖥 Terminal", "🌐 Firefox", "📡 Wi-Fi"]:
    tk.Button(left_frame, text=label, bg="#444", fg="white", bd=0,
              command=lambda name=label.split()[1]: create_app_window(name)).pack(side="left", padx=4)

right_frame = tk.Frame(bottom_bar, bg="#2c2c2c")
right_frame.pack(side="right", padx=10)
tk.Button(right_frame, text="🔊", bg="#444", fg="white", command=open_audio_panel).pack(side="right", padx=3)

# Załaduj konfigurację
config = load_config()
if "resolution" in config:
    try: root.geometry(config["resolution"])
    except: pass
if "wallpaper" in config:
    apply_wallpaper(config["wallpaper"])

root.mainloop()

