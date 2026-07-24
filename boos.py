import time, os, psutil, socket, difflib, urllib.parse, urllib.request, webbrowser, random, select, sys, tty, termios, math, datetime, json

class BoosOS:
    def __init__(self):
        self.version = "3.1.0"
        self.running = True
        self.current_dir = os.getcwd()
        self.users_file = "users.json"
        self.save_dir = "user_saves"
        self.apps_dir = "installed_apps"
        
        # Linked directly to your GitHub repository raw endpoint
        self.repo_url = "https://raw.githubusercontent.com/fabi484/BoosOS-repo/main"
        
        self.current_user = None
        
        if not os.path.exists(self.save_dir): os.makedirs(self.save_dir)
        if not os.path.exists(self.apps_dir): os.makedirs(self.apps_dir)
        
        self.commands = [
            "sysinfo", "ping", "calc", "clear", "exit", "help", "dm", "snake", 
            "tictactoe", "top", "notes", "net", "nano", "date", "bench", 
            "timer", "search", "ls", "dir", "cd", "login", "register", "whoami",
            "pkg", "run"
        ]

    def get_suggestion(self, cmd):
        matches = difflib.get_close_matches(cmd, self.commands, n=1, cutoff=0.5)
        return matches[0] if matches else None

    # --- ONLINE PACKAGE MANAGER (`pkg`) ---
    def pkg_manager(self, args):
        if not args:
            print("Usage: pkg [install <app_name> | update | list | run <app_name>]")
            return

        action = args[0].lower()

        if action == "update":
            print("[PKG] Checking for BoosOS updates...")
            try:
                os_url = f"{self.repo_url}/boos.py"
                with urllib.request.urlopen(os_url, timeout=5) as response:
                    new_code = response.read().decode('utf-8')
                    current_file = os.path.realpath(__file__)
                    with open(current_file, "w") as f:
                        f.write(new_code)
                    print("[PKG] OS successfully updated! Restart BoosOS to load changes.")
            except Exception as e:
                print(f"[PKG Error] Failed to update OS: {e}")

        elif action == "install":
            if len(args) < 2:
                print("Usage: pkg install <app_name>")
                return
            app_name = args[1].lower()
            print(f"[PKG] Fetching '{app_name}' from github.com/fabi484/BoosOS-repo...")
            try:
                app_url = f"{self.repo_url}/apps/{app_name}.py"
                with urllib.request.urlopen(app_url, timeout=5) as response:
                    app_code = response.read().decode('utf-8')
                    app_path = os.path.join(self.apps_dir, f"{app_name}.py")
                    with open(app_path, "w") as f:
                        f.write(app_code)
                    print(f"[PKG] App '{app_name}' successfully installed!")
            except Exception as e:
                print(f"[PKG Error] Failed to install '{app_name}': {e}")

        elif action == "list":
            print("\n--- Installed Applications ---")
            apps = [f[:-3] for f in os.listdir(self.apps_dir) if f.endswith(".py")]
            if apps:
                for app in apps: print(f"  * {app}")
            else:
                print("No external apps installed.")
            print()

        elif action == "run":
            if len(args) < 2:
                print("Usage: pkg run <app_name>")
                return
            self.run_app(args[1].lower())

        else:
            print(f"[PKG] Unknown package command '{action}'.")

    def run_app(self, app_name):
        app_path = os.path.join(self.apps_dir, f"{app_name}.py")
        if not os.path.exists(app_path):
            print(f"[Error] App '{app_name}' is not installed. Run 'pkg install {app_name}'.")
            return
        
        print(f"[System] Executing {app_name}...\n")
        try:
            with open(app_path, "r") as f:
                app_code = f.read()
            exec_globals = {"os": os, "sys": sys, "time": time, "math": math, "random": random}
            exec(app_code, exec_globals)
        except Exception as e:
            print(f"[App Error] Execution halted: {e}")

    # --- DATA PERSISTENCE ---
    def save_data(self, key, value):
        if not self.current_user: return
        path = os.path.join(self.save_dir, f"{self.current_user}.json")
        data = self.load_user_data()
        data[key] = value
        with open(path, "w") as f: json.dump(data, f)
        print(f"[System] Persistent data saved for {self.current_user}.")

    def load_user_data(self):
        if not self.current_user: return {}
        path = os.path.join(self.save_dir, f"{self.current_user}.json")
        return json.load(open(path, "r")) if os.path.exists(path) else {}

    # --- AUTHENTICATION ---
    def load_users(self):
        return json.load(open(self.users_file, "r")) if os.path.exists(self.users_file) else {}

    def register(self):
        users = self.load_users()
        u, p = input("Create Username: "), input("Create Password: ")
        users[u] = p
        json.dump(users, open(self.users_file, "w"))
        print("Registration complete.")

    def login(self):
        users = self.load_users()
        u, p = input("Username: "), input("Password: ")
        if users.get(u) == p: 
            self.current_user = u
            print(f"Welcome, {u}!")
        else: print("Authentication Failed.")

    # --- SYSTEM UTILITIES ---
    def ping_host(self, host='8.8.8.8'):
        print(f"Pinging {host}...")
        try:
            socket.create_connection((host, 80), timeout=2)
            print("Response received.")
        except: print("Host unreachable.")

    def show_sysinfo(self):
        try:
            bat = psutil.sensors_battery()
            bat_str = f"{bat.percent}%" if bat else "N/A"
        except (PermissionError, AttributeError):
            bat_str = "N/A (Access Denied)"
        print(f"\n--- BoosOS {self.version} | {time.strftime('%H:%M:%S')} | Batt: {bat_str} ---\n")

    def task_monitor(self):
        print(f"{'PID':<10} {'NAME':<20} {'CPU%'}")
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
            try: print(f"{proc.info['pid']:<10} {proc.info['name']:<20} {proc.info['cpu_percent']}")
            except: pass

    # --- GAMES ---
    def tictactoe(self):
        board = [" " for _ in range(9)]
        def show(): print(f"{board[0]}|{board[1]}|{board[2]}\n-+-+-\n{board[3]}|{board[4]}|{board[5]}\n-+-+-\n{board[6]}|{board[7]}|{board[8]}")
        for turn in range(9):
            show()
            try:
                move = int(input(f"{'X' if turn%2==0 else 'O'} move (0-8): "))
                if board[move] == " ": board[move] = 'X' if turn%2==0 else 'O'
            except: print("Invalid Input.")
        self.save_data("last_game", "tictactoe")

    def snake_game(self):
        width, height = 20, 15
        snake, food = [[5, 5]], [2, 2]
        direction = [0, 1]
        score = 0
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setcbreak(fd)
            while True:
                print("\033[H\033[J", end="")
                print(f"BoosOS Snake | Score: {score} | Q to quit")
                for y in range(height):
                    line = ""
                    for x in range(width):
                        if [y, x] == snake[0]: line += " @ "
                        elif [y, x] in snake: line += " O "
                        elif [y, x] == food: line += " * "
                        else: line += " . "
                    print(line)
                if select.select([sys.stdin], [], [], 0.1)[0]:
                    move = sys.stdin.read(1).lower()
                    if move == 'q': break
                    if move == 'w': direction = [-1, 0]
                    elif move == 'a': direction = [0, -1]
                    elif move == 's': direction = [1, 0]
                    elif move == 'd': direction = [0, 1]
                new_head = [snake[0][0] + direction[0], snake[0][1] + direction[1]]
                if not (0 <= new_head[0] < height and 0 <= new_head[1] < width) or new_head in snake: break
                snake.insert(0, new_head)
                if new_head == food:
                    score += 10
                    food = [random.randint(0, height-1), random.randint(0, width-1)]
                else: snake.pop()
        finally: termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        if self.current_user: self.save_data("snake_high_score", score)

    def advanced_calc(self):
        print("Calc: Supports +, -, *, /, **, sqrt(x), abs(x). Type 'exit' to quit.")
        while True:
            cmd = input("calc> ")
            if cmd == 'exit': break
            try: print(eval(cmd, {"__builtins__": None}, {"sqrt": math.sqrt, "pow": pow, "abs": abs}))
            except Exception as e: print(f"Error: {e}")

    # --- KERNEL CORE LOOP ---
    def run(self):
        print(f"\n--- BoosOS v{self.version} [Package-Manager Enabled] ---\n")
        while self.running:
            prompt = f"{self.current_user or 'guest'}@boos:{os.path.basename(self.current_dir)}~$ "
            try:
                ui = input(prompt).lower().split()
                if not ui: continue
                c = ui[0]
                
                actions = {
                    "sysinfo": self.show_sysinfo,
                    "ping": lambda: self.ping_host(ui[1] if len(ui)>1 else '8.8.8.8'),
                    "calc": self.advanced_calc,
                    "clear": lambda: print("\033[H\033[J", end=""),
                    "exit": lambda: setattr(self, 'running', False),
                    "help": lambda: print(f"Available: {', '.join(self.commands)}"),
                    "snake": self.snake_game,
                    "tictactoe": self.tictactoe,
                    "top": self.task_monitor,
                    "login": self.login,
                    "register": self.register,
                    "whoami": lambda: print(self.current_user or "Guest"),
                    "pkg": lambda: self.pkg_manager(ui[1:]),
                    "run": lambda: self.run_app(ui[1]) if len(ui) > 1 else print("Usage: run <app_name>")
                }
                if c in actions: actions[c]()
                else:
                    sug = self.get_suggestion(c)
                    print(f"Command '{c}' not found. {f'Did you mean {sug}?' if sug else ''}\n")
            except EOFError: break

if __name__ == "__main__":
    BoosOS().run()