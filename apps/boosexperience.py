try:
    import tkinter as tk
    from tkinter import scrolledtext, messagebox
except Exception as e:
    print("[FATAL] Tkinter is not available:", e)
    print()
    print("Fix ideas:")
    print("  Windows: reinstall Python and enable Tcl/Tk")
    print("  Linux: sudo apt install python3-tk")
    print("  Termux: pkg install python-tkinter")
    print("  Pydroid3: install Tkinter from Quick install")
    raise SystemExit(1)

import builtins
import sys
import os
import threading
import time
import random
import json
import socket
import difflib
import urllib.request
import math
import datetime


# =============================================================================
# STREAM REDIRECTOR
# =============================================================================
class Stream:
    def __init__(self, terminal, tag="stdout"):
        self.terminal = terminal
        self.tag = tag

    def write(self, text):
        if not text:
            return 0
        self.terminal._write(text, self.tag)
        return len(text)

    def flush(self):
        pass


# =============================================================================
# SELF-CONTAINED BOOS CORE
# =============================================================================
class BoosCore:
    def __init__(self):
        self.version = "3.2.8.1-beta8.2"
        self.save_dir = "user_saves"
        self.users_file = "users.json"
        self.repo_url = "https://raw.githubusercontent.com/fabi484/BoosOS-repo/main"
        self.current_user = None
        self.user_dir = None
        self.commands = [
            "help", "sysinfo", "whoami", "clear", "exit",
            "calc", "ping", "pkg", "run", "boosfetch"
        ]

        os.makedirs(self.save_dir, exist_ok=True)
        self.set_active_user("guest")

    def set_active_user(self, username):
        self.current_user = username
        self.user_dir = os.path.abspath(os.path.join(self.save_dir, username))
        os.makedirs(self.user_dir, exist_ok=True)

    def get_apps_dir(self):
        apps_dir = os.path.join(self.user_dir, "installed_apps")
        os.makedirs(apps_dir, exist_ok=True)
        return apps_dir

    def load_users(self):
        if os.path.exists(self.users_file):
            try:
                with open(self.users_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    def save_users(self, users):
        with open(self.users_file, "w", encoding="utf-8") as f:
            json.dump(users, f, indent=4)

    def check_user(self, username, password):
        users = self.load_users()
        return users.get(username) == password

    def add_user(self, username, password):
        users = self.load_users()
        if username in users:
            return False
        users[username] = password
        self.save_users(users)
        return True

    def _installed_apps(self):
        apps_dir = self.get_apps_dir()
        try:
            return sorted([f[:-3] for f in os.listdir(apps_dir) if f.endswith(".py")])
        except Exception:
            return []

    def _safe_app_name(self, app_name):
        name = os.path.basename(str(app_name).strip().lower())
        if name.endswith(".py"):
            name = name[:-3]

        allowed = "abcdefghijklmnopqrstuvwxyz0123456789_-"
        if not name or any(ch not in allowed for ch in name):
            return None
        return name

    def app_exists(self, app_name):
        safe = self._safe_app_name(app_name)
        if not safe:
            return False
        return os.path.exists(os.path.join(self.get_apps_dir(), f"{safe}.py"))

    def get_suggestion(self, cmd):
        all_valid = self.commands + self._installed_apps()
        matches = difflib.get_close_matches(cmd, all_valid, n=1, cutoff=0.5)
        return matches[0] if matches else None

    def show_help(self):
        print("\n--- BoosExperience Terminal Help ---")
        print("Commands:", ", ".join(sorted(self.commands)))

        apps = self._installed_apps()
        if apps:
            print("Installed apps:", ", ".join(apps))
        else:
            print("Installed apps: None")

        print("\nExamples:")
        print("  pkg list")
        print("  pkg install snake")
        print("  run snake")
        print("  calc 2 + 2")
        print("  ping google.com")
        print("  sysinfo")
        print("  clear")
        print("  exit")
        print()

    def show_sysinfo(self):
        print("\n--- BoosOS System Info ---")
        print(f"Experience    : BoosExperience 0.1 Beta 8.2")
        print(f"Core Version  : {self.version}")
        print(f"Active User   : {self.current_user or 'guest'}")
        print(f"User Path     : {self.user_dir}")
        print(f"Python        : {sys.version.split()[0]}")
        print(f"Platform      : {sys.platform}")
        print(f"System Time   : {time.strftime('%Y-%m-%d %H:%M:%S')}")
        print()

    def boos_fetch(self):
        print("\n====================================")
        print(f"OS: BoosOS {self.version}")
        print(f"Experience: BoosExperience 0.1 Beta 8.2")
        print(f"User: {self.current_user or 'guest'}@boos")
        print(f"Time: {time.strftime('%H:%M:%S')}")
        print(f"Platform: {sys.platform}")
        print("====================================\n")

    def ping(self, args):
        host = args[0] if args else "google.com"
        print(f"Pinging {host}...")

        try:
            start = time.time()
            socket.gethostbyname(host)
            latency = round((time.time() - start) * 1000, 2)
            print(f"Reply from {host}: time={latency}ms")
        except Exception:
            print(f"Failed to reach {host}.")

    def calculator(self, args):
        if not args:
            expr = input("Enter expression (example: 2 + 2): ").strip()
        else:
            expr = " ".join(args)

        try:
            allowed = "0123456789+-*/(). "
            if all(c in allowed for c in expr):
                result = eval(expr)
                print(f"Result: {result}")
            else:
                print("[Calc Error] Invalid characters.")
        except Exception as e:
            print(f"[Calc Error] {e}")

    def _download_app(self, app_name, overwrite=True):
        safe = self._safe_app_name(app_name)
        if not safe:
            print("[PKG Error] Invalid app name.")
            return False

        dest_path = os.path.join(self.get_apps_dir(), f"{safe}.py")
        url = f"{self.repo_url.rstrip('/')}/apps/{safe}.py?cb={int(time.time())}"

        print(f"[PKG] Fetching {url}...")

        try:
            req = urllib.request.Request(
                url,
                headers={
                    "Cache-Control": "no-cache",
                    "User-Agent": "BoosExperience"
                }
            )

            with urllib.request.urlopen(req, timeout=10) as resp:
                code = resp.read().decode("utf-8")

            if not code.strip():
                print("[PKG Error] Downloaded file is empty.")
                return False

            existed = os.path.exists(dest_path)

            with open(dest_path, "w", encoding="utf-8") as f:
                f.write(code)

            if existed and overwrite:
                print(f"[PKG] Updated '{safe}' successfully!")
            else:
                print(f"[PKG] Installed '{safe}' successfully!")

            return True

        except Exception as e:
            print(f"[PKG Error] Failed to download '{safe}': {e}")
            return False

    def pkg_manager(self, args):
        if not args:
            print("[PKG] Usage:")
            print("  pkg list")
            print("  pkg install <app>")
            print("  pkg uninstall <app>")
            print("  pkg update all")
            print("  pkg update <app>")
            return

        action = args[0].lower()

        if action == "upgrade":
            action = "update"

        apps_dir = self.get_apps_dir()

        if action == "list":
            print("\n--- Package Manager ---")
            installed = self._installed_apps()
            print("Installed apps:", ", ".join(installed) if installed else "None")
            print("Repository:", self.repo_url)
            print()

        elif action == "install":
            if len(args) < 2:
                print("[PKG Error] Usage: pkg install <app_name>")
                return
            self._download_app(args[1], overwrite=True)

        elif action == "uninstall":
            if len(args) < 2:
                print("[PKG Error] Usage: pkg uninstall <app_name>")
                return

            safe = self._safe_app_name(args[1])
            if not safe:
                print("[PKG Error] Invalid app name.")
                return

            target = os.path.join(apps_dir, f"{safe}.py")
            if os.path.exists(target):
                os.remove(target)
                print(f"[PKG] Uninstalled '{safe}'.")
            else:
                print(f"[PKG Error] App '{safe}' is not installed.")

        elif action == "update":
            target = args[1].lower() if len(args) > 1 else "apps"

            if target in ["os", "system", "core"]:
                print("[PKG] OS updates are disabled in BoosExperience standalone.")
                return

            if target in ["all", "apps", "installed"]:
                installed = self._installed_apps()
                if not installed:
                    print("[PKG] No installed apps to update.")
                    return

                print(f"[PKG] Updating {len(installed)} installed app(s)...")

                ok = 0
                fail = 0

                for app in installed:
                    if self._download_app(app, overwrite=True):
                        ok += 1
                    else:
                        fail += 1

                print(f"[PKG] Update summary -> OK: {ok}, Failed: {fail}")
            else:
                self._download_app(target, overwrite=True)

        else:
            print(f"[PKG Error] Unknown action '{action}'.")

    def run_app(self, app_name):
        safe = self._safe_app_name(app_name)
        if not safe:
            print("[App Error] Invalid app name.")
            return

        app_path = os.path.join(self.get_apps_dir(), f"{safe}.py")

        if not os.path.exists(app_path):
            print(f"[App Error] App '{safe}' not found.")
            print(f"Try: pkg install {safe}")
            return

        try:
            print(f"[System] Running '{safe}'...\n")

            with open(app_path, "r", encoding="utf-8") as f:
                code = f.read()

            exec(
                code,
                {
                    "__builtins__": builtins,
                    "__name__": "__main__",
                    "os": os,
                    "sys": sys,
                    "time": time,
                    "random": random,
                    "json": json,
                    "math": math,
                    "datetime": datetime,
                    "socket": socket,
                    "urllib": urllib,
                    "tk": tk,
                    "messagebox": messagebox,
                    "boos": self
                }
            )

        except Exception as e:
            print(f"[App Execution Error] {e}")


# =============================================================================
# TERMINAL WINDOW
# =============================================================================
class TerminalWindow(tk.Toplevel):
    def __init__(self, master, core, user, title=None, auto_command=None):
        super().__init__(master)

        self.core = core
        self.user = user

        self.title(title or f"Terminal - {user}@boos")
        self.geometry("720x460")
        self.configure(bg="#0c0c0c")

        self.history = []
        self.history_index = -1

        self._waiting_input = False
        self._input_event = None
        self._input_value = ""

        self.output = scrolledtext.ScrolledText(
            self,
            wrap="word",
            bg="#0c0c0c",
            fg="#d4d4d4",
            insertbackground="#d4d4d4",
            font=("Consolas", 11),
            state="disabled",
            borderwidth=0,
            highlightthickness=0
        )
        self.output.pack(fill="both", expand=True)
        self.output.tag_configure("stdout", foreground="#d4d4d4")
        self.output.tag_configure("stderr", foreground="#ff6b6b")

        entry_frame = tk.Frame(self, bg="#0c0c0c")
        entry_frame.pack(fill="x")

        self.prompt_label = tk.Label(
            entry_frame,
            text=f"{user}@boos:> ",
            bg="#0c0c0c",
            fg="#007acc",
            font=("Consolas", 11)
        )
        self.prompt_label.pack(side="left")

        self.cmd_entry = tk.Entry(
            entry_frame,
            bg="#0c0c0c",
            fg="#d4d4d4",
            insertbackground="#d4d4d4",
            font=("Consolas", 11),
            borderwidth=0,
            highlightthickness=0
        )
        self.cmd_entry.pack(side="left", fill="x", expand=True)
        self.cmd_entry.bind("<Return>", self._on_enter)
        self.cmd_entry.bind("<Up>", self._history_up)
        self.cmd_entry.bind("<Down>", self._history_down)

        self.protocol("WM_DELETE_WINDOW", self._on_close)
        self.cmd_entry.focus_set()

        self._write(f"BoosExperience Terminal | User: {user}\n")
        self._write("Type 'help' for commands.\n\n")

        if auto_command:
            self.after(200, lambda: self._run_command(auto_command, echo=True))

    def _write(self, text, tag="stdout"):
        def do_insert():
            try:
                self.output.configure(state="normal")
                self.output.insert("end", text, tag)
                self.output.see("end")
                self.output.configure(state="disabled")
            except Exception:
                pass

        try:
            self.after(0, do_insert)
        except Exception:
            pass

    def _clear(self):
        try:
            self.output.configure(state="normal")
            self.output.delete("1.0", "end")
            self.output.configure(state="disabled")
        except Exception:
            pass

    def _on_close(self):
        if self._waiting_input and self._input_event:
            self._input_value = ""
            self._input_event.set()

        self.destroy()

    def _gui_input(self, prompt=""):
        if prompt:
            self._write(prompt)

        self._input_value = ""
        self._input_event = threading.Event()

        def enter_input_mode():
            self._waiting_input = True
            self.cmd_entry.delete(0, "end")
            self.cmd_entry.focus_set()

        self.after(0, enter_input_mode)

        self._input_event.wait(timeout=600)
        self._waiting_input = False

        return self._input_value

    def _on_enter(self, event=None):
        text = self.cmd_entry.get().strip()
        self.cmd_entry.delete(0, "end")

        if self._waiting_input:
            self._write(text + "\n")
            self._input_value = text
            self._waiting_input = False

            if self._input_event:
                self._input_event.set()

            return

        self._run_command(text, echo=True)

    def _run_command(self, cmd, echo=True):
        cmd = cmd.strip()

        if not cmd:
            return

        self.history.append(cmd)
        self.history_index = len(self.history)

        if echo:
            self._write(f"{self.user}@boos:> {cmd}\n")

        lower = cmd.lower()

        if lower == "exit":
            self._on_close()
            return

        if lower == "clear":
            self._clear()
            return

        threading.Thread(target=self._execute, args=(cmd,), daemon=True).start()

    def _execute(self, cmd_string):
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        old_input = builtins.input

        sys.stdout = Stream(self, "stdout")
        sys.stderr = Stream(self, "stderr")
        builtins.input = self._gui_input

        try:
            parts = cmd_string.strip().split()
            if not parts:
                return

            c = parts[0].lower()
            args = parts[1:]

            actions = {
                "help": self.core.show_help,
                "sysinfo": self.core.show_sysinfo,
                "whoami": lambda: print(f"Logged in as: {self.user}"),
                "boosfetch": self.core.boos_fetch,
                "ping": lambda: self.core.ping(args),
                "calc": lambda: self.core.calculator(args),
                "pkg": lambda: self.core.pkg_manager(args),
                "run": lambda: self.core.run_app(args[0]) if args else print("Usage: run <app_name>")
            }

            if c in actions:
                actions[c]()

                if c == "pkg":
                    print("Tip: Click Refresh on the taskbar if desktop icons changed.")

            elif self.core.app_exists(c):
                self.core.run_app(c)

            else:
                suggestion = self.core.get_suggestion(c)
                if suggestion:
                    print(f"Command '{c}' not found. Did you mean '{suggestion}'?")
                else:
                    print(f"Command '{c}' not found. Type 'help'.")

        except Exception as e:
            print(f"[Terminal Error] {e}")

        finally:
            sys.stdout = old_stdout
            sys.stderr = old_stderr
            builtins.input = old_input

    def _history_up(self, event):
        if self.history:
            self.history_index = max(0, self.history_index - 1)
            self.cmd_entry.delete(0, "end")
            self.cmd_entry.insert(0, self.history[self.history_index])
        return "break"

    def _history_down(self, event):
        if self.history:
            self.history_index = min(len(self.history), self.history_index + 1)
            self.cmd_entry.delete(0, "end")

            if self.history_index < len(self.history):
                self.cmd_entry.insert(0, self.history[self.history_index])

        return "break"


# =============================================================================
# BOOSEXPERIENCE DESKTOP
# =============================================================================
class BoosExperience:
    def __init__(self, root):
        self.root = root
        self.core = BoosCore()
        self.user = None
        self.clock_label = None

        self.root.title("BoosExperience 0.1 Beta 8.2")
        self.root.configure(bg="#1a1a2e")

        try:
            self.root.attributes("-fullscreen", True)
        except Exception:
            try:
                self.root.state("zoomed")
            except Exception:
                pass

        self.root.bind("<Escape>", lambda e: self._toggle_fullscreen())

        self.show_login()

    def _toggle_fullscreen(self):
        try:
            current = self.root.attributes("-fullscreen")
            self.root.attributes("-fullscreen", not current)
        except Exception:
            pass

    def _clear_root(self):
        for child in self.root.winfo_children():
            child.destroy()

    def show_login(self):
        self._clear_root()
        self.user = None
        self.clock_label = None

        login_frame = tk.Frame(self.root, bg="#111111")
        login_frame.pack(fill="both", expand=True)

        box = tk.Frame(login_frame, bg="#1e1e1e")
        box.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(
            box,
            text="🔒 BoosOS Login",
            font=("Segoe UI", 24, "bold"),
            fg="#007acc",
            bg="#1e1e1e"
        ).pack(pady=(20, 10))

        tk.Label(
            box,
            text="Username:",
            font=("Segoe UI", 12),
            fg="#d4d4d4",
            bg="#1e1e1e",
            anchor="w"
        ).pack(fill="x", padx=25)

        user_entry = tk.Entry(
            box,
            font=("Consolas", 14),
            bg="#2d2d2d",
            fg="#d4d4d4",
            insertbackground="#d4d4d4",
            relief="flat"
        )
        user_entry.pack(fill="x", padx=25, pady=(0, 10))
        user_entry.focus_set()

        tk.Label(
            box,
            text="Password:",
            font=("Segoe UI", 12),
            fg="#d4d4d4",
            bg="#1e1e1e",
            anchor="w"
        ).pack(fill="x", padx=25)

        pass_entry = tk.Entry(
            box,
            font=("Consolas", 14),
            bg="#2d2d2d",
            fg="#d4d4d4",
            insertbackground="#d4d4d4",
            show="•",
            relief="flat"
        )
        pass_entry.pack(fill="x", padx=25, pady=(0, 15))

        status_label = tk.Label(
            box,
            text="",
            font=("Segoe UI", 10),
            fg="#ff6b6b",
            bg="#1e1e1e"
        )
        status_label.pack(pady=(0, 10))

        button_frame = tk.Frame(box, bg="#1e1e1e")
        button_frame.pack(fill="x", padx=25, pady=(0, 20))

        def do_login():
            username = user_entry.get().strip()
            password = pass_entry.get().strip()

            if self.core.check_user(username, password):
                self.user = username
                self.core.set_active_user(username)
                self.start_desktop()
            else:
                status_label.config(text="Invalid credentials. Try again.")
                pass_entry.delete(0, "end")

        def do_register():
            username = user_entry.get().strip()
            password = pass_entry.get().strip()

            if not username or not password:
                status_label.config(text="Username and password required.")
                return

            if self.core.add_user(username, password):
                self.user = username
                self.core.set_active_user(username)
                self.start_desktop()
            else:
                status_label.config(text="Username already exists.")

        login_button = tk.Button(
            button_frame,
            text="Login",
            command=do_login,
            bg="#007acc",
            fg="white",
            font=("Segoe UI", 12, "bold"),
            relief="flat",
            cursor="hand2"
        )
        login_button.pack(side="left", expand=True, fill="x", padx=(0, 5))

        register_button = tk.Button(
            button_frame,
            text="Register",
            command=do_register,
            bg="#2d2d2d",
            fg="#d4d4d4",
            font=("Segoe UI", 12),
            relief="flat",
            cursor="hand2"
        )
        register_button.pack(side="right", expand=True, fill="x", padx=(5, 0))

        pass_entry.bind("<Return>", lambda e: do_login())
        user_entry.bind("<Return>", lambda e: pass_entry.focus_set())

    def start_desktop(self):
        self._clear_root()

        self.desktop = tk.Frame(self.root, bg="#1a1a2e")
        self.desktop.place(relx=0, rely=0, relwidth=1, relheight=0.92)

        self.taskbar = tk.Frame(self.root, bg="#161925", height=48)
        self.taskbar.place(relx=0, rely=0.92, relwidth=1, relheight=0.08)
        self.taskbar.pack_propagate(False)

        self._build_taskbar()
        self.refresh_desktop()

    def refresh_desktop(self):
        for child in self.desktop.winfo_children():
            child.destroy()

        terminal_button = tk.Button(
            self.desktop,
            text="💻\nTerminal",
            command=self.open_terminal,
            font=("Segoe UI", 11),
            bg="#252a3a",
            fg="#d4d4d4",
            activebackground="#007acc",
            activeforeground="white",
            relief="flat",
            cursor="hand2"
        )
        terminal_button.grid(row=0, column=0, padx=15, pady=15, sticky="nw")

        apps = self.core._installed_apps()

        if not apps:
            no_apps = tk.Label(
                self.desktop,
                text="No installed apps yet.\nOpen Terminal and type:\npkg install snake",
                font=("Segoe UI", 11),
                bg="#1a1a2e",
                fg="#777777",
                justify="left"
            )
            no_apps.grid(row=1, column=0, padx=15, pady=15, sticky="nw")
            return

        for i, app in enumerate(apps, start=1):
            row = i // 8
            col = i % 8

            button = tk.Button(
                self.desktop,
                text=f"📦\n{app}",
                command=lambda a=app: self.open_app(a),
                font=("Segoe UI", 11),
                bg="#252a3a",
                fg="#d4d4d4",
                activebackground="#007acc",
                activeforeground="white",
                relief="flat",
                cursor="hand2"
            )
            button.grid(row=row, column=col, padx=15, pady=15, sticky="nw")

    def _build_taskbar(self):
        terminal_button = tk.Button(
            self.taskbar,
            text="Terminal",
            command=self.open_terminal,
            bg="#007acc",
            fg="white",
            font=("Segoe UI", 11, "bold"),
            relief="flat",
            cursor="hand2"
        )
        terminal_button.pack(side="left", padx=6, pady=6)

        refresh_button = tk.Button(
            self.taskbar,
            text="Refresh",
            command=self.refresh_desktop,
            bg="#2d2d2d",
            fg="#d4d4d4",
            font=("Segoe UI", 11),
            relief="flat",
            cursor="hand2"
        )
        refresh_button.pack(side="left", padx=6, pady=6)

        logout_button = tk.Button(
            self.taskbar,
            text="Logout",
            command=self.show_login,
            bg="#2d2d2d",
            fg="#ff6b6b",
            font=("Segoe UI", 11),
            relief="flat",
            cursor="hand2"
        )
        logout_button.pack(side="left", padx=6, pady=6)

        user_label = tk.Label(
            self.taskbar,
            text=f"👤 {self.user}@boos",
            font=("Segoe UI", 11, "bold"),
            bg="#161925",
            fg="#007acc"
        )
        user_label.pack(side="right", padx=12)

        self.clock_label = tk.Label(
            self.taskbar,
            font=("Segoe UI", 11),
            bg="#161925",
            fg="#d4d4d4"
        )
        self.clock_label.pack(side="right", padx=12)

        self._update_clock()

    def _update_clock(self):
        try:
            if not self.clock_label:
                return

            if not self.clock_label.winfo_exists():
                return

            self.clock_label.config(text=time.strftime("%H:%M  %b %d"))
            self.root.after(1000, self._update_clock)

        except Exception:
            pass

    def open_terminal(self):
        TerminalWindow(self.root, self.core, self.user)

    def open_app(self, app_name):
        TerminalWindow(
            self.root,
            self.core,
            self.user,
            title=f"{app_name} - {self.user}@boos",
            auto_command=f"run {app_name}"
        )


# =============================================================================
# LAUNCHER
# =============================================================================
def launch():
    try:
        root = tk.Tk()
    except Exception as e:
        print("[FATAL] Could not start Tkinter:", e)
        print()
        print("Fix ideas:")
        print("  Windows: reinstall Python and enable Tcl/Tk")
        print("  Linux: sudo apt install python3-tk")
        print("  Termux: pkg install python-tkinter")
        print("  Pydroid3: install Tkinter from Quick install")
        return

    try:
        app = BoosExperience(root)
        root.mainloop()
    except Exception as e:
        print("[FATAL] BoosExperience crashed:", e)

        try:
            messagebox.showerror("BoosExperience Error", str(e))
        except Exception:
            pass


if globals().get("__name__", "__main__") == "__main__":
    launch()