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
        "romania": ("Bucharest", "44.4° N, 26.1° E", "Europe"),
        "usa": ("Washington D.C.", "38.9° N, 77.0° W", "North America"),
        "germany": ("Berlin", "52.5° N, 13.4° E", "Europe"),
        "japan": ("Tokyo", "35.6° N, 139.6° E", "Asia"),
        "uk": ("London", "51.5° N, 0.1° W", "Europe"),
        "france": ("Paris", "48.8° N, 2.3° E", "Europe"),
        "australia": ("Canberra", "35.2° S, 149.1° E", "Oceania"),
        "brazil": ("Brasília", "15.8° S, 47.9° W", "South America")
    }

    print("\n" + "=" * 74)
    print(f"{C_BOLD}{C_YELLOW}                     BoosOS World Map Viewer v1.0{C_RESET}")
    print("=" * 74 + "\n")

    for line in world_map:
        print(line)

    print(f"\n{C_BOLD}{C_WHITE}Legend:{C_RESET} {C_GREEN}LAND / Continents{C_RESET} | {C_BLUE}OCEAN / Water{C_RESET} | {C_WHITE}ICE / Poles{C_RESET}")
    print(f"\nType a country name for details (e.g., {C_YELLOW}romania{C_YELLOW}, {C_YELLOW}usa{C_YELLOW}, {C_YELLOW}japan{C_RESET}) or type '{C_YELLOW}exit{C_RESET}':")

    while True:
        try:
            cmd = input(f"{C_CYAN}boosmap> {C_RESET}").strip().lower()
            if not cmd:
                continue
            if cmd in ['exit', 'quit', 'q']:
                break
            
            if cmd in capitals:
                city, coords, region = capitals[cmd]
                print(f" -> {C_BOLD}{C_GREEN}{cmd.upper()}{C_RESET} | Capital: {C_YELLOW}{city}{C_RESET} | Coordinates: {C_WHITE}{coords}{C_RESET} | Region: {region}")
            else:
                print(f" -> {C_YELLOW}Country '{cmd}' not found in database.{C_RESET} Available countries: {', '.join(capitals.keys())}")
        except (KeyboardInterrupt, EOFError):
            break

run_boosmap()