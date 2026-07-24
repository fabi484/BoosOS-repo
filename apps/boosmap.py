import os

def run_boosmap():
    # ANSI Color Codes
    C_BLUE   = "\033[94m"
    C_GREEN  = "\033[92m"
    C_YELLOW = "\033[93m"
    C_CYAN   = "\033[96m"
    C_WHITE  = "\033[97m"
    C_BOLD   = "\033[1m"
    C_RESET  = "\033[0m"

    # World Map ASCII Data
    world_map = [
        f"{C_CYAN}  80°N ┌────────────────────────────────────────────────────────────────────────┐{C_RESET}",
        f"{C_CYAN}       │{C_RESET} {C_WHITE}..''..{C_RESET}                   {C_WHITE}.'.{C_RESET}                                       {C_CYAN}│{C_RESET}",
        f"{C_CYAN}  60°N │{C_RESET}  {C_GREEN}.:::..{C_RESET}                 {C_GREEN}.'  '.{C_RESET}      {C_GREEN}.:::..{C_RESET}                          {C_CYAN}│{C_RESET}",
        f"{C_CYAN}       │{C_RESET} {C_GREEN}:  .:::..{C_RESET}              {C_GREEN}:      :...::::'   :::..{C_RESET}               {C_CYAN}│{C_RESET}",
        f"{C_CYAN}  40°N │{C_RESET} {C_GREEN}':::..'''{C_RESET}             {C_GREEN}:     ..::::::::.  ':::::{C_RESET}  {C_GREEN}..{C_RESET}             {C_CYAN}│{C_RESET}",
        f"{C_CYAN}       │{C_RESET}    {C_GREEN}'::{C_RESET}                 {C_GREEN}':::...:::::::::::''  '::{C_RESET}  {C_GREEN}::::.{C_RESET}          {C_CYAN}│{C_RESET}",
        f"{C_CYAN}  20°N │{C_RESET}       {C_GREEN}'{C_RESET}                      {C_GREEN}::. .::::'        '   .::::::{C_RESET}        {C_CYAN}│{C_RESET}",
        f"{C_CYAN}       │{C_RESET}                            {C_GREEN}:::::::''{C_RESET}            {C_GREEN}::::::::{C_RESET}        {C_CYAN}│{C_RESET}",
        f"{C_CYAN}   0°  │{C_RESET}               {C_GREEN}....{C_RESET}         {C_GREEN}::::::'{C_RESET}             {C_GREEN}':::::'{C_RESET}  {C_GREEN}..{C_RESET}     {C_CYAN}│{C_RESET}",
        f"{C_CYAN}       │{C_RESET}              {C_GREEN}.::::.{C_RESET}        {C_GREEN}':::::'{C_RESET}                     {C_GREEN}::::.{C_RESET}   {C_CYAN}│{C_RESET}",
        f"{C_CYAN}  20°S │{C_RESET}             {C_GREEN}:::::::{C_RESET}         {C_GREEN}::::'{C_RESET}                      {C_GREEN}::::::{C_RESET}   {C_CYAN}│{C_RESET}",
        f"{C_CYAN}       │{C_RESET}              {C_GREEN}:::::'{C_RESET}          {C_GREEN}':'{C_RESET}                        {C_GREEN}':::::{C_RESET}   {C_CYAN}│{C_RESET}",
        f"{C_CYAN}  40°S │{C_RESET}               {C_GREEN}:::'{C_RESET}                                              {C_GREEN}':'{C_RESET}    {C_CYAN}│{C_RESET}",
        f"{C_CYAN}       │{C_RESET}                {C_GREEN}'{C_RESET}                                                    {C_CYAN}│{C_RESET}",
        f"{C_CYAN}  60°S │{C_RESET}     {C_WHITE}..................................................................{C_RESET}   {C_CYAN}│{C_RESET}",
        f"{C_CYAN}  80°S └────────────────────────────────────────────────────────────────────────┘{C_RESET}",
        f"{C_YELLOW}        160°W  120°W   80°W   40°W    0°    40°E   80°E   120°E  160°E{C_RESET}"
    ]

    capitals = {
        "romania": ("București", "44.4° N, 26.1° E", "Europa"),
        "usa": ("Washington D.C.", "38.9° N, 77.0° W", "America de Nord"),
        "germany": ("Berlin", "52.5° N, 13.4° E", "Europa"),
        "japan": ("Tokyo", "35.6° N, 139.6° E", "Asia"),
        "uk": ("Londra", "51.5° N, 0.1° W", "Europa"),
        "france": ("Paris", "48.8° N, 2.3° E", "Europa"),
        "australia": ("Canberra", "35.2° S, 149.1° E", "Oceania"),
        "brazil": ("Brasília", "15.8° S, 47.9° W", "America de Sud")
    }

    print("\n" + "=" * 74)
    print(f"{C_BOLD}{C_YELLOW}                     BoosOS World Map Viewer v1.0{C_RESET}")
    print("=" * 74 + "\n")

    for line in world_map:
        print(line)

    print(f"\n{C_BOLD}{C_WHITE}Legendă:{C_RESET} {C_GREEN}USCAT / Continente{C_RESET} | {C_BLUE}OCEAN / Ape{C_RESET} | {C_WHITE}GHEAȚĂ / Poli{C_RESET}")
    print(f"\nTipărește o țară pentru detalii (ex: {C_YELLOW}romania{C_RESET}, {C_YELLOW}usa{C_RESET}, {C_YELLOW}japan{C_RESET}) sau tastați '{C_YELLOW}exit{C_RESET}':")

    while True:
        try:
            cmd = input(f"{C_CYAN}boosmap> {C_RESET}").strip().lower()
            if not cmd:
                continue
            if cmd in ['exit', 'quit', 'q']:
                break
            
            if cmd in capitals:
                city, coords, region = capitals[cmd]
                print(f" -> {C_BOLD}{C_GREEN}{cmd.upper()}{C_RESET} | Capitală: {C_YELLOW}{city}{C_RESET} | Coordonate: {C_WHITE}{coords}{C_RESET} | Regiune: {region}")
            else:
                print(f" -> {C_YELLOW}Țara '{cmd}' nu este în baza de date.{C_RESET} Țări disponibile: {', '.join(capitals.keys())}")
        except (KeyboardInterrupt, EOFError):
            break

run_boosmap()