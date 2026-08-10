import os
import sys
import time
import math
import platform
import datetime
import shutil

# ==============================================================================
# 1. ENVIRONMENT & PLATFORM DETECTION
# ==============================================================================

def detect_environment():
    """Detects whether BoosExperience is running on Android/Mobile or Desktop PC."""
    is_android = hasattr(sys, 'getandroidapilevel') or 'ANDROID_ROOT' in os.environ or 'PREFIX' in os.environ
    return "mobile" if is_android else "pc"

ENV_TYPE = detect_environment()

# ==============================================================================
# 2. COLOR PALETTES & THEME ENGINE
# ==============================================================================

class Colors:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    
    # Standard ANSI Colors
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    GRAY = '\033[90m'

    # Google Pixel Distinct Colors
    P_BLUE = '\033[38;2;66;133;244m'
    P_RED = '\033[38;2;234;67;53m'
    P_YELLOW = '\033[38;2;251;188;5m'
    P_GREEN = '\033[38;2;52;168;83m'

THEMES = {
    "pixel": {
        "primary": Colors.P_BLUE,
        "secondary": Colors.P_GREEN,
        "accent": Colors.P_YELLOW,
        "error": Colors.P_RED,
        "prompt": f"{Colors.P_BLUE}G{Colors.P_RED}o{Colors.P_YELLOW}o{Colors.P_BLUE}g{Colors.P_GREEN}l{Colors.P_RED}e{Colors.RESET} {Colors.P_BLUE}❯{Colors.P_GREEN}❯{Colors.RESET} ",
        "banner_tag": f"{Colors.P_BLUE}[Google Pixel Mobile Mode]{Colors.RESET}"
    },
    "classic": {
        "primary": Colors.CYAN,
        "secondary": Colors.GREEN,
        "accent": Colors.YELLOW,
        "error": Colors.RED,
        "prompt": f"{Colors.CYAN}boos@pc{Colors.RESET}:{Colors.BLUE}~${Colors.RESET} ",
        "banner_tag": f"{Colors.GRAY}[Desktop PC Mode - Classic]{Colors.RESET}"
    },
    "matrix": {
        "primary": Colors.GREEN,
        "secondary": Colors.GREEN,
        "accent": Colors.WHITE,
        "error": Colors.RED,
        "prompt": f"{Colors.GREEN}matrix@boos>{Colors.RESET} ",
        "banner_tag": f"{Colors.GREEN}[Matrix Hacker Theme]{Colors.RESET}"
    }
}

# Default theme selection based on environment
ACTIVE_THEME = "pixel" if ENV_TYPE == "mobile" else "classic"

# ==============================================================================
# 3. BILINGUAL TRANSLATION SYSTEM (EN / RO)
# ==============================================================================

TRANSLATIONS = {
    "en": {
        "welcome": "BoosExperience 0.1 Beta 3 - Environment Loaded",
        "system_ready": "System state normal. Type 'help' for commands.",
        "prompt_unknown": "Command not found. Type 'help' for available utilities.",
        "lang_changed": "Language switched to English.",
        "theme_changed": "Theme changed to: ",
        "help_header": "--- BOOSEXPERIENCE 0.1 BETA 3 COMMAND LIST ---",
        "help_sys": "  sysinfo   - Display system hardware & OS details",
        "help_ls": "  ls        - List contents of current directory",
        "help_cd": "  cd <dir>  - Change working directory",
        "help_pwd": "  pwd       - Display absolute path of current directory",
        "help_cat": "  cat <file>- Output contents of a file",
        "help_calc": "  calc <expr>- Evaluate mathematical expression",
        "help_notes": "  notes     - Manage local quick notes (add/list/clear)",
        "help_theme": "  theme     - Switch UI theme (pixel/classic/matrix)",
        "help_lang": "  lang      - Switch language (en/ro)",
        "help_clear": "  clear     - Clear terminal screen",
        "help_exit": "  exit      - Close BoosExperience session",
        "sys_host": "Hostname",
        "sys_os": "Operating System",
        "sys_arch": "Architecture",
        "sys_env": "Runtime Mode",
        "sys_py": "Python Version",
        "calc_error": "Invalid math expression.",
        "notes_empty": "No notes saved.",
        "notes_saved": "Note saved successfully.",
        "notes_cleared": "All notes cleared.",
        "exit_msg": "Shutting down BoosExperience session. Goodbye Fabi!"
    },
    "ro": {
        "welcome": "BoosExperience 0.1 Beta 3 - Mediu Încărcat",
        "system_ready": "Stare sistem normală. Tastează 'help' pentru comenzi.",
        "prompt_unknown": "Comanda nu a fost găsită. Tastează 'help' pentru opțiuni.",
        "lang_changed": "Limba a fost schimbată în Română.",
        "theme_changed": "Tema a fost schimbată în: ",
        "help_header": "--- LISTĂ COMENZI BOOSEXPERIENCE 0.1 BETA 3 ---",
        "help_sys": "  sysinfo   - Afișează detalii despre hardware și OS",
        "help_ls": "  ls        - Afișează conținutul directorului curent",
        "help_cd": "  cd <dir>  - Schimbă directorul de lucru",
        "help_pwd": "  pwd       - Afișează calea absolută curentă",
        "help_cat": "  cat <fisi>- Afișează conținutul unui fișier",
        "help_calc": "  calc <expr>- Evaluează o expresie matematică",
        "help_notes": "  notes     - Gestionează notițe rapide (add/list/clear)",
        "help_theme": "  theme     - Schimbă tema UI (pixel/classic/matrix)",
        "help_lang": "  lang      - Schimbă limba (en/ro)",
        "help_clear": "  clear     - Curăță ecranul terminalului",
        "help_exit": "  exit      - Închide sesiunea BoosExperience",
        "sys_host": "Nume Host",
        "sys_os": "Sistem de Operare",
        "sys_arch": "Arhitectură",
        "sys_env": "Mod Rulare",
        "sys_py": "Versiune Python",
        "calc_error": "Expresie matematică invalidă.",
        "notes_empty": "Nu există notițe salvate.",
        "notes_saved": "Notiță salvată cu succes.",
        "notes_cleared": "Toate notițele au fost șterse.",
        "exit_msg": "Se închide sesiunea BoosExperience. La revedere Fabi!"
    }
}

ACTIVE_LANG = "en"

def t(key):
    """Retrieves string based on active language."""
    return TRANSLATIONS[ACTIVE_LANG].get(key, f"[{key}]")

# ==============================================================================
# 4. SYSTEM UTILITIES & CORE MODULES
# ==============================================================================

class ShellState:
    def __init__(self):
        self.notes = []
        self.history = []
        self.running = True

state = ShellState()

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def get_pixel_ascii():
    p_blue = Colors.P_BLUE
    p_red = Colors.P_RED
    p_yellow = Colors.P_YELLOW
    p_green = Colors.P_GREEN
    rst = Colors.RESET
    
    return f"""
 {p_blue}  G G G G   {p_red} o o o o   {p_yellow} o o o o   {p_blue} G G G G   {p_green} l {p_red} e e e e {rst}
 {p_blue} G          {p_red}o       o  {p_yellow}o       o  {p_blue}G          {p_green} l {p_red} e       {rst}
 {p_blue} G    G G G {p_red}o       o  {p_yellow}o       o  {p_blue}G    G G G {p_green} l {p_red} e e e e {rst}
 {p_blue} G       G  {p_red}o       o  {p_yellow}o       o  {p_blue}G       G  {p_green} l {p_red} e       {rst}
 {p_blue}  G G G G   {p_red} o o o o   {p_yellow} o o o o   {p_blue}  G G G G   {p_green} l {p_red} e e e e {rst}
"""

def get_pc_ascii():
    primary = THEMES[ACTIVE_THEME]["primary"]
    rst = Colors.RESET
    return f"""
{primary}  ____                  ____   _____ 
 |  _ \  ___   ___  ___/ ___| | ____|
 | |_) |/ _ \ / _ \/ __\___ \ |  _|  
 |  _ <| (_) | (_) \__ \___) || |___ 
 |_| \_\\___/ \___/|___/____/ |_____|{rst}
"""

def display_sysinfo():
    theme = THEMES[ACTIVE_THEME]
    if ENV_TYPE == "mobile":
        print(get_pixel_ascii())
    else:
        print(get_pc_ascii())
        
    print(f"{theme['primary']}{'='*45}{Colors.RESET}")
    print(f"{theme['secondary']}{t('sys_host')}:{Colors.RESET} {platform.node()}")
    print(f"{theme['secondary']}{t('sys_os')}:{Colors.RESET} {platform.system()} {platform.release()}")
    print(f"{theme['secondary']}{t('sys_arch')}:{Colors.RESET} {platform.machine()}")
    print(f"{theme['secondary']}{t('sys_env')}:{Colors.RESET} {ENV_TYPE.upper()} ({theme['banner_tag']})")
    print(f"{theme['secondary']}{t('sys_py')}:{Colors.RESET} {platform.python_version()}")
    print(f"{theme['primary']}{'='*45}{Colors.RESET}")

def evaluate_calc(expr):
    """Safe math evaluator without standard eval security flaws."""
    try:
        allowed_names = {"math": math, "abs": abs, "round": round}
        code = compile(expr, "<string>", "eval")
        for name in code.co_names:
            if name not in allowed_names:
                raise NameError(f"Use of {name} is restricted.")
        result = eval(code, {"__builtins__": {}}, allowed_names)
        print(f"{Colors.GREEN}= {result}{Colors.RESET}")
    except Exception:
        print(f"{Colors.RED}{t('calc_error')}{Colors.RESET}")

def manage_notes(args):
    if not args:
        if not state.notes:
            print(f"{Colors.YELLOW}{t('notes_empty')}{Colors.RESET}")
        else:
            print(f"{Colors.CYAN}--- Saved Notes ---{Colors.RESET}")
            for idx, note in enumerate(state.notes, 1):
                print(f"{idx}. {note}")
    else:
        subcmd = args[0].lower()
        if subcmd == "add":
            note_text = " ".join(args[1:])
            if note_text:
                state.notes.append(note_text)
                print(f"{Colors.GREEN}{t('notes_saved')}{Colors.RESET}")
        elif subcmd == "clear":
            state.notes.clear()
            print(f"{Colors.YELLOW}{t('notes_cleared')}{Colors.RESET}")

def list_dir():
    try:
        items = os.listdir(".")
        for item in sorted(items):
            if os.path.isdir(item):
                print(f"{Colors.BLUE}{item}/{Colors.RESET}")
            else:
                print(f"{Colors.WHITE}{item}{Colors.RESET}")
    except Exception as e:
        print(f"{Colors.RED}Error listing dir: {e}{Colors.RESET}")

def change_dir(path):
    try:
        os.chdir(path)
    except Exception as e:
        print(f"{Colors.RED}cd: {e}{Colors.RESET}")

def cat_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            print(f.read())
    except Exception as e:
        print(f"{Colors.RED}cat: {e}{Colors.RESET}")

# ==============================================================================
# 5. COMMAND DISPATCHER & PARSER
# ==============================================================================

def execute_command(user_input):
    global ACTIVE_LANG, ACTIVE_THEME
    
    parts = user_input.strip().split()
    if not parts:
        return

    cmd = parts[0].lower()
    args = parts[1:]

    state.history.append(user_input)

    if cmd == "help":
        print(f"{THEMES[ACTIVE_THEME]['primary']}{t('help_header')}{Colors.RESET}")
        print(t("help_sys"))
        print(t("help_ls"))
        print(t("help_cd"))
        print(t("help_pwd"))
        print(t("help_cat"))
        print(t("help_calc"))
        print(t("help_notes"))
        print(t("help_theme"))
        print(t("help_lang"))
        print(t("help_clear"))
        print(t("help_exit"))

    elif cmd == "sysinfo":
        display_sysinfo()

    elif cmd == "ls":
        list_dir()

    elif cmd == "cd":
        if args:
            change_dir(args[0])
        else:
            change_dir(os.path.expanduser("~"))

    elif cmd == "pwd":
        print(os.getcwd())

    elif cmd == "cat":
        if args:
            cat_file(args[0])

    elif cmd == "calc":
        if args:
            evaluate_calc(" ".join(args))

    elif cmd == "notes":
        manage_notes(args)

    elif cmd == "lang":
        if args:
            lang_arg = args[0].lower()
            if lang_arg in TRANSLATIONS:
                ACTIVE_LANG = lang_arg
                print(f"{Colors.GREEN}{t('lang_changed')}{Colors.RESET}")
        else:
            print(f"Current language: {ACTIVE_LANG}. Use 'lang en' or 'lang ro'")

    elif cmd == "theme":
        if args:
            theme_arg = args[0].lower()
            if theme_arg in THEMES:
                ACTIVE_THEME = theme_arg
                print(f"{Colors.GREEN}{t('theme_changed')}{ACTIVE_THEME}{Colors.RESET}")
        else:
            print(f"Available themes: {', '.join(THEMES.keys())}")

    elif cmd == "clear":
        clear_screen()

    elif cmd == "exit":
        print(f"{Colors.YELLOW}{t('exit_msg')}{Colors.RESET}")
        state.running = False

    else:
        print(f"{Colors.RED}{t('prompt_unknown')}{Colors.RESET}")

# ==============================================================================
# 6. MAIN ENVIRONMENT ENTRY POINT
# ==============================================================================

def print_banner():
    theme = THEMES[ACTIVE_THEME]
    print(f"{theme['primary']}====================================================={Colors.RESET}")
    print(f"{Colors.BOLD}{t('welcome')}{Colors.RESET}")
    print(f"{theme['banner_tag']}")
    print(f"{t('system_ready')}")
    print(f"{theme['primary']}====================================================={Colors.RESET}")

def main():
    clear_screen()
    print_banner()

    while state.running:
        try:
            current_prompt = THEMES[ACTIVE_THEME]["prompt"]
            user_input = input(current_prompt)
            execute_command(user_input)
        except (KeyboardInterrupt, EOFError):
            print(f"\n{Colors.YELLOW}{t('exit_msg')}{Colors.RESET}")
            break

if __name__ == "__main__":
    main()