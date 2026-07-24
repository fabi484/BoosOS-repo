import time, os, socket, difflib, urllib.parse, urllib.request, webbrowser, random, sys, math, datetime, json

# Optional hardware monitoring library
try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False

# Cross-platform check for non-blocking keyboard input
IS_WINDOWS = sys.platform.startswith("win")
if IS_WINDOWS:
    import msvcrt
else:
    import select, tty, termios


class BoosOS:
    def __init__(self):
        self.version = "3.2.5"
        self.running = True
        self.save_dir = "user_saves"
        
        # Linked directly to your GitHub repository raw endpoint
        self.repo_url = "https://raw.githubusercontent.com/fabi484/BoosOS-repo/main"
        
        self.users_file = "users.json"
        self.current_user = None
        self.user_dir = None
        
        if not os.path.exists(self.save_dir): 
            os.makedirs(self.save_dir)
            
        # Set default guest profile
        self.set_active_user("guest")

        self.commands = [
            "sysinfo", "ping", "calc", "clear", "exit", "help", "snake", 
            "tictactoe", "top", "login", "register", "whoami", "pkg", "run"
        ]

    def clear_screen(self):
        os.system("cls" if IS_WINDOWS else "clear")

    def get_suggestion(self, cmd):
        apps_dir = self.get_apps_dir()
        installed_apps = [f[:-3] for f in os.listdir(apps_dir) if f.endswith(".py")] if os.path.exists(apps_dir) else []
        all_valid = self.commands + installed_apps
        matches = difflib.get_close_matches(cmd, all_valid, n=1, cutoff=0.5)
        return matches[0] if matches else None

    # --- USER FOLDER MANAGEMENT (C: DRIVE MAPPING) ---
    def set_active_user(self, username):
        self.current_user = username
        self.user_dir = os.path.abspath(os.path.join(self.save_dir, username))
        if not os.path.exists(self.user_dir):
            os.makedirs(self.user_dir)

    def get_apps_dir(self):
        """Returns the user-specific apps directory inside C:\\installed_apps."""
        apps_path = os.path.join(self.user_dir, "installed_apps")
        if not os.path.exists(apps_path):
            os.makedirs(apps_path)
        return apps_path

    # --- HELP COMMAND WITH INSTALLED APPS ---
    def show_help(self):
        system_cmds = list(self.commands)
        apps_dir = self.get_apps_dir()
        installed_apps = []
        if os.path.exists(apps_dir):
            installed_apps = [f[:-3] for f in os.listdir(apps_dir) if f.endswith(".py")]

        print("\n--- BoosOS Help ---")
        print(f"System Commands : {', '.join(sorted(system_cmds))}")
        if installed_apps:
            print(f"Installed Apps  : {', '.join(sorted(installed_apps))} (Run with: '<app_name>' or 'run <app_name>')")
        else:
            print("Installed Apps  : None (Use 'pkg install <app>' to add apps)")
        print()

    # --- AUTHENTICATION ---
    def load_users(self):
        return json.load(open(self.users_file, "r")) if os.path.exists(self.users_file) else {}

    def register(self):
        users = self.load_users()
        u = input("Create Username: ").strip()
        p = input("Create Password: ").strip()
        
        if not u:
            print("[Error] Username cannot be empty.")
            return

        if u in users:
            print("[Error] Username already exists.")
            return

        users[u] = p
        with open(self.users_file, "w") as f:
            json.dump(users, f, indent=4)

        self.set_active_user(u)
        print(f"[System] User '{u}' registered. Personal drive mapped to C:\\ (user_saves/{u}).")

    def login(self):
        users = self.load_users()
        u = input("Username: ").strip()
        p = input("Password: ").strip()
        
        if users.get(u) == p:
            self.set_active_user(u)
            print(f"Welcome back, {u}! Active drive: C:\\")
        else:
            print("[Auth Error] Invalid username or password.")

    # --- DATA PERSISTENCE ---
    def save_data(self, key, value):
        if not self.user_dir or not os.path.exists(self.user_dir):
            self.set_active_user(self.current_user or "guest")
            
        path = os.path.join(self.user_dir, "data.json")
        data = self.load_user_data()
        data[key] = value
        
        with open(path, "w") as f:
            json.dump(data, f, indent=4)
        print(f"[System] Saved persistent data to C:\\data.json for {self.current_user}.")

    def load_user_data(self):
        if not self.user_dir or not os.path.exists(self.user_dir):
            return {}
        path = os.path.join(self.user_dir, "data.json")
        return json.load(open(path, "r")) if os.path.exists(path) else {}

    # --- ONLINE PACKAGE MANAGER (`pkg`) ---
    def update_single_app(self, app_name):
        apps_dir = self.get_apps_dir()
        app_path = os.path.join(apps_dir, f"{app_name}.py")
        if not os.path.exists(app_path):
            print(f"[PKG Error] App '{app_name}' is not installed on C:\\. Use 'pkg install {app_name}'.")
            return False

        print(f"[PKG] Updating app '{app_name}' from repository...")
        try:
            app_url = f"{self.repo_url}/apps/{app_name}.py?cb={int(time.time())}"
            req = urllib.request.Request(
                app_url, 
                headers={'Cache-Control': 'no-cache', 'Pragma': 'no-cache'}
            )
            with urllib.request.urlopen(req, timeout=5) as response:
                app_code = response.read().decode('utf-8')
                with open(app_path, "w", encoding="utf-8") as f:
                    f.write(app_code)
                print(f"[PKG] App '{app_name}' updated successfully!")
                return True
        except Exception as e:
            print(f"[PKG Error] Failed to update '{app_name}': {e}")
            return False

    def pkg_manager(self, args):
        if not args:
            print("Usage: pkg [install <app> | update [os|<app>|all] | list | run <app>]")
            return

        action = args[0].lower()

        if action == "update":
            target = args[1].lower() if len(args) > 1 else "os"

            if target in ["os", "system"]:
                print("[PKG] Checking for BoosOS kernel updates...")
                try:
                    os_url = f"{self.repo_url}/boos.py?cb={int(time.time())}"
                    req = urllib.request.Request(
                        os_url, 
                        headers={'Cache-Control': 'no-cache', 'Pragma': 'no-cache'}
                    )
                    with urllib.request.urlopen(req, timeout=5) as response:
                        new_code = response.read().decode('utf-8')
                        if "class BoosOS" in new_code:
                            remote_version = None
                            for line in new_code.splitlines():
                                if "self.version =" in line:
                                    remote_version = line.split("=")[1].strip().strip('"').strip("'")
                                    break
                            
                            if remote_version and remote_version == self.version:
                                print(f"[PKG] You are already running the latest version of BoosOS (v{self.version})!")
                                return

                            current_file = os.path.realpath(__file__)
                            with open(current_file, "w", encoding="utf-8") as f:
                                f.write(new_code)
                            print(f"[PKG] OS successfully updated from v{self.version} to v{remote_version or 'newer'}! Restart BoosOS to apply.")
                        else:
                            print("[PKG Error] Downloaded invalid script. Update aborted.")
                except Exception as e:
                    print(f"[PKG Error] Failed to update OS: {e}")

            elif target == "all":
                apps_dir = self.get_apps_dir()
                apps = [f[:-3] for f in os.listdir(apps_dir) if f.endswith(".py")] if os.path.exists(apps_dir) else []
                if not apps:
                    print("[PKG] No installed apps found to update.")
                    return
                print(f"[PKG] Updating all {len(apps)} installed app(s)...")
                for app in apps:
                    self.update_single_app(app)

            else:
                self.update_single_app(target)

        elif action == "install":
            if len(args) < 2:
                print("Usage: pkg install <app_name>")
                return
            app_name = args[1].lower()
            apps_dir = self.get_apps_dir()
            user_label = self.current_user or "guest"
            print(f"[PKG] Fetching '{app_name}' for drive C:\\ ({user_label})...")
            try:
                app_url = f"{self.repo_url}/apps/{app_name}.py?cb={int(time.time())}"
                req = urllib.request.Request(
                    app_url, 
                    headers={'Cache-Control': 'no-cache', 'Pragma': 'no-cache'}
                )
                with urllib.request.urlopen(req, timeout=5) as response:
                    app_code = response.read().decode('utf-8')
                    app_path = os.path.join(apps_dir, f"{app_name}.py")
                    with open(app_path, "w", encoding="utf-8") as f:
                        f.write(app_code)
                    print(f"[PKG] App '{app_name}' successfully installed to C:\\installed_apps\\{app_name}.py!")
            except Exception as e:
                print(f"[PKG Error] Failed to install '{app_name}': {e}")

        elif action == "list":
            apps_dir = self.get_apps_dir()
            user_label = self.current_user or "guest"
            print(f"\n--- Installed Applications [C:\\ ({user_label})] ---")
            apps = [f[:-3] for f in os.listdir(apps_dir) if f.endswith(".py")] if os.path.exists(apps_dir) else []
            if apps:
                for app in apps: 
                    print(f"  * {app}")
            else:
                print("No external apps installed on C:\\ drive.")
            print()

        elif action == "run":
            if len(args) < 2:
                print("Usage: pkg run <app_name>")
                return
            self.run_app(args[1].lower())

        else:
            print(f"[PKG] Unknown package command '{action}'.")

    # --- APP EXECUTION ENVIRONMENT ---
    def run_app(self, app_name):
        apps_dir = self.get_apps_dir()
        app_path = os.path.join(apps_dir, f"{app_name}.py")
        if not os.path.exists(app_path):
            print(f"[Error] App '{app_name}' is not found in C:\\installed_apps\\. Run 'pkg install {app_name}'.")
            return
        
        print(f"[System] Executing C:\\installed_apps\\{app_name}.py...\n")
        try:
            with open(app_path, "r", encoding="utf-8") as f:
                app_code = f.read()
            
            exec_globals = {
                "__builtins__": __builtins__,
                "os": os,
                "sys": sys,
                "time": time,
                "math": math,
                "random": random,
                "IS_WINDOWS": IS_WINDOWS,
                "user_dir": self.user_dir,
                "current_user": self.current_user
            }
            exec(app_code, exec_globals)
        except Exception as e:
            print(f"[App Error] Execution of '{app_name}' failed: {e}")

    # --- SYSTEM UTILITIES ---
    def ping_host(self, host='8.8.8.8'):
        print(f"Pinging {host}...")
        try:
            socket.create_connection((host, 80), timeout=2)
            print("Response received.")
        except: 
            print("Host unreachable.")

    def show_sysinfo(self):
        if HAS_PSUTIL:
            try:
                bat = psutil.sensors_battery()
                bat_str = f"{bat.percent}%" if bat else "N/A"
            except (PermissionError, AttributeError):
                bat_str = "N/A (Access Denied)"
        else:
            bat_str = "N/A (psutil not installed)"
            
        print(f"\n--- BoosOS {self.version} | Drive: C:\\ | {time.strftime('%H:%M:%S')} | Batt: {bat_str} ---\n")

    def task_monitor(self):
        if not HAS_PSUTIL:
            print("[System] Task monitor requires 'psutil'. Install via: pip install psutil")
            return
        print(f"{'PID':<10} {'NAME':<20} {'CPU%'}")
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
            try: 
                print(f"{proc.info['pid']:<10} {proc.info['name']:<20} {proc.info['cpu_percent']}")
            except: 
                pass

    # --- GAMES ---
    def tictactoe(self):
        board = [" " for _ in range(9)]
        def show(): 
            print(f"{board[0]}|{board[1]}|{board[2]}\n-+-+-\n{board[3]}|{board[4]}|{board[5]}\n-+-+-\n{board[6]}|{board[7]}|{board[8]}")
        for turn in range(9):
            show()
            try:
                move = int(input(f"{'X' if turn%2==0 else 'O'} move (0-8): "))
                if board[move] == " ": 
                    board[move] = 'X' if turn%2==0 else 'O'
            except: 
                print("Invalid Input.")
        self.save_data("last_game", "tictactoe")

    def snake_game(self):
        width, height = 20, 15
        snake, food = [[5, 5]], [2, 2]
        direction = [0, 1]
        score = 0
        
        if not IS_WINDOWS:
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            tty.setcbreak(fd)

        try:
            while True:
                self.clear_screen()
                print(f"BoosOS Snake | Score: {score} | Q to quit")
                for y in range(height):
                    line = ""
                    for x in range(width):
                        if [y, x] == snake[0]: line += " @ "
                        elif [y, x] in snake: line += " O "
                        elif [y, x] == food: line += " * "
                        else: line += " . "
                    print(line)

                move = None
                if IS_WINDOWS:
                    time.sleep(0.1)
                    if msvcrt.kbhit():
                        move = msvcrt.getch().decode('utf-8', errors='ignore').lower()
                else:
                    if select.select([sys.stdin], [], [], 0.1)[0]:
                        move = sys.stdin.read(1).lower()

                if move:
                    if move == 'q': break
                    elif move == 'w': direction = [-1, 0]
                    elif move == 'a': direction = [0, -1]
                    elif move == 's': direction = [1, 0]
                    elif move == 'd': direction = [0, 1]

                new_head = [snake[0][0] + direction[0], snake[0][1] + direction[1]]
                if not (0 <= new_head[0] < height and 0 <= new_head[1] < width) or new_head in snake: 
                    break
                snake.insert(0, new_head)
                if new_head == food:
                    score += 10
                    food = [random.randint(0, height-1), random.randint(0, width-1)]
                else: 
                    snake.pop()
        finally:
            if not IS_WINDOWS:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

        if self.current_user: 
            self.save_data("snake_high_score", score)

    def advanced_calc(self):
        print("Calc: Supports +, -, *, /, **, sqrt(x), abs(x). Type 'exit' to quit.")
        while True:
            cmd = input("calc> ")
            if cmd == 'exit': break
            try: 
                print(eval(cmd, {"__builtins__": None}, {"sqrt": math.sqrt, "pow": pow, "abs": abs}))
            except Exception as e: 
                print(f"Error: {e}")

    # --- KERNEL CORE LOOP ---
    def run(self):
        print(f"\n--- BoosOS v{self.version} [Drive C:\\ Mapped] ---\n")
        while self.running:
            prompt = f"{self.current_user or 'guest'}@boos:C:\\>$ "
            try:
                ui = input(prompt).lower().split()
                if not ui: continue
                c = ui[0]
                
                # Check if user tries to execute an installed app directly
                apps_dir = self.get_apps_dir()
                app_path = os.path.join(apps_dir, f"{c}.py")
                
                actions = {
                    "sysinfo": self.show_sysinfo,
                    "ping": lambda: self.ping_host(ui[1] if len(ui)>1 else '8.8.8.8'),
                    "calc": self.advanced_calc,
                    "clear": self.clear_screen,
                    "exit": lambda: setattr(self, 'running', False),
                    "help": self.show_help,
                    "snake": self.snake_game,
                    "tictactoe": self.tictactoe,
                    "top": self.task_monitor,
                    "login": self.login,
                    "register": self.register,
                    "whoami": lambda: print(f"{self.current_user or 'guest'} (Drive: C:\\)"),
                    "pkg": lambda: self.pkg_manager(ui[1:]),
                    "run": lambda: self.run_app(ui[1]) if len(ui) > 1 else print("Usage: run <app_name>")
                }
                
                if c in actions: 
                    actions[c]()
                elif os.path.exists(app_path):
                    self.run_app(c)
                else:
                    sug = self.get_suggestion(c)
                    print(f"Command '{c}' not found. {f'Did you mean {sug}?' if sug else ''}\n")
            except EOFError: 
                break


if __name__ == "__main__":
    try:
        BoosOS().run()
    except Exception as e:
        print(f"\n[System Error] {e}")
    finally:
        if IS_WINDOWS:
            input("\nPress Enter to exit...")