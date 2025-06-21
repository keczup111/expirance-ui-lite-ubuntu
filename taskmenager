#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk
import subprocess

def open_task_manager():
    manager = tk.Tk()
    manager.title("Menadżer Zadań")
    manager.geometry("800x550")
    manager.configure(bg="white")

    notebook = ttk.Notebook(manager)
    notebook.pack(expand=True, fill="both", padx=10, pady=10)

    # === Zakładka: PROCESY ===
    proc_tab = tk.Frame(notebook, bg="white")
    notebook.add(proc_tab, text="Procesy")

    proc_output = tk.Text(proc_tab, font=("Courier New", 9), bg="#f0f0f0", wrap="none")
    proc_output.pack(expand=True, fill="both", padx=5, pady=5)

    def update_processes():
        try:
            output = subprocess.check_output(["ps", "aux"], text=True)
            proc_output.config(state="normal")
            proc_output.delete("1.0", tk.END)
            proc_output.insert("1.0", output)
            proc_output.config(state="disabled")
        except Exception as e:
            proc_output.insert("1.0", f"Błąd:\n{e}")

    tk.Button(proc_tab, text="🔁 Odśwież", command=update_processes).pack(pady=5)
    update_processes()

    # === Zakładka: SYSTEM ===
    sys_tab = tk.Frame(notebook, bg="black")
    notebook.add(sys_tab, text="System")

    sys_output = tk.Text(sys_tab, bg="black", fg="lime", font=("Courier New", 10), wrap="none")
    sys_output.pack(expand=True, fill="both", padx=5, pady=5)

    try:
        result = subprocess.run(["neofetch", "--stdout"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output = result.stdout or result.stderr
    except Exception as e:
        output = f"Błąd:\n{e}"

    sys_output.insert("1.0", output)
    sys_output.config(state="disabled")

    # === Zamknięcie ===
    tk.Button(manager, text="Zamknij", command=manager.destroy).pack(pady=8)

    manager.mainloop()

if __name__ == "__main__":
    open_task_manager()
