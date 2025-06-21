import tkinter as tk
from tkinter import ttk, messagebox
import subprocess

def get_wifi_list():
    try:
        result = subprocess.check_output(["nmcli", "-t", "-f", "SSID", "dev", "wifi"], encoding="utf-8")
        lines = result.strip().split("\n")
        ssids = sorted(set([l.strip() for l in lines if l.strip()]))
        return ssids
    except subprocess.CalledProcessError as e:
        return [f"Błąd: {e}"]
def connect_to_wifi(ssid, password):
    try:
        result = subprocess.run(["nmcli", "dev", "wifi", "connect", ssid, "password", password],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8")
        if result.returncode == 0:
            messagebox.showinfo("Sukces", f"Połączono z siecią: {ssid}")
        else:
            messagebox.showerror("Błąd", result.stderr.strip())
    except Exception as e:
        messagebox.showerror("Błąd", str(e))
def get_current_connection():
    try:
        result = subprocess.check_output(["nmcli", "-t", "-f", "NAME,DEVICE", "connection", "show", "--active"],
                                         encoding="utf-8")
        return result.strip()
    except:
        return "Brak aktywnego połączenia"
root = tk.Tk()
root.title("Menedżer Wi-Fi")
root.geometry("400x350")

ssid_var = tk.StringVar()
password_var = tk.StringVar()

tk.Label(root, text="Dostępne sieci Wi-Fi:").pack(pady=5)
networks_combo = ttk.Combobox(root, textvariable=ssid_var, width=40)
networks_combo.pack()

def refresh_networks():
    networks_combo["values"] = get_wifi_list()
    if networks_combo["values"]:
        ssid_var.set(networks_combo["values"][0])

tk.Button(root, text="Odśwież listę", command=refresh_networks).pack(pady=5)

tk.Label(root, text="Hasło:").pack()
tk.Entry(root, textvariable=password_var, show="*").pack(pady=5)

tk.Button(root, text="Połącz", command=lambda: connect_to_wifi(ssid_var.get(), password_var.get())).pack(pady=10)

tk.Label(root, text="Obecne połączenie:").pack(pady=(20, 0))
current_label = tk.Label(root, text=get_current_connection())
current_label.pack()

def update_status():
    current_label.config(text=get_current_connection())
    root.after(5000, update_status)

update_status()
refresh_networks()

root.mainloop()
