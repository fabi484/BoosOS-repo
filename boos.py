# BoosOS v3.2.8.1
import time
import os
import socket
import difflib
import urllib.parse
import urllib.request
import webbrowser
import random
import sys
import math
import datetime
import json

# Suport Tkinter nativ pentru BoosOS Experience GUI
try:
    import tkinter as tk
    from tkinter import ttk, messagebox, scrolledtext
    HAS_TKINTER = True
except ImportError:
    HAS_TKINTER = False

try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False

IS_WINDOWS = sys.platform.startswith("win")
if IS_WINDOWS:
    import msvcrt
else:
    import select
    import tty
    import termios

IS_PYDROID = 'pydroid' in sys.executable.lower() or os.path.exists('/data/data/ru.iiec.pydroid3')


def safe_input(prompt=""):
    try:
        return input(prompt)
    except EOFError:
        return ""


def get_key_nonblocking():
    if IS_WINDOWS:
        if msvcrt.kbhit():
            ch = msvcrt.getch()
            if ch in (b'\x00', b'\xe0'):
                ch2 = msvcrt.getch()
                if ch2 == b'H':
                    return 'w'
                elif ch2 == b'P':
                    return 's'
                elif ch2 == b'K':
                    return 'a'
                elif ch2 == b'M':
                    return 'd'
            try:
                return ch.decode('utf-8', errors='ignore').lower()
            except Exception:
                return ''
        return None
    else:
        dr, _, _ = select.select([sys.stdin], [], [], 0)
        if dr:
            ch = sys.stdin.read(1)
            if ch == '\x1b':
                dr2, _, _ = select.select([sys.stdin], [], [], 0)
                if dr2:
                    ch2 = sys.stdin.read(1)
                    if ch2 == '[':
                        dr3, _, _ = select.select([sys.stdin], [], [], 0)
                        if dr3:
                            ch3 = sys.stdin.read(1)
                            if ch3 == 'A':
                                return 'w'
                            elif ch3 == 'B':
                                return 's'
                            elif ch3 == 'D':
                                return 'a'
                            elif ch3 == 'C':
                                return 'd'
            return ch.lower()
        return None


class BoosOSExperience:
    """BoosOS Experience v0.1 Beta 2 - Native Tkinter Desktop Environment"""
    def __init__(self, root, boos_instance):
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
            self.desktop, text="Experience v0.1 Beta 2", font=("Consolas", 18), 
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
        term.insert(tk.END, "BoosOS Terminal Subsystem\nType 'help' for options...\n\n")

        cmd_frame = tk.Frame(win, bg=self.BG_DARK)
        cmd_frame.pack(fill="x", padx=5, pady=5)

        tk.Label(cmd_frame, text=f"{self.boos.current_user or 'guest'}@boos:C:\\>$ ", fg=self.ACCENT, bg=self.BG_DARK, font=("Consolas", 10, "bold")).pack(side="left")
        entry = tk.Entry(cmd_frame, bg=self.PANEL_BG, fg=self.TEXT_COLOR, font=("Consolas", 10), insertbackground="white")
        entry.pack(side="left", fill="x", expand=True)

        def exec_cmd(event=None):
            c = entry.get().strip()
            term.insert(tk.END, f"{self.boos.current_user or 'guest'}@boos:C:\\>$ {c}\n")
            entry.delete(0, tk.END)
            
            if c.lower() == "clear":
                term.delete("1.0", tk.END)
            elif c.lower() == "boosfetch":
                term.insert(tk.END, f"OS: BoosOS v{self.boos.version}\nUser: {self.boos.current_user or 'guest'}\nPlatform: {sys.platform}\n\n")
            elif c.lower() == "help":
                term.insert(tk.END, "Available commands: clear, boosfetch, help\n\n")
            else:
                term.insert(tk.END, f"Command '{c}' processed.\n\n")
            term.see(tk.END)

        entry.bind("<Return>", exec_cmd)

    def open_fetch_window(self):
        win = self.create_window("ℹ️ BoosFetch Info", 380, 220)
        
        info = f"""
====================================
OS: BoosOS v{self.boos.version}
GUI: Experience v0.1 Beta 2
User: {self.boos.current_user or 'guest'}@boos
Platform: {sys.platform}
Tkinter Native: Active
====================================
        """
        lbl = tk.Label(win, text=info, font=("Consolas", 10), fg=self.ACCENT, bg=self.BG_DARK, justify="left")
        lbl.pack(padx=10, pady=10)


class BoosNotes:
    def __init__(self, boos_instance):
        self.boos = boos_instance

    def get_notes_file(self):
        if not self.boos.user_dir or not os.path.exists(self.boos.user_dir):
            self.boos.set_active_user(self.boos.current_user or "guest")
        return os.path.join(self.boos.user_dir, "boosnotes_data.json")

    def load_notes(self):
        notes_file = self.get_notes_file()
        if os.path.exists(notes_file):
            try:
                with open(notes_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    def save_notes(self, notes):
        notes_file = self.get_notes_file()
        try:
            with open(notes_file, "w", encoding="utf-8") as f:
                json.dump(notes, f, indent=4)
        except Exception as e:
            print(f"[Notes Error] Could not save notes: {e}")

    def run(self):
        notes = self.load_notes()
        while True:
            print("\n--- BoosNotes ---")
            print("1. View all notes")
            print("2. Add / Edit a note")
            print("3. Delete a note")
            print("4. Back to BoosOS")
            
            choice = safe_input("Choose an option: ").strip()
            
            if choice == "1":
                if not notes:
                    print("\n[No notes saved yet.]")
                else:
                    print("\n--- Your Notes ---")
                    for title, content in notes.items():
                        print(f" * {title}: {content}")
            elif choice == "2":
                title = safe_input("Note title: ").strip()
                if title:
                    content = safe_input("Content: ").strip()
                    notes[title] = content
                    self.save_notes(notes)
                    print("[Note saved successfully!]")
            elif choice == "3":
                title = safe_input("Title to delete: ").strip()
                if title in notes:
                    del notes[title]
                    self.save_notes(notes)
                    print("[Note deleted!]")
                else:
                    print("[Note not found.]")
            elif choice == "4":
                break


class BoosOS:
    def __init__(self):
        self.version = "3.2.8.1"
        self.running = True
        self.save_dir = "user_saves"
        self.repo_url = "https://raw.githubusercontent.com/fabi484/BoosOS-repo/main"
        self.users_file = "users.json"
        self.current_user = None
        self.user_dir = None
        
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)
            
        self.set_active_user("guest")
        self.boos_notes = BoosNotes(self)
        self.commands = [
            "sysinfo", "ping", "calc", "clear", "exit", 
            "help", "snake", "tictactoe", "top", "login", 
            "register", "whoami", "pkg", "run", "notes", "boosfetch", "boosexperience"
        ]

    def clear_screen(self):
        os.system("cls" if IS_WINDOWS else "clear")

    def get_suggestion(self, cmd):
        apps_dir = self.get_apps_dir()
        installed_apps = []
        if os.path.exists(apps_dir):
            installed_apps = [f[:-3] for f in os.listdir(apps_dir) if f.endswith(".py")]
            
        all_valid = self.commands + installed_apps
        matches = difflib.get_close_matches(cmd, all_valid, n=1, cutoff=0.5)
        return matches[0] if matches else None

    def set_active_user(self, username):
        self.current_user = username
        self.user_dir = os.path.abspath(os.path.join(self.save_dir, username))
        if not os.path.exists(self.user_dir):
            os.makedirs(self.user_dir)

    def get_apps_dir(self):
        apps_path = os.path.join(self.user_dir, "installed_apps")
        if not os.path.exists(apps_path):
            os.makedirs(apps_path)
        return apps_path

    def launch_boosexperience(self):
        if not HAS_TKINTER:
            print("[Error] Tkinter/GUI support is not installed or available in this Python environment.")
            return

        print("[System] Initializing BoosOS Experience v0.1 Beta 2 GUI...")
        try:
            root = tk.Tk()
            app = BoosOSExperience(root, self)
            root.mainloop()
            print("[System] Returned from BoosOS Experience Desktop.")
        except Exception as e:
            print(f"[GUI Error] Could not start Experience desktop: {e}")
            print("[Info] Make sure you are running on a machine with an active graphical display (Windows/Linux Desktop).")

    def show_help(self):
        print("\n--- BoosOS Help ---")
        print(f"System Commands : {', '.join(sorted(self.commands))}")
        
        apps_dir = self.get_apps_dir()
        if os.path.exists(apps_dir):
            installed = [f[:-3] for f in os.listdir(apps_dir) if f.endswith(".py")]
            if installed:
                print(f"Installed Apps  : {', '.join(sorted(installed))}")
        print()

    def load_users(self):
        if os.path.exists(self.users_file):
            try:
                with open(self.users_file, "r") as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    def register(self):
        users = self.load_users()
        u = safe_input("Create Username: ").strip()
        p = safe_input("Create Password: ").strip()
        if not u or not p:
            print("[Error] Username and password cannot be empty.")
            return
        if u in users:
            print("[Error] Username already exists.")
            return
        users[u] = p
        try:
            with open(self.users_file, "w") as f:
                json.dump(users, f, indent=4)
            self.set_active_user(u)
            print(f"[System] Registered and logged in as '{u}'.")
        except Exception as e:
            print(f"[Error] Could not save user data: {e}")

    def login(self):
        users = self.load_users()
        u = safe_input("Username: ").strip()
        p = safe_input("Password: ").strip()
        if users.get(u) == p:
            self.set_active_user(u)
            print(f"Welcome back, {u}!")
        else:
            print("[Error] Invalid credentials.")

    def boos_fetch(self):
        print("\n====================================")
        print(f"OS: BoosOS v{self.version}")
        print(f"User: {self.current_user or 'guest'}@boos")
        print(f"Time: {time.strftime('%H:%M:%S')}")
        print(f"Platform: {sys.platform}")
        if HAS_PSUTIL:
            print(f"CPU Usage: {psutil.cpu_percent()}%")
            print(f"RAM Usage: {psutil.virtual_memory().percent}%")
        print("====================================\n")

    def ping(self, args):
        host = args[0] if args else "google.com"
        print(f"Pinging {host}...")
        try:
            start_time = time.time()
            socket.gethostbyname(host)
            latency = round((time.time() - start_time) * 1000, 2)
            print(f"Reply from {host}: time={latency}ms")
        except Exception:
            print(f"Failed to reach {host}.")

    def calculator(self, args):
        if not args:
            expr = safe_input("Enter expression (e.g., 2 + 2): ").strip()
        else:
            expr = " ".join(args)
        try:
            allowed = "0123456789+-*/(). "
            if all(c in allowed for c in expr):
                result = eval(expr)
                print(f"Result: {result}")
            else:
                print("[Error] Invalid characters in math expression.")
        except Exception as e:
            print(f"[Calc Error] {e}")

    def top_process(self):
        print("\n--- Task Manager / System Monitor ---")
        if HAS_PSUTIL:
            print(f"CPU Usage    : {psutil.cpu_percent()}%")
            mem = psutil.virtual_memory()
            print(f"RAM Usage    : {mem.percent}% ({round(mem.used/1024**2, 1)}MB / {round(mem.total/1024**2, 1)}MB)")
            print("\nTop 5 Processes by Memory:")
            procs = []
            for p in psutil.process_iter(['pid', 'name', 'memory_percent']):
                try:
                    procs.append(p.info)
                except Exception:
                    pass
            procs = sorted(procs, key=lambda x: x['memory_percent'] or 0, reverse=True)[:5]
            for p in procs:
                print(f" PID {p['pid']:<6} | {p['name']:<20} | Mem: {round(p['memory_percent'] or 0, 2)}%")
        else:
            print("[Warning] 'psutil' module is not installed. Limited info available.")
            print(f"Python Executable: {sys.executable}")
            print(f"Platform: {sys.platform}")

    def play_tictactoe(self):
        board = [" " for _ in range(9)]

        def print_board():
            print("\n")
            print(f" {board[0]} | {board[1]} | {board[2]} ")
            print("---|---|---")
            print(f" {board[3]} | {board[4]} | {board[5]} ")
            print("---|---|---")
            print(f" {board[6]} | {board[7]} | {board[8]} ")
            print("\n")

        def check_winner(b, mark):
            win_conds = [
                (0,1,2), (3,4,5), (6,7,8),
                (0,3,6), (1,4,7), (2,5,8),
                (0,4,8), (2,4,6)
            ]
            return any(b[x] == b[y] == b[z] == mark for x, y, z in win_conds)

        current_player = "X"
        for _ in range(9):
            print_board()
            if current_player == "X":
                move = safe_input(f"Player {current_player} (1-9): ").strip()
                if not move.isdigit() or int(move) not in range(1, 10):
                    print("Invalid input! Try 1-9.")
                    continue
                idx = int(move) - 1
                if board[idx] != " ":
                    print("Spot taken!")
                    continue
                board[idx] = "X"
            else:
                available = [i for i, x in enumerate(board) if x == " "]
                idx = random.choice(available)
                board[idx] = "O"
                print(f"BoosOS Bot placed 'O' at spot {idx + 1}")

            if check_winner(board, current_player):
                print_board()
                print(f"Player {current_player} wins!")
                return
            current_player = "O" if current_player == "X" else "X"

        print_board()
        print("It's a draw!")

    def play_snake(self):
        print("\nStarting Snake Game... (Use W/A/S/D to change direction, Q to quit)")
        width = 15
        height = 10
        snake = [(5, 5), (5, 4), (5, 3)]
        direction = 'd'
        food = (random.randint(1, height - 2), random.randint(1, width - 2))
        score = 0

        old_settings = None
        if not IS_WINDOWS:
            try:
                fd = sys.stdin.fileno()
                old_settings = termios.tcgetattr(fd)
                tty.setcbreak(fd)
            except Exception:
                pass

        try:
            while True:
                self.clear_screen()
                print(f"--- BoosSnake | Score: {score} ---")
                
                for r in range(height):
                    line = ""
                    for c in range(width):
                        if r == 0 or r == height - 1 or c == 0 or c == width - 1:
                            line += "#"
                        elif (r, c) == snake[0]:
                            line += "O"
                        elif (r, c) in snake[1:]:
                            line += "o"
                        elif (r, c) == food:
                            line += "*"
                        else:
                            line += " "
                    print(line)

                time.sleep(0.2)
                key = get_key_nonblocking()
                if key == 'q':
                    break
                if key in ['w', 'a', 's', 'd']:
                    opposite = {'w': 's', 's': 'w', 'a': 'd', 'd': 'a'}
                    if key != opposite.get(direction):
                        direction = key

                head_r, head_c = snake[0]
                if direction == 'w':
                    head_r -= 1
                elif direction == 's':
                    head_r += 1
                elif direction == 'a':
                    head_c -= 1
                elif direction == 'd':
                    head_c += 1

                new_head = (head_r, head_c)

                if (head_r <= 0 or head_r >= height - 1 or 
                    head_c <= 0 or head_c >= width - 1 or 
                    new_head in snake):
                    print(f"\nGame Over! Final Score: {score}")
                    time.sleep(2)
                    break

                snake.insert(0, new_head)
                if new_head == food:
                    score += 10
                    food = (random.randint(1, height - 2), random.randint(1, width - 2))
                else:
                    snake.pop()

        finally:
            if not IS_WINDOWS and old_settings:
                try:
                    termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, old_settings)
                except Exception:
                    pass

    def pkg_manager(self, args):
        if not args:
            print("[PKG] Usage: pkg <install|uninstall|list|update> [app_name|os|all]")
            return

        action = args[0].lower()
        apps_dir = self.get_apps_dir()

        if action == "list":
            print("\n--- Available Remote / Local Apps ---")
            if os.path.exists(apps_dir):
                installed = [f[:-3] for f in os.listdir(apps_dir) if f.endswith(".py")]
                print("Installed Local Apps:", ", ".join(installed) if installed else "None")
            print("Repository URL:", self.repo_url)

        elif action == "install":
            if len(args) < 2:
                print("[PKG Error] Specify app name to install.")
                return
            app_name = args[1].lower()
            url = f"{self.repo_url}/apps/{app_name}.py"
            print(f"[PKG] Fetching {url}...")
            try:
                req = urllib.request.Request(url, headers={'Cache-Control': 'no-cache'})
                with urllib.request.urlopen(req, timeout=5) as resp:
                    code = resp.read().decode('utf-8')
                    dest_path = os.path.join(apps_dir, f"{app_name}.py")
                    with open(dest_path, "w", encoding="utf-8") as f:
                        f.write(code)
                    print(f"[PKG] Installed '{app_name}' successfully!")
            except Exception as e:
                print(f"[PKG Error] Failed to download package: {e}")

        elif action == "uninstall":
            if len(args) < 2:
                print("[PKG Error] Specify app name to uninstall.")
                return
            app_name = args[1].lower()
            target_path = os.path.join(apps_dir, f"{app_name}.py")
            if os.path.exists(target_path):
                os.remove(target_path)
                print(f"[PKG] App '{app_name}' uninstalled.")
            else:
                print(f"[PKG Error] App '{app_name}' is not installed.")

        elif action == "update":
            target = args[1].lower() if len(args) > 1 else "os"
            
            # --- UPDATE SYSTEM OS ---
            if target in ["os", "system", "all"]:
                print("[PKG] Checking for BoosOS core updates...")
                try:
                    url = f"{self.repo_url}/boos.py?cb={int(time.time())}"
                    req = urllib.request.Request(url, headers={'Cache-Control': 'no-cache'})
                    with urllib.request.urlopen(req, timeout=5) as resp:
                        new_code = resp.read().decode('utf-8')
                        if "class BoosOS" in new_code:
                            current_script = os.path.realpath(__file__)
                            with open(current_script, "w", encoding="utf-8") as f:
                                f.write(new_code)
                            print("[PKG] BoosOS system core updated successfully!")
                        else:
                            print("[PKG Error] Valid system code not found at repository source.")
                except Exception as e:
                    print(f"[PKG Error] Could not update system: {e}")

            # --- UPDATE INSTALLED APPS ---
            if target in ["all", "apps"]:
                print("[PKG] Updating all installed apps...")
                if os.path.exists(apps_dir):
                    installed = [f[:-3] for f in os.listdir(apps_dir) if f.endswith(".py")]
                    for app_name in installed:
                        url = f"{self.repo_url}/apps/{app_name}.py?cb={int(time.time())}"
                        try:
                            req = urllib.request.Request(url, headers={'Cache-Control': 'no-cache'})
                            with urllib.request.urlopen(req, timeout=5) as resp:
                                code = resp.read().decode('utf-8')
                                dest_path = os.path.join(apps_dir, f"{app_name}.py")
                                with open(dest_path, "w", encoding="utf-8") as f:
                                    f.write(code)
                                print(f"  * Updated '{app_name}'")
                        except Exception as e:
                            print(f"  * Failed to update '{app_name}': {e}")
            
            # --- UPDATE SPECIFIC APP ---
            elif target not in ["os", "system", "all", "apps"]:
                app_name = target
                url = f"{self.repo_url}/apps/{app_name}.py?cb={int(time.time())}"
                print(f"[PKG] Updating app '{app_name}'...")
                try:
                    req = urllib.request.Request(url, headers={'Cache-Control': 'no-cache'})
                    with urllib.request.urlopen(req, timeout=5) as resp:
                        code = resp.read().decode('utf-8')
                        dest_path = os.path.join(apps_dir, f"{app_name}.py")
                        with open(dest_path, "w", encoding="utf-8") as f:
                            f.write(code)
                        print(f"[PKG] Updated '{app_name}' successfully!")
                except Exception as e:
                    print(f"[PKG Error] Failed to update '{app_name}': {e}")

    def run_app(self, app_name):
        app_path = os.path.join(self.get_apps_dir(), f"{app_name}.py")
        if os.path.exists(app_path):
            try:
                print(f"[System] Running '{app_name}'...\n")
                with open(app_path, "r", encoding="utf-8") as f:
                    code = f.read()
                exec(code, {"__builtins__": __builtins__, "os": os, "sys": sys, "boos": self})
            except Exception as e:
                print(f"[App Execution Error] {e}")
        else:
            print(f"[Error] App '{app_name}' not found. Use 'pkg install {app_name}' to get it.")

    def show_sysinfo(self):
        print(f"\n--- BoosOS System Info ---")
        print(f"OS Version  : {self.version}")
        print(f"Active User : {self.current_user or 'guest'}")
        print(f"User Path   : {self.user_dir}")
        print(f"Python      : {sys.version.split()[0]}")
        print(f"System Time : {time.strftime('%Y-%m-%d %H:%M:%S')}\n")

    def run(self):
        self.clear_screen()
        print(f"==================================================")
        print(f"           Welcome to BoosOS v{self.version}")
        print(f"  Type 'help' for commands or 'exit' to quit.  ")
        print(f"==================================================\n")

        while self.running:
            try:
                prompt = f"{self.current_user or 'guest'}@boos:C:\\>$ "
                user_input = safe_input(prompt)
                ui = user_input.strip().split()
                if not ui:
                    continue

                c = ui[0].lower()
                args = ui[1:]

                actions = {
                    "sysinfo": self.show_sysinfo,
                    "clear": self.clear_screen,
                    "exit": lambda: setattr(self, 'running', False),
                    "help": self.show_help,
                    "pkg": lambda: self.pkg_manager(args),
                    "notes": self.boos_notes.run,
                    "boosfetch": self.boos_fetch,
                    "boosexperience": self.launch_boosexperience,
                    "ping": lambda: self.ping(args),
                    "calc": lambda: self.calculator(args),
                    "top": self.top_process,
                    "tictactoe": self.play_tictactoe,
                    "snake": self.play_snake,
                    "register": self.register,
                    "login": self.login,
                    "whoami": lambda: print(f"Logged in as: {self.current_user or 'guest'}")
                }

                if c in actions:
                    actions[c]()
                elif c == "run" and args:
                    self.run_app(args[0])
                elif os.path.exists(os.path.join(self.get_apps_dir(), f"{c}.py")):
                    self.run_app(c)
                else:
                    sugg = self.get_suggestion(c)
                    if sugg:
                        print(f"Command '{c}' not found. Did you mean '{sugg}'?")
                    else:
                        print(f"Command '{c}' not found. Type 'help' for available commands.")

            except KeyboardInterrupt:
                print("\n[Use 'exit' command to shutdown cleanly]")
            except EOFError:
                break


if __name__ == "__main__":
    BoosOS().run()