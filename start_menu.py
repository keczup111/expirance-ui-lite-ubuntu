import tkinter as tk
import subprocess
import os

programs = {
    "Firefox": "/usr/bin/firefox",
    "Terminal": "/usr/bin/xfce4-terminal",
    "Pliki": "/usr/bin/thunar",
    "Wi-Fi": "python3 wifi_manager.py"
}

def run_app(name):
    if name in programs:
        try:
            subprocess.Popen(programs[name].split())
        except Exception as e:
            print(f"Błąd: {e}")

root = tk.Tk()
root.title("Start Menu")
root.geometry("300x400")
root.configure(bg="#222")

tk.Label(root, text="🔍 Szukaj:", fg="white", bg="#222").pack(pady=5)
search_var = tk.StringVar()
entry = tk.Entry(root, textvariable=search_var)
entry.pack(fill="x", padx=10)

frame = tk.Frame(root, bg="#222")
frame.pack(fill="both", expand=True, padx=10, pady=10)

def update_list(*args):
    for widget in frame.winfo_children():
        widget.destroy()
    query = search_var.get().lower()
    for name in programs:
        if query in name.lower():
            tk.Button(
                frame, text=name, anchor="w", width=25,
                bg="#333", fg="white", bd=0,
                command=lambda n=name: run_app(n)
            ).pack(fill="x", pady=2)
    if query and not frame.winfo_children():
        tk.Label(frame, text="(Brak wyników)", fg="#aaa", bg="#222").pack(pady=10)

search_var.trace_add("write", update_list)
update_list()

root.mainloop()
