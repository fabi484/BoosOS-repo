import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import time
import os
import sys
import json
import random

class BoosOSExperience:
    def __init__(self, root):
        self.root = root
        self.root.title("BoosOS Experience v3.2.8 - Desktop Environment")
        self.root.geometry("1000 Granger" if False else "1024x640")
        self.root.configure(bg="#0f172a")

        # Culori Stil Windows/Modern Retro
        self.BG_DARK = "#0f172a"
        self.PANEL_BG = "#1e293b"
        self.ACCENT = "#38bdf8"
        self.TEXT_COLOR = "#f8fafc"
        
        # Stare Start Menu
        self.start_menu_open = False

        self.setup_ui()

    def setup_ui(self):
        # --- DESKTOP AREA ---
        self.desktop = tk.Frame(self.root, bg=self.BG_DARK)
        self.desktop.pack(fill="both", expand=True)

        # Wallpaper / Logo
        title_label = tk.Label(
            self.desktop, 
            text="BoosOS", 
            font=("Consolas", 64, "bold"), 
            fg="#1e293b", 
            bg=self.BG_DARK
        )
        title_label.place(relx=0.5, rely=0.4, anchor="center")

        sub_label = tk.Label(
            self.desktop, 
            text="v3.2.8 GUI Experience", 
            font=("Consolas", 18), 
            fg="#334155", 
            bg=self.BG_DARK
        )
        sub_label.place(relx=0.5, rely=0.52, anchor="center")

        # Desktop Icons
        self.create_desktop_icon("⚙️ Gearbox", 30, 30, lambda: self.open_gearbox_window())
        self.create_desktop_icon("📝 Notes", 30, 120, lambda: self.open_notes_window())
        self.create_desktop_icon("🧮 Calc", 30, 210, lambda: self.open_calc_window())
        self.create_desktop_icon("💻 Terminal", 30, 300, lambda: self.open_terminal_window())

        # --- TASKBAR ---
        self.taskbar = tk.Frame(self.root, bg=self.PANEL_BG, height=40)
        self.taskbar.pack(side="bottom", fill="x")

        # Start Button
        self.start_btn = tk.Button(
            self.taskbar, 
            text="❖ Start", 
            font=("Segoe UI", 10, "bold"), 
            bg=self.ACCENT, 
            fg="#0f172a", 
            relief="flat", 
            command=self.toggle_start_menu
        )
        self.start_btn.pack(side="left", padx=5, pady=5)

        # Clock
        self.clock_label = tk.Label(
            self.taskbar, 
            text="", 
            font=("Consolas", 10, "bold"), 
            fg=self.TEXT_COLOR, 
            bg=self.PANEL_BG
        )
        self.clock_label.pack(side="right", padx=15)
        self.update_clock()

        # --- START MENU (Hidden by default) ---
        self.start_menu = tk.Frame(self.desktop, bg=self.PANEL_BG, highlightbackground=self.ACCENT, highlightthickness=1)
        
        start_items = [
            ("⚙️ Manual Gearbox", self.open_gearbox_window),
            ("📝 BoosNotes", self.open_notes_window),
            ("🧮 Calculator", self.open_calc_window),
            ("💻 BoosOS Terminal", self.open_terminal_window),
            ("ℹ️ BoosFetch Info", self.open_fetch_window),
            ("❌ Exit Experience", self.root.quit)
        ]

        for text, cmd in start_items:
            btn = tk.Button(
                self.start_menu, 
                text=text, 
                font=("Segoe UI", 10), 
                fg=self.TEXT_COLOR, 
                bg=self.PANEL_BG, 
                activebackground=self.ACCENT,
                activeforeground="#0f172a",
                anchor="w", 
                bd=0, 
                padx=15, 
                pady=8,
                command=lambda c=cmd: [self.toggle_start_menu(), c()]
            )
            btn.pack(fill="x")

    def create_desktop_icon(self, text, x, y, command):
        btn = tk.Button(
            self.desktop, 
            text=text, 
            font=("Segoe UI", 10, "bold"), 
            fg=self.TEXT_COLOR, 
            bg=self.BG_DARK, 
            activebackground="#1e293b",
            activeforeground=self.ACCENT,
            bd=0, 
            command=command
        )
        btn.place(x=x, y=y)

    def update_clock(self):
        current_time = time.strftime("%H:%M:%S | %d/%m/%Y")
        self.clock_label.config(text=current_time)
        self.root.after(1000, self.update_clock)

    def toggle_start_menu(self):
        if self.start_menu_open:
            self.start_menu.place_forget()
            self.start_menu_open = False
        else:
            self.start_menu.place(x=5, y=self.desktop.winfo_height() - 230, width=220)
            self.start_menu_open = True

    # --- BASE WINDOW CREATOR ---
    def create_window(self, title, width=500, height=350):
        win = tk.Toplevel(self.root)
        win.title(title)
        win.geometry(f"{width}x{height}")
        win.configure(bg=self.BG_DARK)
        return win

    # --- APPS IMPLEMENTATION ---
    def open_gearbox_window(self):
        win = self.create_window("⚙️ Manual Gearbox & Piston Simulator", 550, 420)
        
        gear_var = tk.StringVar(value="N")
        rpm_var = tk.StringVar(value="0 RPM")
        stroke_state = [0]
        anim_job = [None]

        # UI Elements
        top_frame = tk.Frame(win, bg=self.BG_DARK)
        top_frame.pack(pady=10)

        tk.Label(top_frame, text="Treaptă:", font=("Segoe UI", 11), fg=self.TEXT_COLOR, bg=self.BG_DARK).pack(side="left", padx=5)
        gear_lbl = tk.Label(top_frame, textvariable=gear_var, font=("Consolas", 14, "bold"), fg=self.ACCENT, bg=self.BG_DARK)
        gear_lbl.pack(side="left", padx=5)

        tk.Label(top_frame, text="Turație:", font=("Segoe UI", 11), fg=self.TEXT_COLOR, bg=self.BG_DARK).pack(side="left", padx=15)
        rpm_lbl = tk.Label(top_frame, textvariable=rpm_var, font=("Consolas", 14, "bold"), fg="#4ade80", bg=self.BG_DARK)
        rpm_lbl.pack(side="left", padx=5)

        canvas = tk.Canvas(win, width=300, height=220, bg="#020617", highlightthickness=0)
        canvas.pack(pady=10)

        # Controls
        ctrl_frame = tk.Frame(win, bg=self.BG_DARK)
        ctrl_frame.pack(pady=5)

        delays = {"N": 0.5, 1: 0.35, 2: 0.25, 3: 0.18, 4: 0.12, 5: 0.08, 6: 0.04}

        def draw_engine(stroke, gear):
            canvas.delete("all")
            # Cilindru
            canvas.create_rectangle(90, 20, 210, 180, outline="#ffffff", width=2)
            
            if gear == "N":
                delay = delays["N"]
            else:
                delay = delays.get(int(gear), 0.3)

            rpm = int(1 / delay * 350)
            rpm_var.set(f"{rpm} RPM")

            if stroke == 0:
                # Sus - DETONAȚIE (ROȘU)
                canvas.create_rectangle(92, 22, 208, 90, fill="#ef4444", outline="")
                canvas.create_text(150, 45, text="💥 EXPLOZIE", fill="#ffffff", font=("Consolas", 12, "bold"))
                # Piston Sus
                canvas.create_rectangle(100, 90, 200, 130, fill="#64748b", outline="#f8fafc", width=2)
                # Biela
                canvas.create_line(150, 130, 150, 190, fill="#94a3b8", width=6)
            else:
                # Jos
                canvas.create_rectangle(100, 130, 200, 170, fill="#64748b", outline="#f8fafc", width=2)
                # Biela
                canvas.create_line(150, 170, 150, 190, fill="#94a3b8", width=6)

        def animate():
            stroke_state[0] = (stroke_state[0] + 1) % 2
            draw_engine(stroke_state[0], gear_var.get())
            
            g = gear_var.get()
            delay = delays["N"] if g == "N" else delays.get(int(g), 0.3)
            anim_job[0] = win.after(int(delay * 1000), animate)

        def set_gear(g):
            gear_var.set(str(g))

        # Butoane viteze
        for g in [1, 2, 3, 4, 5, 6, "N"]:
            b = tk.Button(
                ctrl_frame, 
                text=str(g), 
                font=("Consolas", 10, "bold"), 
                width=3, 
                bg=self.PANEL_BG, 
                fg=self.ACCENT, 
                command=lambda val=g: set_gear(val)
            )
            b.pack(side="left", padx=2)

        win.protocol("WM_DELETE_WINDOW", lambda: [win.after_cancel(anim_job[0]) if anim_job[0] else None, win.destroy()])
        animate()

    def open_notes_window(self):
        win = self.create_window("📝 BoosNotes GUI", 450, 350)
        
        tk.Label(win, text="Titlu Notă:", fg=self.TEXT_COLOR, bg=self.BG_DARK).pack(anchor="w", padx=10, pady=2)
        title_entry = tk.Entry(win, bg=self.PANEL_BG, fg=self.TEXT_COLOR, insertbackground="white")
        title_entry.pack(fill="x", padx=10, pady=2)

        tk.Label(win, text="Conținut:", fg=self.TEXT_COLOR, bg=self.BG_DARK).pack(anchor="w", padx=10, pady=2)
        text_area = scrolledtext.ScrolledText(win, bg=self.PANEL_BG, fg=self.TEXT_COLOR, height=10, insertbackground="white")
        text_area.pack(fill="both", expand=True, padx=10, pady=5)

        def save_note():
            t = title_entry.get().strip()
            c = text_area.get("1.0", tk.END).strip()
            if t and c:
                messagebox.showinfo("BoosNotes", f"Nota '{t}' a fost salvată!")
            else:
                messagebox.showwarning("BoosNotes", "Completează titlul și conținutul!")

        save_btn = tk.Button(win, text="Salvează Nota", bg=self.ACCENT, fg="#0f172a", font=("Segoe UI", 9, "bold"), command=save_note)
        save_btn.pack(pady=5)

    def open_calc_window(self):
        win = self.create_window("🧮 Calculator", 300, 380)
        
        display = tk.Entry(win, font=("Consolas", 18), bg=self.PANEL_BG, fg=self.ACCENT, justify="right")
        display.pack(fill="x", padx=10, pady=10)

        buttons = [
            ('7', '8', '9', '/'),
            ('4', '5', '6', '*'),
            ('1', '2', '3', '-'),
            ('C', '0', '=', '+')
        ]

        def btn_click(char):
            if char == 'C':
                display.delete(0, tk.END)
            elif char == '=':
                try:
                    res = eval(display.get())
                    display.delete(0, tk.END)
                    display.insert(tk.END, str(res))
                except Exception:
                    display.delete(0, tk.END)
                    display.insert(tk.END, "Error")
            else:
                display.insert(tk.END, char)

        for row in buttons:
            f = tk.Frame(win, bg=self.BG_DARK)
            f.pack(fill="both", expand=True, padx=5, pady=2)
            for char in row:
                b = tk.Button(
                    f, text=char, font=("Consolas", 12, "bold"), 
                    bg=self.PANEL_BG, fg=self.TEXT_COLOR,
                    command=lambda c=char: btn_click(c)
                )
                b.pack(side="left", fill="both", expand=True, padx=2)

    def open_terminal_window(self):
        win = self.create_window("💻 BoosOS Terminal", 600, 350)
        
        term = scrolledtext.ScrolledText(win, bg="#020617", fg="#4ade80", font=("Consolas", 10), insertbackground="white")
        term.pack(fill="both", expand=True, padx=5, pady=5)
        term.insert(tk.END, "BoosOS v3.2.8 Terminal Environment\nType 'help' or commands...\n\n")

        cmd_frame = tk.Frame(win, bg=self.BG_DARK)
        cmd_frame.pack(fill="x", padx=5, pady=5)

        tk.Label(cmd_frame, text="fabi@boos:C:\\>$ ", fg=self.ACCENT, bg=self.BG_DARK, font=("Consolas", 10, "bold")).pack(side="left")
        entry = tk.Entry(cmd_frame, bg=self.PANEL_BG, fg=self.TEXT_COLOR, font=("Consolas", 10), insertbackground="white")
        entry.pack(side="left", fill="x", expand=True)

        def exec_cmd(event=None):
            c = entry.get().strip()
            term.insert(tk.END, f"fabi@boos:C:\\>$ {c}\n")
            entry.delete(0, tk.END)
            
            if c.lower() == "clear":
                term.delete("1.0", tk.END)
            elif c.lower() == "boosfetch":
                term.insert(tk.END, "OS: BoosOS v3.2.8 GUI\nUser: fabi@boos\nPlatform: " + sys.platform + "\n\n")
            elif c.lower() == "help":
                term.insert(tk.END, "Commands: help, clear, boosfetch, gearbox, notes, calc, exit\n\n")
            elif c.lower() == "gearbox":
                self.open_gearbox_window()
            elif c.lower() == "notes":
                self.open_notes_window()
            elif c.lower() == "calc":
                self.open_calc_window()
            else:
                term.insert(tk.END, f"Command '{c}' executed locally.\n\n")
            term.see(tk.END)

        entry.bind("<Return>", exec_cmd)

    def open_fetch_window(self):
        win = self.create_window("ℹ️ BoosFetch System Info", 350, 220)
        
        info = f"""
        ====================================
        OS: BoosOS v3.2.8 Experience
        User: fabi@boos
        Kernel: Python {sys.version.split()[0]}
        Platform: {sys.platform}
        Status: Active GUI Desktop
        ====================================
        """
        lbl = tk.Label(win, text=info, font=("Consolas", 10), fg=self.ACCENT, bg=self.BG_DARK, justify="left")
        lbl.pack(padx=10, pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = BoosOSExperience(root)
    root.mainloop()