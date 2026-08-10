#!/usr/bin/env python3
"""
===============================================================================
 BOOSEXPERIENCE 0.1 BETA 3 - MULTI-PLATFORM CLI ENVIRONMENT
 Developed for BoosOS Architecture
 Features: Dual-Language Engine (EN/RO), Auto-Environment Styling,
           Google Pixel Mobile Prompt, Micro-File Browser, System Utilities.
===============================================================================
"""

import os
import sys
import time
import math
import platform
import datetime
import shutil

# ==============================================================================
# 1. ENVIRONMENT & HARDWARE DETECTION ENGINE
# ==============================================================================

def detect_device_type():
    """Detects whether runtime is Android/Mobile (Termux/Pydroid) or PC Desktop."""
    is_android = (
        hasattr(sys, 'getandroidapilevel') or 
        'ANDROID_ROOT' in os.environ or 
        'PREFIX' in os.environ or
        'TERMUX_VERSION' in os.environ
    )
    return "mobile" if is_android else "pc"

ENV_TYPE = detect_device_type()

# ==============================================================================
# 2. COLOR ENGINE & PALETTE DEFINITIONS
# ==============================================================================

class Colors:
    RESET   = '\033[0m'
    BOLD    = '\033[1m'
    DIM     = '\033[2m'
    ITALIC  = '\033[3m'
    UNDER   = '\033[4m'
    
    # Standard Colors
    RED     = '\033[91m'
    GREEN   = '\033[92m'
    YELLOW  = '\033[93m'
    BLUE    = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN    = '\033[96m'
    WHITE   = '\033[97m'
    GRAY    = '\033[90m'

    # Google Pixel Distinct Branding Palette (RGB)
    P_BLUE   = '\033[38;2;66;133;244m'
    P_RED    = '\033[38;2;234;67;53m'
    P_YELLOW = '\033[38;2;251;188;5m'
    P_GREEN  = '\033[38;2;52;168;83m'

THEMES = {
    "pixel": {
        "primary": Colors.P_BLUE,
        "secondary": Colors.P_GREEN,
        "accent": Colors.P_YELLOW,
        "error": Colors.P_RED,
        "prompt": f"{Colors.P_BLUE}G{Colors.P_RED}o{Colors.P_YELLOW}o{Colors.P_BLUE}g{Colors.P_GREEN}l{Colors.P_RED}e{Colors.RESET} {Colors.P_BLUE}❯{Colors.P_GREEN}❯{Colors.RESET} ",
        "tag": f"{Colors.P_BLUE}[Pixel Mobile Engine]{Colors.RESET}"
    },
    "classic": {
        "primary": Colors.CYAN,
        "secondary": Colors.GREEN,
        "accent": Colors.YELLOW,
        "error": Colors.RED,
        "prompt": f"{Colors.CYAN}boos@pc{Colors.RESET}:{Colors.BLUE}~${Colors.RESET} ",
        "tag": f"{Colors.GRAY}[PC Desktop Environment]{Colors.RESET}"
    },
    "matrix": {
        "primary": Colors.GREEN,
        "secondary": Colors.GREEN,
        "accent": Colors.WHITE,
        "error": Colors.RED,
        "prompt": f"{Colors.GREEN}boos@matrix>{Colors.RESET} ",
        "tag": f"{Colors.GREEN}[Matrix Cyber Subsystem]{Colors.RESET}"
    }
}

# Auto-select initial theme based on platform
ACTIVE_THEME = "pixel" if ENV_TYPE == "mobile" else "classic"

# ==============================================================================
# 3. BILINGUAL LOCALIZATION SYSTEM (EN / RO)
# ==============================================================================

TRANSLATIONS = {
    "en": {
        "welcome": "BoosExperience 0.1 Beta 3 Shell Loaded",
        "ready": "System status normal. Type 'help' for available commands.",
        "unknown": "Command not recognized. Type 'help' for options.",
        "lang_set": "Language switched to English.",
        "theme_set": "Active theme set to: ",
        "hdr_help": "=== BOOSEXPERIENCE 0.1 BETA 3 COMMAND LIST ===",
        "cmd_sys": "  sysinfo         - Print hardware, OS, and runtime details",
        "cmd_ls": "  ls [path]       - List files in current or target directory",
        "cmd_cd": "  cd <path>       - Change current working directory",
        "cmd_pwd": "  pwd             - Display current absolute path",
        "cmd_cat": "  cat <file>      - Output file contents to screen",
        "cmd_calc": "  calc <expr>     - Evaluate math expression safely",
        "cmd_notes": "  notes <add/ls>  - Manage quick session notes",
        "cmd_theme": "  theme <name>    - Switch theme (pixel, classic, matrix)",
        "cmd_lang": "  lang <en/ro>    - Switch system language",
        "cmd_hist": "  history         - Display command history",
        "cmd_clear": "  clear           - Clear terminal viewport",
        "cmd_exit": "  exit            - Close shell session",
        "sys_host": "Host Machine",
        "sys_os": "Operating System",
        "sys_arch": "Architecture",
        "sys_runtime": "Environment",
        "sys_py": "Python Engine",
        "sys_time": "System Time",
        "err_calc": "Error evaluating mathematical expression.",
        "notes_empty": "No notes stored in current session.",
        "notes_saved": "Note saved to memory.",
        "notes_cleared": "All session notes cleared.",
        "exit_msg": "Shutting down BoosExperience session. Goodbye Fabi!"
    },
    "ro": {
        "welcome": "Terminal BoosExperience 0.1 Beta 3 Încărcat",
        "ready": "Stare sistem normală. Tastează 'help' pentru comenzi.",
        "unknown": "Comandă necunoscută. Tastează 'help' pentru opțiuni.",
        "lang_set": "Limba sistemului a fost schimbată în Română.",
        "theme_set": "Tema activă a fost schimbată în: ",
        "hdr_help": "=== LISTĂ COMENZI BOOSEXPERIENCE 0.1 BETA 3 ===",
        "cmd_sys": "  sysinfo         - Afișează detalii hardware, OS și runtime",
        "cmd_ls": "  ls [cale]       - Listează fișierele din director",
        "cmd_cd": "  cd <cale>       - Schimbă directorul curent de lucru",
        "cmd_pwd": "  pwd             - Afișează calea absolută curentă",
        "cmd_cat": "  cat <fișier>    - Afișează conținutul unui fișier",
        "cmd_calc": "  calc <expr>     - Evaluează o expresie matematică",
        "cmd_notes": "  notes <add/ls>  - Gestionează notițe rapide de sesiune",
        "cmd_theme": "  theme <nume>    - Schimbă tema (pixel, classic, matrix)",
        "cmd_lang": "  lang <en/ro>    - Schimbă limba sistemului",
        "cmd_hist": "  history         - Afișează istoricul comenzilor",
        "cmd_clear": "  clear           - Curăță ecranul terminalului",
        "cmd_exit": "  exit            - Închide sesiunea curentă",
        "sys_host": "Nume Host",
        "sys_os": "Sistem Operare",
        "sys_arch": "Arhitectură",
        "sys_runtime": "Mediu Rulare",
        "sys_py": "Versiune Python",
        "sys_time": "Ora Sistemului",
        "err_calc": "Eroare la evaluarea expresiei matematice.",
        "notes_empty": "Nu există notițe salvate în această sesiune.",
        "notes_saved": "Notița a fost salvată în memorie.",
        "notes_cleared": "Toate notițele au fost șterse.",
        "exit_msg": "Se închide sesiunea BoosExperience. La revedere Fabi!"
    }
}

ACTIVE_LANG = "en"

def t(key):
    """Localization lookup helper."""
    return TRANSLATIONS[ACTIVE_LANG].get(key, f"[{key}]")

# ==============================================================================
# 4. SYSTEM UTILITIES & ASCII GRAPHICS
# ==============================================================================

class SessionState:
    def __init__(self):
        self.notes = []
        self.history = []
        self.running = True

state = SessionState()

def clear_viewport():
    os.system('clear' if os.name == 'posix' else 'cls')

def get_pixel_banner():
    pb, pr, py, pg, rst = Colors.P_BLUE, Colors.P_RED, Colors.P_YELLOW, Colors.P_GREEN, Colors.RESET
    return f"""
 {pb}   G G G G   {pr} o o o o   {py} o o o o   {pb} G G G G   {pg} l {pr} e e e e {rst}
 {pb}  G          {pr}o       o  {py}o       o  {pb}G          {pg} l {pr} e       {rst}
 {pb}  G    G G G {pr}o       o  {py}o       o  {pb}G    G G G {pg} l {pr} e e e e {rst}
 {pb}  G       G  {pr}o       o  {py}o       o  {pb}G       G  {pg} l {pr} e       {rst}
 {pb}   G G G G   {pr} o o o o   {py} o o o o   {pb}  G G G G   {pg} l {pr} e e e e {rst}
"""

def get_pc_banner():
    p = THEMES[ACTIVE_THEME]["primary"]
    rst = Colors.RESET
    return f"""
{p}  ____                  ____   _____ 
 |  _ \  ___   ___  ___/ ___| | ____|
 | |_) |/ _ \ / _ \/ __\___ \ |  _|  
 |  _ <| (_) | (_) \__ \___) || |___ 
 |_| \_\\___/ \___/|___/____/ |_____|{rst}
"""

def print_sysinfo():
    theme = THEMES[ACTIVE_THEME]
    print(get_pixel_banner() if ENV_TYPE == "mobile" else get_pc_banner())
    print(f"{theme['primary']}{'='*55}{Colors.RESET}")
    print(f"{theme['secondary']}{t('sys_host')}:{Colors.RESET} {platform.node()}")
    print(f"{theme['secondary']}{t('sys_os')}:{Colors.RESET} {platform.system()} {platform.release()}")
    print(f"{theme['secondary']}{t('sys_arch')}:{Colors.RESET} {platform.machine()}")
    print(f"{theme['secondary']}{t('sys_runtime')}:{Colors.RESET} {ENV_TYPE.upper()} {theme['tag']}")
    print(f"{theme['secondary']}{t('sys_py')}:{Colors.RESET} Python {platform.python_version()}")
    print(f"{theme['secondary']}{t('sys_time')}:{Colors.RESET} {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{theme['primary']}{'='*55}{Colors.RESET}")

def safe_calc(expr):
    """Safely evaluates math expressions without arbitrary code execution."""
    try:
        allowed = {"math": math, "abs": abs, "round": round, "pow": pow, "sqrt": math.sqrt}
        compiled = compile(expr, "<string>", "eval")
        for name in compiled.co_names:
            if name not in allowed:
                raise NameError(f"Function {name} restricted.")
        res = eval(compiled, {"__builtins__": {}}, allowed)
        print(f"{Colors.GREEN}= {res}{Colors.RESET}")
    except Exception:
        print(f"{Colors.RED}{t('err_calc')}{Colors.RESET}")

def handle_notes(args):
    if not args:
        if not state.notes:
            print(f"{Colors.YELLOW}{t('notes_empty')}{Colors.RESET}")
        else:
            print(f"{Colors.CYAN}--- Session Notes ---{Colors.RESET}")
            for idx, note in enumerate(state.notes, 1):
                print(f"{idx}. {note}")
    else:
        sub = args[0].lower()
        if sub == "add":
            text = " ".join(args[1:])
            if text:
                state.notes.append(text)
                print(f"{Colors.GREEN}{t('notes_saved')}{Colors.RESET}")
        elif sub == "clear":
            state.notes.clear()
            print(f"{Colors.YELLOW}{t('notes_cleared')}{Colors.RESET}")

def list_files(target_dir="."):
    try:
        entries = os.listdir(target_dir)
        for entry in sorted(entries):
            full_path = os.path.join(target_dir, entry)
            if os.path.isdir(full_path):
                print(f"{Colors.BLUE}{entry}/{Colors.RESET}")
            else:
                print(f"{Colors.WHITE}{entry}{Colors.RESET}")
    except Exception as e:
        print(f"{Colors.RED}ls: {e}{Colors.RESET}")

# ==============================================================================
# 5. COMMAND INTERPRETER & DISPATCHER
# ==============================================================================

def process_command(user_cmd):
    global ACTIVE_LANG, ACTIVE_THEME
    
    parts = user_cmd.strip().split()
    if not parts:
        return

    cmd = parts[0].lower()
    args = parts[1:]

    state.history.append(user_cmd)

    if cmd == "help":
        print(f"{THEMES[ACTIVE_THEME]['primary']}{t('hdr_help')}{Colors.RESET}")
        print(t("cmd_sys"))
        print(t("cmd_ls"))
        print(t("cmd_cd"))
        print(t("cmd_pwd"))
        print(t("cmd_cat"))
        print(t("cmd_calc"))
        print(t("cmd_notes"))
        print(t("cmd_theme"))
        print(t("cmd_lang"))
        print(t("cmd_hist"))
        print(t("cmd_clear"))
        print(t("cmd_exit"))

    elif cmd == "sysinfo":
        print_sysinfo()

    elif cmd == "ls":
        target = args[0] if args else "."
        list_files(target)

    elif cmd == "cd":
        target = args[0] if args else os.path.expanduser("~")
        try:
            os.chdir(target)
        except Exception as e:
            print(f"{Colors.RED}cd: {e}{Colors.RESET}")

    elif cmd == "pwd":
        print(os.getcwd())

    elif cmd == "cat":
        if args:
            try:
                with open(args[0], 'r', encoding='utf-8') as f:
                    print(f.read())
            except Exception as e:
                print(f"{Colors.RED}cat: {e}{Colors.RESET}")

    elif cmd == "calc":
        if args:
            safe_calc(" ".join(args))

    elif cmd == "notes":
        handle_notes(args)

    elif cmd == "lang":
        if args and args[0].lower() in TRANSLATIONS:
            ACTIVE_LANG = args[0].lower()
            print(f"{Colors.GREEN}{t('lang_set')}{Colors.RESET}")
        else:
            print(f"Active language: {ACTIVE_LANG}. Usage: lang <en/ro>")

    elif cmd == "theme":
        if args and args[0].lower() in THEMES:
            ACTIVE_THEME = args[0].lower()
            print(f"{Colors.GREEN}{t('theme_set')}{ACTIVE_THEME}{Colors.RESET}")
        else:
            print(f"Available themes: {', '.join(THEMES.keys())}")

    elif cmd == "history":
        for i, h in enumerate(state.history, 1):
            print(f" {i}  {h}")

    elif cmd == "clear":
        clear_viewport()

    elif cmd == "exit":
        print(f"{Colors.YELLOW}{t('exit_msg')}{Colors.RESET}")
        state.running = False

    else:
        print(f"{Colors.RED}{t('unknown')}{Colors.RESET}")

# ==============================================================================
# 6. MAIN REPL ENTRY POINT
# ==============================================================================

def main():
    clear_viewport()
    theme = THEMES[ACTIVE_THEME]
    print(f"{theme['primary']}======================================================={Colors.RESET}")
    print(f"{Colors.BOLD}{t('welcome')}{Colors.RESET}")
    print(f"{theme['tag']} | {t('ready')}")
    print(f"{theme['primary']}======================================================={Colors.RESET}")

    while state.running:
        try:
            prompt_str = THEMES[ACTIVE_THEME]["prompt"]
            user_input = input(prompt_str)
            process_command(user_input)
        except (KeyboardInterrupt, EOFError):
            print(f"\n{Colors.YELLOW}{t('exit_msg')}{Colors.RESET}")
            break

if __name__ == "__main__":
    main()