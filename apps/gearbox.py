import time
import os
import sys

IS_WINDOWS = sys.platform.startswith("win")

# Activăm culorile în terminalul Windows
if IS_WINDOWS:
    os.system("")

# Coduri de culoare ANSI
RESET = "\033[0m"
RED = "\033[91;1m"      # Roșu aprins pentru explozie / detonație
YELLOW = "\033[93;1m"   # Galben pentru scânteie
CYAN = "\033[96m"       # Albastru deschis pentru schimbător
GREEN = "\033[92;1m"    # Verde pentru bord / informații
BOLD = "\033[1m"

def clear():
    os.system("cls" if IS_WINDOWS else "clear")

def render_gearbox(current_gear):
    g = {i: str(i) for i in range(1, 7)}
    g['N'] = 'N'
    
    if current_gear in g:
        g[current_gear] = f"{CYAN}[{current_gear}]{RESET}"

    shifter = f"""
    --- H-SHIFTER ---
      {g[1]:<12}   {g[3]:<12}   {g[5]:<12}
      |            |            |
      +------------+------------+
      |            |            |
      {g[2]:<12}   {g[4]:<12}   {g[6]:<12}

     [ Current: {CYAN}{current_gear}{RESET} | Neutral: N | Quit: Q ]
    """
    return shifter

def render_engine(gear, stroke):
    # Când stroke == 0, pistonul este sus și are loc detonația (Roșu)
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
    
    # Delays (viteza de ciclu a pistonului în funcție de treaptă)
    delays = {
        "N": 0.4,
        1: 0.30,
        2: 0.22,
        3: 0.16,
        4: 0.11,
        5: 0.07,
        6: 0.04
    }

    clear()
    print(f"{GREEN}=== MANUAL GEARBOX & DYNAMIC PISTON SIMULATOR ==={RESET}")
    print("Introdu treapta (1-6), N pentru liber sau Q pentru ieșire.")
    time.sleep(1.5)

    try:
        while True:
            clear()
            current_delay = delays.get(gear, 0.3)
            rpm = int(1 / current_delay * 350) # Estimare RPM realistă pentru simulator
            
            print(f"Treaptă: {CYAN}{gear}{RESET} | Turație Motor: {GREEN}{rpm} RPM{RESET}\n")
            print(render_gearbox(gear))
            print(render_engine(gear, stroke))
            
            print(f"\n{BOLD}Comandă (1-6, N, Q): {RESET}", end="", flush=True)

            # Alternăm starea pistonului (sus/jos)
            stroke = (stroke + 1) % 2
            
            # Verificăm input-ul non-blocant în funcție de timp
            start_wait = time.time()
            while time.time() - start_wait < current_delay:
                if IS_WINDOWS:
                    import msvcrt
                    if msvcrt.kbhit():
                        ch = msvcrt.getch().decode('utf-8', errors='ignore').lower()
                        if ch in ['1', '2', '3', '4', '5', '6']:
                            gear = int(ch)
                        elif ch == 'n':
                            gear = "N"
                        elif ch == 'q':
                            return
                else:
                    import select
                    dr, _, _ = select.select([sys.stdin], [], [], 0.02)
                    if dr:
                        ch = sys.stdin.read(1).lower()
                        if ch in ['1', '2', '3', '4', '5', '6']:
                            gear = int(ch)
                        elif ch == 'n':
                            gear = "N"
                        elif ch == 'q':
                            return
                time.sleep(0.01)

    except KeyboardInterrupt:
        pass

# Apel direct pentru a rula corect în mediul BoosOS exec()
main()