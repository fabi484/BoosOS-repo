import time
import os
import sys

IS_WINDOWS = sys.platform.startswith("win")

# Activăm culorile în terminalul Windows dacă este nevoie
if IS_WINDOWS:
    os.system("")

# Coduri de culoare ANSI
RESET = "\033[0m"
RED = "\033[91;1m"      # Roșu aprins pentru explozie / aprindere
YELLOW = "\033[93;1m"   # Galben pentru scânteie
CYAN = "\033[96m"       # Albastru deschis pentru schimbător
BOLD = "\033[1m"

def clear():
    os.system("cls" if IS_WINDOWS else "clear")

def render_gearbox(current_gear):
    g = {i: str(i) for i in range(1, 7)}
    g['N'] = 'N'
    
    if current_gear in g:
        g[current_gear] = f"{CYAN}[{current_gear}]{RESET}"

    shifter = f"""
    --- GEAR SHIFTER ---
      {g[1]:<12}   {g[3]:<12}   {g[5]:<12}
      |            |            |
      +------------+------------+
      |            |            |
      {g[2]:<12}   {g[4]:<12}   {g[6]:<12}

     [ Neutral: N ]
    """
    return shifter

def render_engine(gear, stroke):
    # Când stroke == 0, pistonul este sus și are loc EXPLOZIA (Culoare Roșie)
    if stroke == 0:
        spark = f"{YELLOW}( * DETONATION * ){RESET}"
        chamber_color = RED
        piston_top = f"{RED}   |==========|{RESET}"
        piston_mid = "   |          |"
    else:
        spark = " (   Spark    ) "
        chamber_color = RESET
        piston_top = "   |          |"
        piston_mid = f"{BOLD}   |==========|{RESET}"
    
    engine_ascii = f"""
    --- ENGINE CYLINDER ---
         /------\\
        | {spark} |
        +--------+
{chamber_color}        |        |
     {piston_top}{chamber_color}
     {piston_mid}{chamber_color}
        |   ||   |
         \\  ||  /
          \\_||_/
            ||
          (CRANK){RESET}
    """
    return engine_ascii

def main():
    gear = "N"
    stroke = 0
    
    delays = {
        "N": 0.5,
        1: 0.35,
        2: 0.25,
        3: 0.18,
        4: 0.12,
        5: 0.08,
        6: 0.04
    }

    clear()
    print("=== MANUAL GEARBOX & DYNAMIC PISTON SIMULATOR ===")
    print("Comenzi: 1-6 pentru viteze, N pentru liber, Q pentru ieșire.")
    time.sleep(1.5)

    try:
        while True:
            clear()
            rpm = int(1 / delays[gear] * 60)
            print(f"Treaptă selectată: {CYAN}{gear}{RESET} | RPM Piston: {BOLD}{rpm} RPM{RESET}\n")
            
            print(render_gearbox(gear))
            print(render_engine(gear, stroke))
            print("\nSchimbă viteza (1-6, N, Q de ieșire): ")

            # Schimbăm faza pistonului (0 = sus/detonație roșie, 1 = jos)
            stroke = (stroke + 1) % 2
            
            time.sleep(delays[gear])

            # Citire input din tastatură
            if IS_WINDOWS:
                import msvcrt
                if msvcrt.kbhit():
                    ch = msvcrt.getch().decode('utf-8', errors='ignore').lower()
                    if ch in ['1', '2', '3', '4', '5', '6']:
                        gear = int(ch)
                    elif ch == 'n':
                        gear = "N"
                    elif ch == 'q':
                        break
            else:
                import select
                dr, _, _ = select.select([sys.stdin], [], [], 0)
                if dr:
                    ch = sys.stdin.read(1).lower()
                    if ch in ['1', '2', '3', '4', '5', '6']:
                        gear = int(ch)
                    elif ch == 'n':
                        gear = "N"
                    elif ch == 'q':
                        break

    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()