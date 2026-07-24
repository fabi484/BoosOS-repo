import os
import sys
import time
import platform
import datetime

# Check hardware stats availability
try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False

def run_boosfetch():
    # Context variables from BoosOS runtime environment
    user = current_user if 'current_user' in globals() and current_user else "guest"
    u_dir = user_dir if 'user_dir' in globals() and user_dir else "user_saves/guest"
    
    # Detect dynamically the active BoosOS version from the running kernel/class instance
    os_version = "Unknown"
    # Search frame stack for active BoosOS instance
    try:
        frame = sys._getframe()
        while frame:
            if 'self' in frame.f_locals and hasattr(frame.f_locals['self'], 'version'):
                os_version = f"v{frame.f_locals['self'].version}"
                break
            frame = frame.f_back
    except Exception:
        pass

    # Calculate installed apps
    apps_path = os.path.join(u_dir, "installed_apps")
    app_count = 0
    if os.path.exists(apps_path):
        app_count = len([f for f in os.listdir(apps_path) if f.endswith('.py')])

    # Calculate Uptime
    uptime_seconds = int(time.time() - psutil.boot_time()) if HAS_PSUTIL else 0
    uptime_str = str(datetime.timedelta(seconds=uptime_seconds)) if HAS_PSUTIL else "N/A"

    # Hardware stats
    if HAS_PSUTIL:
        cpu_usage = f"{psutil.cpu_percent()}%"
        ram = psutil.virtual_memory()
        ram_str = f"{ram.used // (1024**2)}MB / {ram.total // (1024**2)}MB ({ram.percent}%)"
        try:
            bat = psutil.sensors_battery()
            bat_str = f"{bat.percent}% {'(Charging)' if bat.power_plugged else '(Discharging)'}" if bat else "N/A"
        except (PermissionError, AttributeError):
            bat_str = "N/A"
    else:
        cpu_usage = "N/A (psutil required)"
        ram_str = "N/A (psutil required)"
        bat_str = "N/A"

    # Terminal ANSI Colors
    C_CYAN   = "\033[96m"
    C_BLUE   = "\033[94m"
    C_GREEN  = "\033[92m"
    C_YELLOW = "\033[93m"
    C_MAG    = "\033[95m"
    C_WHITE  = "\033[97m"
    C_BOLD   = "\033[1m"
    C_RESET  = "\033[0m"

    # Custom ASCII Art (Square Box with 'B' Logo)
    logo = [
        f"{C_CYAN}┌─────────────┐{C_RESET}",
        f"{C_CYAN}│  ██████╗    │{C_RESET}",
        f"{C_CYAN}│  ██╔══██╗   │{C_RESET}",
        f"{C_CYAN}│  ██████╔╝   │{C_RESET}",
        f"{C_CYAN}│  ██╔══██╗   │{C_RESET}",
        f"{C_CYAN}│  ██████╔╝   │{C_RESET}",
        f"{C_CYAN}└─────────────┘{C_RESET}"
    ]

    # Data items to render
    info = [
        f"{C_BOLD}{C_GREEN}{user}{C_WHITE}@{C_GREEN}BoosOS{C_RESET}",
        f"{C_CYAN}----------------------------------{C_RESET}",
        f"{C_BOLD}{C_YELLOW}OS         :{C_RESET} BoosOS {os_version}",
        f"{C_BOLD}{C_YELLOW}Host OS    :{C_RESET} {platform.system()} {platform.release()} ({platform.machine()})",
        f"{C_BOLD}{C_YELLOW}Python     :{C_RESET} {platform.python_version()} ({platform.python_implementation()})",
        f"{C_BOLD}{C_YELLOW}Active User:{C_RESET} {user}",
        f"{C_BOLD}{C_YELLOW}Mapped Drive:{C_RESET} C:\\ ({u_dir})",
        f"{C_BOLD}{C_YELLOW}Uptime     :{C_RESET} {uptime_str}",
        f"{C_BOLD}{C_YELLOW}Packages   :{C_RESET} {app_count} (BoosOS apps)",
        f"{C_BOLD}{C_YELLOW}CPU Usage  :{C_RESET} {cpu_usage}",
        f"{C_BOLD}{C_YELLOW}Memory     :{C_RESET} {ram_str}",
        f"{C_BOLD}{C_YELLOW}Battery    :{C_RESET} {bat_str}",
        "",
        f"{C_CYAN}███{C_GREEN}███{C_YELLOW}███{C_BLUE}███{C_MAG}███{C_WHITE}███{C_RESET}"
    ]

    print("\n")
    max_lines = max(len(logo), len(info))
    for i in range(max_lines):
        left = logo[i] if i < len(logo) else "               "
        right = info[i] if i < len(info) else ""
        print(f" {left}   {right}")
    print("\n")

run_boosfetch()