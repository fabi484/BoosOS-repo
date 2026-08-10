"""
BoosOS Experience v0.1 Beta 2 App
Compatible with BoosOS v3.2.8 (pkg/run system)
"""
import sys
import os
import time

try:
    import tkinter as tk
    from tkinter import ttk, messagebox, scrolledtext
    HAS_TKINTER = True
except ImportError:
    HAS_TKINTER = False


class BoosOSExperienceApp:
    def __init__(self, root, boos_instance=None):
        self.root = root
        self.boos = boos_instance
        self.root.title("BoosOS Experience v0.1 Beta 2")
        self.root.geometry("1024x640")
        self.root.configure(bg="#0f172a")

        self.BG_DARK = "#0f172a"
        self.PANEL_BG = "#1e293b"
        self.ACCENT = "#38bdf8"
        self.TEXT_COLOR = "#f8fafc"
        
        self.start_menu_open = False
        self.setup_ui()

    def setup_ui(self):
        # Desktop Area
        self.desktop = tk.Frame(self.root, bg=self.BG_DARK)
        self.desktop.pack(fill="both", expand=True)

        # Wallpaper Banner
        title_label = tk.Label(
            self.desktop, text="BoosOS", font=("Consolas", 64, "bold"), 
            fg="#1e293b", bg=self.BG_DARK
        )
        title_label.place(relx=0.5, rely=0.4, anchor="center")

        sub_label = tk.Label(
            self.desktop, text="Experience v0.1 Beta 2 App", font=("Consolas", 18), 
            fg="#334155", bg=self.BG_DARK
        )
        sub_label.place(relx=0.5, rely=0.52, anchor="center")

        # Desktop Icons
        self.create_desktop_icon("📝 Notes", 30, 30, self.open_notes_window)
        self.create_desktop_icon("🧮 Calc", 30, 110, self.open_calc_window)
        self.create_desktop_icon("💻 Terminal", 30, 190, self.open_terminal_window)
        self.create_desktop_icon("ℹ️ SysInfo", 30, 270, self.open_fetch_window)

        # Taskbar
        self.taskbar = tk.Frame(self.root, bg=self.PANEL_BG, height=40)
        self.taskbar.pack(side="bottom", fill="x")

        self.start_btn = tk.Button(
            self.taskbar, text="❖ Start", font=("Segoe UI", 10, "bold"), 
            bg=self.ACCENT, fg="#0f172a", relief="flat", command=self.toggle_start_menu
        )
        self.start_btn.pack(side="left", padx=5, pady=5)

        self.clock_label = tk.Label(
            self.taskbar, text="", font=("Consolas", 10, "bold"), 
            fg=self.TEXT_COLOR, bg=self.PANEL_BG
        )
        self.clock_label.pack(side="right", padx=15)
        self.update_clock()

        # Start Menu
        self.start_menu = tk.Frame(self.desktop, bg=self.PANEL_BG, highlightbackground=self.ACCENT, highlightthickness=1)
        
        start_items = [
            ("📝 BoosNotes", self.open_notes_window),
            ("🧮 Calculator", self.open_calc_window),
            ("💻 Terminal Shell", self.open_terminal_window),
            ("ℹ️ BoosFetch Info", self.open_fetch_window),
            ("❌ Close Desktop", self.root.destroy)
        ]

        for text, cmd in start_items:
            btn = tk.Button(
                self.start_menu, text=text, font=("Segoe UI", 10), 
                fg=self.TEXT_COLOR, bg=self.PANEL_BG, activebackground=self.ACCENT,
                activeforeground="#0f172a", anchor="w", bd=0, padx=15, pady=8,
                command=lambda c=cmd: [self.toggle_start_menu(), c()]
            )
            btn.pack(fill="x")

    def create_desktop_icon(self, text, x, y, command):
        btn = tk.Button(
            self.desktop, text=text, font=("Segoe UI", 10, "bold"), 
            fg=self.TEXT_COLOR, bg=self.BG_DARK, activebackground="#1e293b",
            activeforeground=self.ACCENT, bd=0, command=command
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
            self.start_menu.place(x=5, y=self.desktop.winfo_height() - 200, width=200)
            self.start_menu_open = True

    def create_window(self, title, width=500, height=350):
        win = tk.Toplevel(self.root)
        win.title(title)
        win.geometry(f"{width}x{height}")
        win.configure(bg=self.BG_DARK)
        return win

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
                if self.boos and hasattr(self.boos, "boos_notes"):
                    notes = self.boos.boos_notes.load_notes()
                    notes[t] = c
                    self.boos.boos_notes.save_notes(notes)
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
        win = self.create_window("💻 BoosOS Terminal Window", 600, 350)
        
        term = scrolledtext.ScrolledText(win, bg="#020617", fg="#4ade80", font=("Consolas", 10), insertbackground="white")
        term.pack(fill="both", expand=True, padx=5, pady=5)
        user_name = self.boos.current_user if self.boos else "guest"
        term.insert(tk.END, f"BoosOS Terminal Subsystem ({user_name}@boos)\nType 'help' for options...\n\n")

        cmd_frame = tk.Frame(win, bg=self.BG_DARK)
        cmd_frame.pack(fill="x", padx=5, pady=5)

        tk.Label(cmd_frame, text=f"{user_name}@boos:C:\\>$ ", fg=self.ACCENT, bg=self.BG_DARK, font=("Consolas", 10, "bold")).pack(side="left")
        entry = tk.Entry(cmd_frame, bg=self.PANEL_BG, fg=self.TEXT_COLOR, font=("Consolas", 10), insertbackground="white")
        entry.pack(side="left", fill="x", expand=True)

        def exec_cmd(event=None):
            c = entry.get().strip()
            term.insert(tk.END, f"{user_name}@boos:C:\\>$ {c}\n")
            entry.delete(0, tk.END)
            
            if c.lower() == "clear":
                term.delete("1.0", tk.END)
            elif c.lower() == "boosfetch":
                ver = self.boos.version if self.boos else "3.2.8"
                term.insert(tk.END, f"OS: BoosOS v{ver}\nUser: {user_name}@boos\nPlatform: {sys.platform}\n\n")
            elif c.lower() == "help":
                term.insert(tk.END, "Available commands: clear, boosfetch, help\n\n")
            else:
                term.insert(tk.END, f"Command '{c}' processed.\n\n")
            term.see(tk.END)

        entry.bind("<Return>", exec_cmd)

    def open_fetch_window(self):
        win = self.create_window("ℹ️ BoosFetch Info", 380, 220)
        ver = self.boos.version if self.boos else "3.2.8"
        user_name = self.boos.current_user if self.boos else "guest"
        
        info = f"""
====================================
OS: BoosOS v{ver}
GUI App: Experience v0.1 Beta 2
User: {user_name}@boos
Platform: {sys.platform}
Tkinter Support: Active
====================================
        """
        lbl = tk.Label(win, text=info, font=("Consolas", 10), fg=self.ACCENT, bg=self.BG_DARK, justify="left")
        lbl.pack(padx=10, pady=10)


def main():
    if not HAS_TKINTER:
        print("[GUI Error] Tkinter is not installed/supported in this environment.")
        return

    # Verificăm dacă este rulat prin BoosOS 'exec()' (unde obiectul 'boos' este injectat)
    boos_instance = globals().get("boos", None)

    try:
        root = tk.Tk()
        app = BoosOSExperienceApp(root, boos_instance)
        root.mainloop()
    except Exception as e:
        print(f"[GUI Error] Could not start BoosOS Experience GUI: {e}")
        print("[Note] Make sure you are running on a local desktop environment (Windows or Linux GUI).")


# Rulare automată atât la 'run boosexperience', cât și la execuție directă cu 'python apps/boosexperience.py'
main()