# BoosOS v3.2.8.1 - Final Release
import time
import os
import socket
import difflib
import urllib.parse
import urllib.request
import urllib.error
import webbrowser
import random
import sys
import math
import datetime
import json

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
        try:
            dr, _, _ = select.select([sys.stdin], [], [], 0)
        except Exception:
            return None

        if dr:
            ch = sys.stdin.read(1)

            if ch == '\x1b':
                try:
                    dr2, _, _ = select.select([sys.stdin], [], [], 0)
                except Exception:
                    dr2 = []

                if dr2:
                    ch2 = sys.stdin.read(1)

                    if ch2 == '[':
                        try:
                            dr3, _, _ = select.select([sys.stdin], [], [], 0)
                        except Exception:
                            dr3 = []

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
            "register", "whoami", "pkg", "run", "notes",
            "boosfetch", "version"
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

    def show_help(self):
        print("\n--- BoosOS Help ---")
        print(f"BoosOS Version  : {self.version}")
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
                with open(self.users_file, "r", encoding="utf-8") as f:
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
            with open(self.users_file, "w", encoding="utf-8") as f:
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

    def save_data(self, key, value):
        data_path = os.path.join(self.user_dir, "data.json")
        data = {}

        if os.path.exists(data_path):
            try:
                with open(data_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except Exception:
                data = {}

        data[key] = value

        try:
            with open(data_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            print(f"[Error] Failed to save data: {e}")

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
            print(
                f"RAM Usage    : {mem.percent}% "
                f"({round(mem.used / 1024 ** 2, 1)}MB / "
                f"{round(mem.total / 1024 ** 2, 1)}MB)"
            )

            print("\nTop 5 Processes by Memory:")

            procs = []

            for p in psutil.process_iter(['pid', 'name', 'memory_percent']):
                try:
                    procs.append(p.info)
                except Exception:
                    pass

            procs = sorted(
                procs,
                key=lambda x: x['memory_percent'] or 0,
                reverse=True
            )[:5]

            for p in procs:
                print(
                    f" PID {p['pid']:<6} | "
                    f"{p['name']:<20} | "
                    f"Mem: {round(p['memory_percent'] or 0, 2)}%"
                )

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
                (0, 1, 2), (3, 4, 5), (6, 7, 8),
                (0, 3, 6), (1, 4, 7), (2, 5, 8),
                (0, 4, 8), (2, 4, 6)
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

                if (
                    head_r <= 0 or head_r >= height - 1 or
                    head_c <= 0 or head_c >= width - 1 or
                    new_head in snake
                ):
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
            self._pkg_print_help()
            return

        action = args[0].lower()
        upgrade_requested = False

        if action in ("upgrade", "up"):
            action = "update"
            upgrade_requested = True
        elif action in ("remove", "rm", "delete"):
            action = "uninstall"
        elif action in ("ls", "list"):
            action = "list"
        elif action in ("help", "-h", "--help"):
            self._pkg_print_help()
            return

        if action == "list":
            print("\n--- BoosOS Package Manager ---")

            installed = self._pkg_installed_apps()

            print(f"Installed apps : {', '.join(installed) if installed else 'None'}")
            print(f"Repository URL : {self.repo_url}")
            print("Update targets  : os, all, apps, <app_name>")
            print()

        elif action == "install":
            if len(args) < 2:
                print("[PKG Error] Usage: pkg install <app_name>")
                return

            self._pkg_install_app(args[1])

        elif action == "uninstall":
            if len(args) < 2:
                print("[PKG Error] Usage: pkg uninstall <app_name>")
                return

            self._pkg_uninstall_app(args[1])

        elif action == "update":
            if len(args) > 1:
                target = args[1].lower()
            else:
                target = "all" if upgrade_requested else "os"

            if target in ("all", "*", "everything"):
                print("[PKG] Updating BoosOS core and all installed apps...")
                self._pkg_update_os()
                self._pkg_update_all_apps()

            elif target in ("os", "system", "core", "boos", "boosos"):
                self._pkg_update_os()

            elif target in ("apps", "installed", "local"):
                self._pkg_update_all_apps()

            else:
                self._pkg_update_app(target)

        else:
            print(f"[PKG Error] Unknown action '{action}'. Try 'pkg help'.")

    def _pkg_print_help(self):
        print("\n--- BoosOS Package Manager ---")
        print("Usage:")
        print("  pkg list                         Show installed apps")
        print("  pkg install <app_name>           Install/update an app from repo")
        print("  pkg uninstall <app_name>         Remove an installed app")
        print("  pkg update                       Update BoosOS core")
        print("  pkg update os                    Update BoosOS core")
        print("  pkg update all                   Update BoosOS core + all installed apps")
        print("  pkg update apps                  Update all installed apps")
        print("  pkg update <app_name>            Update one installed app")
        print("  pkg upgrade                      Same as pkg update all")
        print("  pkg upgrade <target>             Same as pkg update <target>")
        print()

    def _pkg_repo_url(self, path=""):
        base = str(self.repo_url).rstrip("/")

        if not path:
            return base

        return f"{base}/{path.lstrip('/')}"

    def _pkg_installed_apps(self):
        apps_dir = self.get_apps_dir()

        if not os.path.exists(apps_dir):
            return []

        try:
            return sorted([f[:-3] for f in os.listdir(apps_dir) if f.endswith(".py")])
        except Exception:
            return []

    def _pkg_safe_app_name(self, app_name):
        app_name = os.path.basename(str(app_name).strip().lower())

        if app_name.endswith(".py"):
            app_name = app_name[:-3]

        allowed = "abcdefghijklmnopqrstuvwxyz0123456789_-"

        if not app_name or any(ch not in allowed for ch in app_name):
            return None

        return app_name

    def _pkg_fetch(self, url, timeout=10):
        req = urllib.request.Request(
            url,
            headers={
                "Cache-Control": "no-cache",
                "Pragma": "no-cache",
                "User-Agent": f"BoosOS/{self.version}"
            }
        )

        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read().decode("utf-8")

    def _pkg_write_text(self, path, text):
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)

    def _pkg_backup_file(self, path):
        try:
            if os.path.exists(path):
                backup = path + ".bak"

                with open(path, "r", encoding="utf-8") as src:
                    data = src.read()

                with open(backup, "w", encoding="utf-8") as dst:
                    dst.write(data)

                return backup

        except Exception:
            return None

        return None

    def _pkg_install_app(self, app_name):
        safe_name = self._pkg_safe_app_name(app_name)

        if not safe_name:
            print("[PKG Error] Invalid app name. Use letters, numbers, '-' and '_'.")
            return False

        url = self._pkg_repo_url(f"apps/{safe_name}.py?cb={int(time.time())}")
        print(f"[PKG] Fetching {url}...")

        try:
            code = self._pkg_fetch(url)

            if not code.strip():
                print("[PKG Error] Downloaded file is empty.")
                return False

            dest_path = os.path.join(self.get_apps_dir(), f"{safe_name}.py")
            existed = os.path.exists(dest_path)

            self._pkg_backup_file(dest_path)
            self._pkg_write_text(dest_path, code)

            verb = "Updated" if existed else "Installed"
            print(f"[PKG] {verb} '{safe_name}' successfully!")

            return True

        except Exception as e:
            print(f"[PKG Error] Failed to download package: {e}")
            return False

    def _pkg_uninstall_app(self, app_name):
        safe_name = self._pkg_safe_app_name(app_name)

        if not safe_name:
            print("[PKG Error] Invalid app name. Use letters, numbers, '-' and '_'.")
            return False

        target_path = os.path.join(self.get_apps_dir(), f"{safe_name}.py")

        if os.path.exists(target_path):
            try:
                os.remove(target_path)
                print(f"[PKG] App '{safe_name}' uninstalled.")
                return True
            except Exception as e:
                print(f"[PKG Error] Could not uninstall '{safe_name}': {e}")
                return False
        else:
            print(f"[PKG Error] App '{safe_name}' is not installed.")
            return False

    def _pkg_update_os(self):
        try:
            url = self._pkg_repo_url(f"boos.py?cb={int(time.time())}")
            print(f"[PKG] Fetching {url}...")

            new_code = self._pkg_fetch(url)

            if "class BoosOS" not in new_code:
                print("[PKG Error] Valid system code not found at repository source.")
                return False

            script = globals().get("__file__")

            if not script:
                script = sys.argv[0] if sys.argv else "boos.py"

            current_script = os.path.realpath(script)

            if not os.path.isfile(current_script):
                print("[PKG Error] Could not locate the current BoosOS script file.")
                return False

            try:
                with open(current_script, "r", encoding="utf-8") as f:
                    old_code = f.read()

                if old_code == new_code:
                    print("[PKG] BoosOS is already up to date.")
                    return True

            except Exception:
                old_code = None

            backup = self._pkg_backup_file(current_script)
            self._pkg_write_text(current_script, new_code)

            if backup:
                print(f"[PKG] Backup saved to {backup}")

            print("[PKG] BoosOS system core updated successfully! Restart BoosOS to use the new version.")

            return True

        except Exception as e:
            print(f"[PKG Error] Could not update system: {e}")
            return False

    def _pkg_update_app(self, app_name, quiet=False):
        safe_name = self._pkg_safe_app_name(app_name)

        if not safe_name:
            if not quiet:
                print("[PKG Error] Invalid app name. Use letters, numbers, '-' and '_'.")
            return False

        dest_path = os.path.join(self.get_apps_dir(), f"{safe_name}.py")

        if not os.path.exists(dest_path):
            if not quiet:
                print(f"[PKG Error] App '{safe_name}' is not installed. Use 'pkg install {safe_name}'.")
            return False

        url = self._pkg_repo_url(f"apps/{safe_name}.py?cb={int(time.time())}")

        if not quiet:
            print(f"[PKG] Fetching {url}...")

        try:
            code = self._pkg_fetch(url)

            if not code.strip():
                print(f"[PKG Error] Downloaded file for '{safe_name}' is empty.")
                return False

            try:
                with open(dest_path, "r", encoding="utf-8") as f:
                    old_code = f.read()

                if old_code == code:
                    if not quiet:
                        print(f"[PKG] App '{safe_name}' is already up to date.")
                    return True

            except Exception:
                old_code = None

            self._pkg_backup_file(dest_path)
            self._pkg_write_text(dest_path, code)

            if not quiet:
                print(f"[PKG] Updated app '{safe_name}' successfully!")

            return True

        except Exception as e:
            print(f"[PKG Error] Failed to update '{safe_name}': {e}")
            return False

    def _pkg_update_all_apps(self):
        installed = self._pkg_installed_apps()

        if not installed:
            print("[PKG] No installed apps to update.")
            return 0

        print(f"[PKG] Checking updates for {len(installed)} installed app(s)...")

        updated = 0
        failed = 0

        for app in installed:
            if self._pkg_update_app(app, quiet=True):
                updated += 1
                print(f"[PKG] OK: {app}")
            else:
                failed += 1
                print(f"[PKG] FAILED/SKIPPED: {app}")

        print(f"[PKG] App update summary -> OK: {updated}, Failed/Skipped: {failed}")

        return updated

    def run_app(self, app_name):
        app_path = os.path.join(self.get_apps_dir(), f"{app_name}.py")

        if os.path.exists(app_path):
            try:
                print(f"[System] Running '{app_name}'...\n")

                with open(app_path, "r", encoding="utf-8") as f:
                    code = f.read()

                exec(
                    code,
                    {
                        "__builtins__": __builtins__,
                        "__name__": "__main__",
                        "__file__": app_path,
                        "os": os,
                        "sys": sys,
                        "time": time,
                        "random": random,
                        "math": math,
                        "json": json,
                        "socket": socket,
                        "datetime": datetime,
                        "urllib": urllib,
                        "webbrowser": webbrowser,
                        "safe_input": safe_input,
                        "input": safe_input,
                        "get_key_nonblocking": get_key_nonblocking,
                        "IS_WINDOWS": IS_WINDOWS,
                        "HAS_PSUTIL": HAS_PSUTIL,
                        "boos": self
                    }
                )

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

        print("==================================================")
        print(f"           Welcome to BoosOS v{self.version}")
        print("  Type 'help' for commands or 'exit' to quit.  ")
        print("==================================================\n")

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
                    "ping": lambda: self.ping(args),
                    "calc": lambda: self.calculator(args),
                    "top": self.top_process,
                    "tictactoe": self.play_tictactoe,
                    "snake": self.play_snake,
                    "register": self.register,
                    "login": self.login,
                    "whoami": lambda: print(f"Logged in as: {self.current_user or 'guest'}"),
                    "version": lambda: print(f"BoosOS v{self.version}")
                }

                if c in actions:
                    actions[c]()

                elif c == "run" and args:
                    app_name = args[0]

                    if app_name.endswith(".py"):
                        app_name = app_name[:-3]

                    self.run_app(app_name)

                elif c == "run":
                    print("[Error] Usage: run <app_name>")

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