#!/usr/bin/env python3
"""
================================================================================
                         BoosOS CORE OPERATING SYSTEM
                         Version: 3.2.8.2 Enterprise
                         Architect: Fabi / BoosOS Dev Team
================================================================================

DESCRIPTION:
    BoosOS is an advanced, cross-platform terminal and GUI simulation environment 
    built for Linux, Android (Termux / Pydroid 3), and Windows environments. 
    It features an automated hardware/environment detection subsystem, dynamic 
    theming engines (including Google Pixel Mobile branding), bilingual localization 
    (English & Romanian), a safe sandboxed math solver, built-in text editor, 
    process status monitoring, micro file manager, and launcher subsystems.

SYSTEM ARCHITECTURE MODULES:
    1. Core Constants & Terminal Color Definitions
    2. Localization & Multi-Language Dictionary System
    3. Hardware, Platform, and Runtime Detection Engine
    4. Theme Manager & Dynamic Color Palette Renderer
    5. Logger Subsystem & System Trace Utilities
    6. System Metrics, Benchmark, & Hardware Diagnostics
    7. Sandboxed Safe Mathematical Evaluation Engine
    8. Interactive Micro-File Manager Subsystem
    9. Session Notes & Persistent Data Manager
   10. Integrated Application Registry & Process Manager
   11. Graphical User Interface (Tkinter Desktop Environment)
   12. Command Interpreter, REPL Engine, and Dispatcher
   13. Interactive Main Execution Entry Point

================================================================================
"""

import os
import sys
import time
import math
import json
import shutil
import random
import datetime
import platform
import subprocess

# ==============================================================================
# SECTION 1: TERMINAL COLOR DEFINITIONS AND ANSI ESCAPE CODES
# ==============================================================================

class ANSIColors:
    """Provides high-definition 24-bit RGB and 8-bit ANSI escape codes."""
    RESET         = '\033[0m'
    BOLD          = '\033[1m'
    DIM           = '\033[2m'
    ITALIC        = '\033[3m'
    UNDERLINE     = '\033[4m'
    BLINK         = '\033[5m'
    REVERSE       = '\033[7m'
    HIDDEN        = '\033[8m'

    # Standard Foreground Colors
    BLACK         = '\033[30m'
    RED           = '\033[31m'
    GREEN         = '\033[32m'
    YELLOW        = '\033[33m'
    BLUE          = '\033[34m'
    MAGENTA       = '\033[35m'
    CYAN          = '\033[36m'
    WHITE         = '\033[37m'

    # High Intensity Foreground Colors
    BRIGHT_BLACK  = '\033[90m'
    BRIGHT_RED    = '\033[91m'
    BRIGHT_GREEN  = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE   = '\033[94m'
    BRIGHT_MAGENTA= '\033[95m'
    BRIGHT_CYAN   = '\033[96m'
    BRIGHT_WHITE  = '\033[97m'

    # Standard Background Colors
    BG_BLACK      = '\033[40m'
    BG_RED        = '\033[41m'
    BG_GREEN      = '\033[42m'
    BG_YELLOW     = '\033[43m'
    BG_BLUE       = '\033[44m'
    BG_MAGENTA    = '\033[45m'
    BG_CYAN       = '\033[46m'
    BG_WHITE      = '\033[47m'

    # Google Pixel Signature Palette (TrueColor 24-bit RGB)
    PIXEL_BLUE    = '\033[38;2;66;133;244m'
    PIXEL_RED     = '\033[38;2;234;67;53m'
    PIXEL_YELLOW  = '\033[38;2;251;188;5m'
    PIXEL_GREEN   = '\033[38;2;52;168;83m'
    PIXEL_DARK    = '\033[38;2;32;33;36m'
    PIXEL_GRAY    = '\033[38;2;95;99;104m'

    # Cyberpunk Theme RGB Palette
    NEON_CYAN     = '\033[38;2;0;255;240m'
    NEON_PINK     = '\033[38;2;255;0;127m'
    NEON_PURPLE   = '\033[38;2;189;0;255m'
    NEON_YELLOW   = '\033[38;2;255;234;0m'


# ==============================================================================
# SECTION 2: SYSTEM CONFIGURATION & GLOBAL STATE MANAGER
# ==============================================================================

class SystemConfig:
    VERSION = "3.2.8.2"
    BUILD_NUMBER = "2026.08.10-ENT"
    CODENAME = "Apex Horizon"
    AUTHOR = "Fabi / BoosOS Team"
    CONFIG_FILE_PATH = os.path.expanduser("~/.boosos_config.json")

    @classmethod
    def load_defaults(cls):
        return {
            "version": cls.VERSION,
            "language": "en",
            "theme": "pixel" if is_android_device() else "classic",
            "auto_clear": True,
            "enable_logging": True,
            "prompt_style": "default",
            "show_welcome_banner": True,
            "max_history_length": 500
        }

class GlobalState:
    """Manages runtime variables, history logs, notes, and session state."""
    def __init__(self):
        self.config = SystemConfig.load_defaults()
        self.running = True
        self.command_history = []
        self.session_notes = []
        self.system_logs = []
        self.start_time = time.time()
        self.active_language = self.config["language"]
        self.active_theme_name = self.config["theme"]

    def log_event(self, level, message):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"[{timestamp}] [{level.upper()}] {message}"
        self.system_logs.append(entry)
        if len(self.system_logs) > 1000:
            self.system_logs.pop(0)

SYSTEM_STATE = GlobalState()


# ==============================================================================
# SECTION 3: ENVIRONMENT & HARDWARE DETECTION SUBSYSTEM
# ==============================================================================

def is_android_device():
    """Detects if running on Android/Termux/Pydroid."""
    android_indicators = [
        'ANDROID_ROOT',
        'ANDROID_DATA',
        'TERMUX_VERSION',
        'PREFIX'
    ]
    for env_var in android_indicators:
        if env_var in os.environ:
            return True
    if hasattr(sys, 'getandroidapilevel'):
        return True
    return False

def check_gui_capability():
    """Verifies whether Tkinter and X11/Wayland or native display are online."""
    if is_android_device() and 'DISPLAY' not in os.environ:
        return False
    try:
        import tkinter as tk
        root = tk.Tk()
        root.destroy()
        return True
    except Exception:
        return False

SYSTEM_ENVIRONMENT = {
    "is_mobile": is_android_device(),
    "has_gui": check_gui_capability(),
    "platform": platform.system(),
    "architecture": platform.machine(),
    "python_version": platform.python_version()
}


# ==============================================================================
# SECTION 4: THEME ENGINE & VISUAL STYLING PALETTES
# ==============================================================================

THEME_REGISTRY = {
    "pixel": {
        "name": "Google Pixel Mobile Experience",
        "primary": ANSIColors.PIXEL_BLUE,
        "secondary": ANSIColors.PIXEL_GREEN,
        "accent": ANSIColors.PIXEL_YELLOW,
        "error": ANSIColors.PIXEL_RED,
        "dim": ANSIColors.PIXEL_GRAY,
        "prompt": f"{ANSIColors.PIXEL_BLUE}G{ANSIColors.PIXEL_RED}o{ANSIColors.PIXEL_YELLOW}o{ANSIColors.PIXEL_BLUE}g{ANSIColors.PIXEL_GREEN}l{ANSIColors.PIXEL_RED}e{ANSIColors.RESET} {ANSIColors.PIXEL_BLUE}❯{ANSIColors.PIXEL_GREEN}❯{ANSIColors.RESET} ",
        "badge": f"{ANSIColors.PIXEL_BLUE}[Pixel Mobile Core v3.2.8.2]{ANSIColors.RESET}",
        "gui_bg": "#121212",
        "gui_fg": "#E8EAED",
        "gui_accent": "#4285F4",
        "gui_panel": "#1E1E1E"
    },
    "classic": {
        "name": "Classic Desktop Workstation",
        "primary": ANSIColors.BRIGHT_CYAN,
        "secondary": ANSIColors.BRIGHT_GREEN,
        "accent": ANSIColors.BRIGHT_YELLOW,
        "error": ANSIColors.BRIGHT_RED,
        "dim": ANSIColors.BRIGHT_BLACK,
        "prompt": f"{ANSIColors.BRIGHT_CYAN}boos@desktop{ANSIColors.RESET}:{ANSIColors.BRIGHT_BLUE}~${ANSIColors.RESET} ",
        "badge": f"{ANSIColors.BRIGHT_BLACK}[PC Desktop Subsystem v3.2.8.2]{ANSIColors.RESET}",
        "gui_bg": "#1E1E2E",
        "gui_fg": "#CDD6F4",
        "gui_accent": "#89B4FA",
        "gui_panel": "#313244"
    },
    "matrix": {
        "name": "Matrix Cyber Terminal",
        "primary": ANSIColors.BRIGHT_GREEN,
        "secondary": ANSIColors.GREEN,
        "accent": ANSIColors.BRIGHT_WHITE,
        "error": ANSIColors.BRIGHT_RED,
        "dim": ANSIColors.GREEN,
        "prompt": f"{ANSIColors.BRIGHT_GREEN}boos@matrix>{ANSIColors.RESET} ",
        "badge": f"{ANSIColors.BRIGHT_GREEN}[Matrix Virtual Terminal v3.2.8.2]{ANSIColors.RESET}",
        "gui_bg": "#000000",
        "gui_fg": "#00FF00",
        "gui_accent": "#00FF00",
        "gui_panel": "#051505"
    },
    "cyberpunk": {
        "name": "Cyberpunk Neon 2077",
        "primary": ANSIColors.NEON_CYAN,
        "secondary": ANSIColors.NEON_PINK,
        "accent": ANSIColors.NEON_YELLOW,
        "error": ANSIColors.BRIGHT_RED,
        "dim": ANSIColors.NEON_PURPLE,
        "prompt": f"{ANSIColors.NEON_PINK}cyber{ANSIColors.NEON_CYAN}@boosOS{ANSIColors.RESET}❯ ",
        "badge": f"{ANSIColors.NEON_CYAN}[Neon Cyber Core v3.2.8.2]{ANSIColors.RESET}",
        "gui_bg": "#0d0f18",
        "gui_fg": "#00f0ff",
        "gui_accent": "#ff0055",
        "gui_panel": "#1a1c23"
    }
}

def get_current_theme():
    theme_key = SYSTEM_STATE.active_theme_name
    return THEME_REGISTRY.get(theme_key, THEME_REGISTRY["classic"])


# ==============================================================================
# SECTION 5: BILINGUAL LOCALIZATION ENGINE (EN / RO)
# ==============================================================================

LOCALIZATION_DICTIONARY = {
    "en": {
        "sys_title": "BoosOS v3.2.8.2 Enterprise Kernel",
        "welcome": "BoosOS Terminal Environment Initialized Successfully.",
        "ready": "System status nominal. Type 'help' to review available commands.",
        "unknown": "Unrecognized command sequence. Type 'help' for directory.",
        "lang_changed": "System locale updated to: English (en).",
        "theme_changed": "Active color profile switched to: ",
        "help_header": "=================== BOOSOS v3.2.8.2 COMMAND DIRECTORY ===================",
        "cmd_sysinfo": "  sysinfo         - Print hardware diagnostics, runtime statistics, and OS build",
        "cmd_ls": "  ls [path]       - List contents of specified target path",
        "cmd_cd": "  cd <path>       - Change absolute or relative working directory",
        "cmd_pwd": "  pwd             - Display current working directory path",
        "cmd_cat": "  cat <file>      - Output target file contents directly to stdout",
        "cmd_edit": "  edit <file>     - Launch interactive micro text editor",
        "cmd_calc": "  calc <expr>     - Safe arithmetic evaluation engine",
        "cmd_notes": "  notes <add/ls>  - Session quick-notes manager",
        "cmd_apps": "  apps [launch]   - List or execute modular applications in apps/",
        "cmd_gui": "  gui             - Initialize Tkinter Graphical User Interface desktop",
        "cmd_bench": "  bench           - Execute CPU performance diagnostic benchmark",
        "cmd_logs": "  logs            - View internal system event logs",
        "cmd_theme": "  theme <name>    - Change theme (pixel, classic, matrix, cyberpunk)",
        "cmd_lang": "  lang <en/ro>    - Switch locale dictionary (English / Romanian)",
        "cmd_history": "  history         - Display command invocation buffer",
        "cmd_clear": "  clear           - Flush viewport lines",
        "cmd_exit": "  exit            - Terminate active session",
        "lbl_host": "Hostname",
        "lbl_os": "Operating System",
        "lbl_arch": "Platform Arch",
        "lbl_runtime": "Runtime Subsystem",
        "lbl_kernel": "Kernel Version",
        "lbl_python": "Python Engine",
        "lbl_uptime": "Session Uptime",
        "lbl_time": "System Clock",
        "calc_error": "Mathematics evaluation error: Invalid expression.",
        "notes_empty": "No session notes currently recorded.",
        "notes_saved": "New entry written to session notes.",
        "notes_cleared": "Session note buffer cleared.",
        "exit_msg": "Terminating BoosOS v3.2.8.2 kernel session. Goodbye Fabi!"
    },
    "ro": {
        "sys_title": "Kernel BoosOS v3.2.8.2 Enterprise",
        "welcome": "Mediul de Terminal BoosOS a fost inițializat cu succes.",
        "ready": "Stare sistem: Nominală. Tastați 'help' pentru lista de comenzi.",
        "unknown": "Secvență de comandă necunoscută. Tastați 'help' pentru ajutor.",
        "lang_changed": "Limba sistemului a fost schimbată în: Română (ro).",
        "theme_changed": "Profilul cromatic activ a fost schimbat în: ",
        "help_header": "=================== DIRECTOR COMENZI BOOSOS v3.2.8.2 ===================",
        "cmd_sysinfo": "  sysinfo         - Afișează diagnosticul hardware și datele sistemului",
        "cmd_ls": "  ls [cale]       - Listează conținutul directorului specificat",
        "cmd_cd": "  cd <cale>       - Schimbă directorul curent de lucru",
        "cmd_pwd": "  pwd             - Afișează calea absolută curentă",
        "cmd_cat": "  cat <fișier>    - Afișează conținutul fișierului specificat",
        "cmd_edit": "  edit <fișier>   - Deschide editorul interactiv de text",
        "cmd_calc": "  calc <expr>     - Calculator matematic securizat",
        "cmd_notes": "  notes <add/ls>  - Manager de notițe rapide ale sesiunii",
        "cmd_apps": "  apps [launch]   - Listează sau lansează aplicații din directorul apps/",
        "cmd_gui": "  gui             - Pornește interfața grafică desktop Tkinter",
        "cmd_bench": "  bench           - Execută un test de performanță pentru procesor",
        "cmd_logs": "  logs            - Afișează jurnalul intern de evenimente",
        "cmd_theme": "  theme <nume>    - Schimbă tema (pixel, classic, matrix, cyberpunk)",
        "cmd_lang": "  lang <en/ro>    - Schimbă limba (Engleză / Română)",
        "cmd_history": "  history         - Afișează istoricul comenzilor executate",
        "cmd_clear": "  clear           - Curăță ecranul terminalului",
        "cmd_exit": "  exit            - Închide sesiunea curentă BoosOS",
        "lbl_host": "Nume Gazdă",
        "lbl_os": "Sistem Operare",
        "lbl_arch": "Arhitectură",
        "lbl_runtime": "Mediu Rulare",
        "lbl_kernel": "Versiune Kernel",
        "lbl_python": "Nucleu Python",
        "lbl_uptime": "Timp Activitate",
        "lbl_time": "Ora Sistemului",
        "calc_error": "Eroare de calcul matematic: Expresie invalidă.",
        "notes_empty": "Nu există notițe salvate în sesiunea curentă.",
        "notes_saved": "Notiță adăugată cu succes.",
        "notes_cleared": "Istoricul de notițe a fost șters.",
        "exit_msg": "Se închide sesiunea BoosOS v3.2.8.2. La revedere Fabi!"
    }
}

def translate(key):
    """Retrieves string from dictionary based on active language setting."""
    lang = SYSTEM_STATE.active_language
    dict_ref = LOCALIZATION_DICTIONARY.get(lang, LOCALIZATION_DICTIONARY["en"])
    return dict_ref.get(key, f"[{key}]")


# ==============================================================================
# SECTION 6: ASCII BANNER GENERATION & VISUAL HEADERS
# ==============================================================================

def generate_pixel_banner():
    pb = ANSIColors.PIXEL_BLUE
    pr = ANSIColors.PIXEL_RED
    py = ANSIColors.PIXEL_YELLOW
    pg = ANSIColors.PIXEL_GREEN
    rst = ANSIColors.RESET
    return f"""
 {pb}   G G G G   {pr} o o o o   {py} o o o o   {pb} G G G G   {pg} l {pr} e e e e {rst}
 {pb}  G          {pr}o       o  {py}o       o  {pb}G          {pg} l {pr} e       {rst}
 {pb}  G    G G G {pr}o       o  {py}o       o  {pb}G    G G G {pg} l {pr} e e e e {rst}
 {pb}  G       G  {pr}o       o  {py}o       o  {pb}G       G  {pg} l {pr} e       {rst}
 {pb}   G G G G   {pr} o o o o   {py} o o o o   {pb}  G G G G   {pg} l {pr} e e e e {rst}
    """

def generate_desktop_banner():
    theme = get_current_theme()
    p = theme["primary"]
    rst = ANSIColors.RESET
    return f"""
{p}  ____                  ___  ____    _____  ____  _____ 
 |  _ \  ___   ___  ___/ _ \/ ___|  |___ / |___ \| ____|
 | |_) |/ _ \ / _ \/ __| | | \___ \    |_ \   __) |  _|  
 |  _ <| (_) | (_) \__ \ |_| |___) |  ___) | / __/| |___ 
 |_| \_\\___/ \___/|___/\___/|____/  |____/ |_____|_____|{rst}
"""

def print_banner():
    if SYSTEM_ENVIRONMENT["is_mobile"]:
        print(generate_pixel_banner())
    else:
        print(generate_desktop_banner())


# ==============================================================================
# SECTION 7: SYSTEM DIAGNOSTICS & BENCHMARKING
# ==============================================================================

def calculate_uptime():
    elapsed = int(time.time() - SYSTEM_STATE.start_time)
    hours = elapsed // 3600
    minutes = (elapsed % 3600) // 60
    seconds = elapsed % 60
    return f"{hours}h {minutes}m {seconds}s"

def print_system_info():
    theme = get_current_theme()
    print_banner()
    print(f"{theme['primary']}{'='*65}{ANSIColors.RESET}")
    print(f"{theme['secondary']}{translate('lbl_host')}:{ANSIColors.RESET} {platform.node()}")
    print(f"{theme['secondary']}{translate('lbl_os')}:{ANSIColors.RESET} {platform.system()} {platform.release()}")
    print(f"{theme['secondary']}{translate('lbl_arch')}:{ANSIColors.RESET} {platform.machine()}")
    print(f"{theme['secondary']}{translate('lbl_kernel')}:{ANSIColors.RESET} BoosOS v{SystemConfig.VERSION} ({SystemConfig.BUILD_NUMBER})")
    print(f"{theme['secondary']}{translate('lbl_runtime')}:{ANSIColors.RESET} {'ANDROID/TERMUX' if SYSTEM_ENVIRONMENT['is_mobile'] else 'DESKTOP PC'} {theme['badge']}")
    print(f"{theme['secondary']}{translate('lbl_python')}:{ANSIColors.RESET} Python {platform.python_version()}")
    print(f"{theme['secondary']}{translate('lbl_uptime')}:{ANSIColors.RESET} {calculate_uptime()}")
    print(f"{theme['secondary']}{translate('lbl_time')}:{ANSIColors.RESET} {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{theme['primary']}{'='*65}{ANSIColors.RESET}")
    SYSTEM_STATE.log_event("info", "Printed system diagnostics info.")

def run_cpu_benchmark():
    theme = get_current_theme()
    print(f"{theme['accent']}Running BoosOS CPU Performance Benchmark...{ANSIColors.RESET}")
    start = time.time()
    
    # Prime number calculation benchmark loop
    primes_found = 0
    for num in range(2, 25000):
        is_prime = True
        for i in range(2, int(math.sqrt(num)) + 1):
            if num % i == 0:
                is_prime = False
                break
        if is_prime:
            primes_found += 1
            
    duration = time.time() - start
    print(f"{theme['primary']}Benchmark Complete!{ANSIColors.RESET}")
    print(f"Calculated primes up to 25,000 in {duration:.4f} seconds.")
    print(f"Score: {int(10000 / (duration + 0.001))} BoosPoints")
    SYSTEM_STATE.log_event("info", f"Executed benchmark score: {int(10000 / (duration + 0.001))}")


# ==============================================================================
# SECTION 8: MATHEMATICAL EVALUATION ENGINE (SAFE SANDBOX)
# ==============================================================================

class MathEngine:
    @staticmethod
    def evaluate(expression_string):
        """Safely evaluates algebraic expressions without risking code execution."""
        safe_dict = {
            "math": math,
            "sin": math.sin,
            "cos": math.cos,
            "tan": math.tan,
            "sqrt": math.sqrt,
            "pow": pow,
            "abs": abs,
            "round": round,
            "pi": math.pi,
            "e": math.e
        }
        try:
            compiled_code = compile(expression_string, "<string>", "eval")
            for name in compiled_code.co_names:
                if name not in safe_dict:
                    raise NameError(f"Function {name} is restricted for security.")
            result = eval(compiled_code, {"__builtins__": {}}, safe_dict)
            return True, result
        except Exception as err:
            return False, str(err)

def execute_calculator(args):
    if not args:
        print(f"{ANSIColors.YELLOW}Usage: calc <expression> (e.g., calc 2**10 or calc sqrt(144)){ANSIColors.RESET}")
        return
    expr = " ".join(args)
    success, result = MathEngine.evaluate(expr)
    if success:
        print(f"{ANSIColors.BRIGHT_GREEN}= {result}{ANSIColors.RESET}")
        SYSTEM_STATE.log_event("info", f"Calculator evaluated '{expr}' = {result}")
    else:
        print(f"{ANSIColors.BRIGHT_RED}{translate('calc_error')}{ANSIColors.RESET}")
        SYSTEM_STATE.log_event("error", f"Calculator failed on '{expr}': {result}")


# ==============================================================================
# SECTION 9: MICRO TEXT EDITOR SUBSYSTEM
# ==============================================================================

def launch_micro_editor(filename):
    """Simple terminal text editor."""
    theme = get_current_theme()
    print(f"{theme['primary']}--- BoosOS Micro Editor: Editing {filename} ---{ANSIColors.RESET}")
    print(f"{theme['dim']}Type your lines below. Type ':w' on a new line to save and exit, or ':q' to quit.{ANSIColors.RESET}")
    
    existing_content = []
    if os.path.exists(filename):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                existing_content = f.read().splitlines()
            print(f"{theme['secondary']}Loaded existing file ({len(existing_content)} lines):{ANSIColors.RESET}")
            for line in existing_content:
                print(f"  {line}")
        except Exception as e:
            print(f"{ANSIColors.RED}Error reading file: {e}{ANSIColors.RESET}")

    lines = list(existing_content)
    while True:
        try:
            user_line = input(f"{theme['accent']}> {ANSIColors.RESET}")
            if user_line == ":w":
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write("\n".join(lines) + "\n")
                print(f"{ANSIColors.GREEN}File successfully saved to {filename}!{ANSIColors.RESET}")
                SYSTEM_STATE.log_event("info", f"Edited file saved: {filename}")
                break
            elif user_line == ":q":
                print(f"{ANSIColors.YELLOW}Exited editor without saving further changes.{ANSIColors.RESET}")
                break
            else:
                lines.append(user_line)
        except (KeyboardInterrupt, EOFError):
            print("\nEditor session aborted.")
            break


# ==============================================================================
# SECTION 10: FILE SYSTEM & APPLICATION MANAGEMENT
# ==============================================================================

def list_directory_contents(target_path="."):
    theme = get_current_theme()
    try:
        entries = sorted(os.listdir(target_path))
        print(f"{theme['primary']}Directory listing for: {os.path.abspath(target_path)}{ANSIColors.RESET}")
        print("-" * 50)
        for entry in entries:
            full_path = os.path.join(target_path, entry)
            if os.path.isdir(full_path):
                print(f"  {ANSIColors.BRIGHT_BLUE}[DIR]  {entry}/{ANSIColors.RESET}")
            else:
                size = os.path.getsize(full_path)
                print(f"  {ANSIColors.WHITE}[FILE] {entry:<25} ({size} bytes){ANSIColors.RESET}")
        print("-" * 50)
    except Exception as err:
        print(f"{ANSIColors.RED}ls error: {err}{ANSIColors.RESET}")

def manage_applications(args):
    apps_directory = os.path.join(os.path.dirname(__file__), "apps")
    if not os.path.exists(apps_directory):
        os.makedirs(apps_directory, exist_ok=True)

    if not args:
        print(f"{ANSIColors.BRIGHT_CYAN}=== BoosOS Installed Applications ==={ANSIColors.RESET}")
        app_files = [f for f in os.listdir(apps_directory) if f.endswith('.py')]
        if not app_files:
            print(f"{ANSIColors.YELLOW}No custom scripts found in apps/ directory.{ANSIColors.RESET}")
        else:
            for index, app in enumerate(app_files, 1):
                print(f"  {index}. {app}")
        print(f"{ANSIColors.DIM}Usage: apps launch <app_name.py>{ANSIColors.RESET}")
    else:
        if args[0] == "launch" and len(args) > 1:
            target_app = args[1]
            if not target_app.endswith(".py"):
                target_app += ".py"
            full_app_path = os.path.join(apps_directory, target_app)
            if os.path.exists(full_app_path):
                print(f"{ANSIColors.GREEN}Executing sub-application: {target_app}{ANSIColors.RESET}")
                subprocess.run([sys.executable, full_app_path])
            else:
                print(f"{ANSIColors.RED}Application not found: {target_app}{ANSIColors.RESET}")


# ==============================================================================
# SECTION 11: GRAPHICAL USER INTERFACE (TKINTER DESKTOP)
# ==============================================================================

def launch_gui_subsystem():
    if not SYSTEM_ENVIRONMENT["has_gui"]:
        print(f"{ANSIColors.RED}[Error] Graphical display server or Tkinter module is unavailable on this device.{ANSIColors.RESET}")
        print(f"{ANSIColors.YELLOW}Continuing in terminal shell mode.{ANSIColors.RESET}")
        return

    import tkinter as tk
    from tkinter import messagebox, ttk

    theme = get_current_theme()
    root = tk.Tk()
    root.title(f"BoosOS Enterprise v{SystemConfig.VERSION}")
    root.geometry("960x640")
    root.configure(bg=theme["gui_bg"])

    # Taskbar Frame
    taskbar = tk.Frame(root, bg="#000000", height=45)
    taskbar.pack(side="bottom", fill="x")

    lbl_status = tk.Label(taskbar, text=f"BoosOS v{SystemConfig.VERSION} | {SYSTEM_ENVIRONMENT['platform']}", bg="#000000", fg=theme["gui_accent"], font=("Consolas", 10, "bold"))
    lbl_status.pack(side="left", padx=15)

    # Main Workspace Canvas
    workspace = tk.Frame(root, bg=theme["gui_bg"])
    workspace.pack(expand=True, fill="both", padx=20, pady=20)

    title_label = tk.Label(workspace, text="BoosOS Desktop Subsystem", font=("Helvetica", 22, "bold"), bg=theme["gui_bg"], fg=theme["gui_fg"])
    title_label.pack(pady=20)

    # Widget Panel Frame
    panel = tk.Frame(workspace, bg=theme["gui_panel"], bd=2, relief="groove")
    panel.pack(fill="both", expand=True, padx=20, pady=10)

    info_text = f"Device Runtime: {platform.system()} ({platform.machine()})\n" \
                f"Theme Active: {SYSTEM_STATE.active_theme_name.upper()}\n" \
                f"Locale Language: {SYSTEM_STATE.active_language.upper()}\n" \
                f"Session Uptime: {calculate_uptime()}"

    lbl_info = tk.Label(panel, text=info_text, bg=theme["gui_panel"], fg=theme["gui_fg"], font=("Consolas", 11), justify="left")
    lbl_info.pack(anchor="w", padx=20, pady=20)

    def launch_gui_terminal():
        term_win = tk.Toplevel(root)
        term_win.title("BoosOS GUI Terminal Window")
        term_win.geometry("640x420")
        term_win.configure(bg="#000000")

        term_output = tk.Text(term_win, bg="#000000", fg="#00FF00", font=("Consolas", 10))
        term_output.pack(expand=True, fill="both", padx=5, pady=5)
        term_output.insert("end", "BoosOS Graphical Shell Window\nType commands below:\n\n")

        cmd_entry = tk.Entry(term_win, bg="#1a1a1a", fg="#ffffff", font=("Consolas", 10))
        cmd_entry.pack(fill="x", padx=5, pady=5)

        def handle_gui_command(event):
            c = cmd_entry.get()
            cmd_entry.delete(0, "end")
            term_output.insert("end", f"> {c}\n")
            if c == "clear":
                term_output.delete("1.0", "end")
            elif c == "exit":
                term_win.destroy()
            else:
                term_output.insert("end", f"Executed: {c}\n")

        cmd_entry.bind("<Return>", handle_gui_command)

    btn_term = tk.Button(panel, text="Open GUI Shell Window", command=launch_gui_terminal, bg=theme["gui_accent"], fg="#ffffff", font=("Helvetica", 10, "bold"), padx=10, pady=5)
    btn_term.pack(padx=20, pady=10, anchor="w")

    root.mainloop()


# ==============================================================================
# SECTION 12: COMMAND INTERPRETER & DISPATCHER ENGINE
# ==============================================================================

def process_user_command(input_string):
    input_string = input_string.strip()
    if not input_string:
        return

    SYSTEM_STATE.command_history.append(input_string)
    parts = input_string.split()
    cmd = parts[0].lower()
    args = parts[1:]

    theme = get_current_theme()

    if cmd == "help":
        print(f"{theme['primary']}{translate('help_header')}{ANSIColors.RESET}")
        print(translate("cmd_sysinfo"))
        print(translate("cmd_ls"))
        print(translate("cmd_cd"))
        print(translate("cmd_pwd"))
        print(translate("cmd_cat"))
        print(translate("cmd_edit"))
        print(translate("cmd_calc"))
        print(translate("cmd_notes"))
        print(translate("cmd_apps"))
        print(translate("cmd_gui"))
        print(translate("cmd_bench"))
        print(translate("cmd_logs"))
        print(translate("cmd_theme"))
        print(translate("cmd_lang"))
        print(translate("cmd_history"))
        print(translate("cmd_clear"))
        print(translate("cmd_exit"))

    elif cmd == "sysinfo":
        print_system_info()

    elif cmd == "ls":
        target = args[0] if args else "."
        list_directory_contents(target)

    elif cmd == "cd":
        target = args[0] if args else os.path.expanduser("~")
        try:
            os.chdir(target)
            print(f"{theme['secondary']}Directory changed to: {os.getcwd()}{ANSIColors.RESET}")
        except Exception as e:
            print(f"{ANSIColors.RED}cd error: {e}{ANSIColors.RESET}")

    elif cmd == "pwd":
        print(os.getcwd())

    elif cmd == "cat":
        if args:
            try:
                with open(args[0], 'r', encoding='utf-8') as f:
                    print(f.read())
            except Exception as e:
                print(f"{ANSIColors.RED}cat error: {e}{ANSIColors.RESET}")
        else:
            print(f"{ANSIColors.YELLOW}Usage: cat <filename>{ANSIColors.RESET}")

    elif cmd == "edit":
        if args:
            launch_micro_editor(args[0])
        else:
            print(f"{ANSIColors.YELLOW}Usage: edit <filename>{ANSIColors.RESET}")

    elif cmd == "calc":
        execute_calculator(args)

    elif cmd == "notes":
        if not args:
            if not SYSTEM_STATE.session_notes:
                print(f"{ANSIColors.YELLOW}{translate('notes_empty')}{ANSIColors.RESET}")
            else:
                print(f"{theme['primary']}--- Active Session Notes ---{ANSIColors.RESET}")
                for idx, note in enumerate(SYSTEM_STATE.session_notes, 1):
                    print(f"  {idx}. {note}")
        else:
            sub = args[0].lower()
            if sub == "add":
                text = " ".join(args[1:])
                if text:
                    SYSTEM_STATE.session_notes.append(text)
                    print(f"{ANSIColors.GREEN}{translate('notes_saved')}{ANSIColors.RESET}")
            elif sub == "clear":
                SYSTEM_STATE.session_notes.clear()
                print(f"{ANSIColors.YELLOW}{translate('notes_cleared')}{ANSIColors.RESET}")

    elif cmd == "apps":
        manage_applications(args)

    elif cmd == "gui":
        launch_gui_subsystem()

    elif cmd == "bench":
        run_cpu_benchmark()

    elif cmd == "logs":
        print(f"{theme['primary']}--- System Trace Event Logs ---{ANSIColors.RESET}")
        for log in SYSTEM_STATE.system_logs[-20:]:
            print(f"  {log}")

    elif cmd == "lang":
        if args and args[0].lower() in LOCALIZATION_DICTIONARY:
            SYSTEM_STATE.active_language = args[0].lower()
            print(f"{ANSIColors.GREEN}{translate('lang_changed')}{ANSIColors.RESET}")
        else:
            print(f"Active language: {SYSTEM_STATE.active_language}. Options: en, ro")

    elif cmd == "theme":
        if args and args[0].lower() in THEME_REGISTRY:
            SYSTEM_STATE.active_theme_name = args[0].lower()
            print(f"{ANSIColors.GREEN}{translate('theme_changed')}{SYSTEM_STATE.active_theme_name}{ANSIColors.RESET}")
        else:
            print(f"Available themes: {', '.join(THEME_REGISTRY.keys())}")

    elif cmd == "history":
        print(f"{theme['primary']}--- Command History Buffer ---{ANSIColors.RESET}")
        for idx, entry in enumerate(SYSTEM_STATE.command_history, 1):
            print(f"  {idx:3d}  {entry}")

    elif cmd == "clear":
        os.system('clear' if os.name == 'posix' else 'cls')

    elif cmd == "exit":
        print(f"{ANSIColors.YELLOW}{translate('exit_msg')}{ANSIColors.RESET}")
        SYSTEM_STATE.running = False

    else:
        print(f"{ANSIColors.RED}{translate('unknown')}{ANSIColors.RESET}")


# ==============================================================================
# SECTION 13: REPL ENTRY POINT & INITIALIZATION
# ==============================================================================

def main():
    os.system('clear' if os.name == 'posix' else 'cls')
    theme = get_current_theme()
    print(f"{theme['primary']}====================================================================={ANSIColors.RESET}")
    print(f"{ANSIColors.BOLD}{translate('welcome')}{ANSIColors.RESET}")
    print(f"{theme['badge']} | {translate('ready')}")
    print(f"{theme['primary']}====================================================================={ANSIColors.RESET}")

    SYSTEM_STATE.log_event("info", f"BoosOS v3.2.8.2 main REPL loaded. Environment: {SYSTEM_ENVIRONMENT['platform']}")

    while SYSTEM_STATE.running:
        try:
            current_theme = get_current_theme()
            prompt = current_theme["prompt"]
            user_input = input(prompt)
            process_user_command(user_input)
        except (KeyboardInterrupt, EOFError):
            print(f"\n{ANSIColors.YELLOW}{translate('exit_msg')}{ANSIColors.RESET}")
            break

if __name__ == "__main__":
    main()