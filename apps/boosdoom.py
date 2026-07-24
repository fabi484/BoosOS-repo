import os
import sys
import time
import math

# Cross-platform non-blocking key reader
IS_WINDOWS = sys.platform.startswith("win")
if IS_WINDOWS:
    import msvcrt
else:
    import select, tty, termios

def run_boosdoom():
    # ANSI Colors
    C_GREEN  = "\033[92m"
    C_RED    = "\033[91m"
    C_YELLOW = "\033[93m"
    C_CYAN   = "\033[96m"
    C_WHITE  = "\033[97m"
    C_BOLD   = "\033[1m"
    C_RESET  = "\033[0m"

    # --- FLASHING LIGHTS WARNING ---
    os.system("cls" if IS_WINDOWS else "clear")
    print(f"\n{C_BOLD}{C_RED}===================================================={C_RESET}")
    print(f"{C_BOLD}{C_YELLOW}              [!] PHOTOSENSITIVITY WARNING [!]{C_RESET}")
    print(f"{C_BOLD}{C_RED}===================================================={C_RESET}")
    print(f"{C_WHITE}This game renders high-frequency ASCII raycasting graphics")
    print(f"which may cause terminal flickering or flashing light effects.{C_RESET}\n")
    
    choice = input(f"Press {C_GREEN}'Y'{C_RESET} to continue or any other key to exit: ").strip().lower()
    if choice != 'y':
        print(f"\n{C_CYAN}Exiting BoosDOOM...{C_RESET}")
        return

    # Screen resolution in terminal characters
    SCREEN_WIDTH = 60
    SCREEN_HEIGHT = 20
    FOV = math.pi / 3  # 60 degrees Field of View

    # World Map (1 = Wall, 0 = Empty Space)
    MAP_WIDTH = 12
    MAP_HEIGHT = 12
    world_map = [
        ["1","1","1","1","1","1","1","1","1","1","1","1"],
        ["1","0","0","0","0","0","0","0","0","0","0","1"],
        ["1","0","1","1","1","1","0","1","1","1","0","1"],
        ["1","0","1","0","0","0","0","0","0","1","0","1"],
        ["1","0","1","0","1","1","1","1","0","1","0","1"],
        ["1","0","0","0","1","0","0","1","0","0","0","1"],
        ["1","0","1","0","1","0","0","1","0","1","0","1"],
        ["1","0","1","0","1","1","0","1","0","1","0","1"],
        ["1","0","1","0","0","0","0","0","0","1","0","1"],
        ["1","0","1","1","1","1","1","1","1","1","0","1"],
        ["1","0","0","0","0","0","0","0","0","0","0","1"],
        ["1","1","1","1","1","1","1","1","1","1","1","1"]
    ]

    # Player initial state
    player_x = 2.0
    player_y = 2.0
    player_angle = 0.0

    # Editor Cursor state
    editor_x = 1
    editor_y = 1
    in_editor = False

    # Wall texture gradient based on distance
    SHADE_CHARS = ["█", "▓", "▒", "░", ":", ".", " "]

    def clear_screen():
        os.system("cls" if IS_WINDOWS else "clear")

    def get_input():
        if IS_WINDOWS:
            if msvcrt.kbhit():
                ch = msvcrt.getch()
                try:
                    return ch.decode('utf-8').lower()
                except UnicodeDecodeError:
                    return ""
            return ""
        else:
            if select.select([sys.stdin], [], [], 0.01)[0]:
                return sys.stdin.read(1).lower()
            return ""

    # Set terminal mode for POSIX systems
    if not IS_WINDOWS:
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        tty.setcbreak(fd)

    try:
        clear_screen()
        print(f"{C_GREEN}Initializing ASCII DOOM Engine...{C_RESET}")
        time.sleep(0.5)

        running = True
        while running:
            key = get_input()
            if key == 'q':
                running = False
                break

            # Toggle Map Editor Mode
            if key == 'e':
                in_editor = not in_editor
                editor_x = int(player_x)
                editor_y = int(player_y)

            # --- MODE 1: MAP EDITOR ---
            if in_editor:
                if key == 'w' and editor_y > 0: editor_y -= 1
                elif key == 's' and editor_y < MAP_HEIGHT - 1: editor_y += 1
                elif key == 'a' and editor_x > 0: editor_x -= 1
                elif key == 'd' and editor_x < MAP_WIDTH - 1: editor_x += 1
                elif key == ' ':  # Toggle wall with SPACE
                    # Do not block outer border walls
                    if 0 < editor_x < MAP_WIDTH - 1 and 0 < editor_y < MAP_HEIGHT - 1:
                        world_map[editor_y][editor_x] = '0' if world_map[editor_y][editor_x] == '1' else '1'

                # Render Editor Overlay
                clear_screen()
                print(f"{C_YELLOW}=== MAP EDITOR MODE ==={C_RESET}")
                print(f"Move: {C_WHITE}W/A/S/D{C_RESET} | Toggle Wall: {C_WHITE}SPACE{C_RESET} | Exit Editor: {C_WHITE}E{C_RESET}\n")

                for my in range(MAP_HEIGHT):
                    line = ""
                    for mx in range(MAP_WIDTH):
                        if my == editor_y and mx == editor_x:
                            line += f"{C_YELLOW}[X]{C_RESET}"  # Cursor
                        elif int(player_y) == my and int(player_x) == mx:
                            line += f"{C_GREEN} P {C_RESET}"    # Player
                        elif world_map[my][mx] == '1':
                            line += "███"
                        else:
                            line += " . "
                    print(line)
                
                print(f"\n{C_CYAN}Current Block: {'Wall (1)' if world_map[editor_y][editor_x] == '1' else 'Empty (0)'}{C_RESET}")
                time.sleep(0.05)
                continue

            # --- MODE 2: 3D RAYCASTER GAMEPLAY ---
            move_speed = 0.25
            rot_speed = 0.15

            if key == 'w':
                nx = player_x + math.cos(player_angle) * move_speed
                ny = player_y + math.sin(player_angle) * move_speed
                if world_map[int(ny)][int(nx)] == '0':
                    player_x, player_y = nx, ny
            elif key == 's':
                nx = player_x - math.cos(player_angle) * move_speed
                ny = player_y - math.sin(player_angle) * move_speed
                if world_map[int(ny)][int(nx)] == '0':
                    player_x, player_y = nx, ny
            elif key == 'a':
                player_angle -= rot_speed
            elif key == 'd':
                player_angle += rot_speed

            player_angle %= (2 * math.pi)

            # Raycasting Engine
            buffer = [[" " for _ in range(SCREEN_WIDTH)] for _ in range(SCREEN_HEIGHT)]

            for x in range(SCREEN_WIDTH):
                ray_angle = (player_angle - FOV / 2.0) + (x / float(SCREEN_WIDTH)) * FOV
                distance_to_wall = 0.0
                hit_wall = False

                eye_x = math.cos(ray_angle)
                eye_y = math.sin(ray_angle)

                while not hit_wall and distance_to_wall < 16.0:
                    distance_to_wall += 0.08
                    test_x = int(player_x + eye_x * distance_to_wall)
                    test_y = int(player_y + eye_y * distance_to_wall)

                    if test_x < 0 or test_x >= MAP_WIDTH or test_y < 0 or test_y >= MAP_HEIGHT:
                        hit_wall = True
                        distance_to_wall = 16.0
                    else:
                        if world_map[test_y][test_x] == '1':
                            hit_wall = True

                corrected_dist = distance_to_wall * math.cos(ray_angle - player_angle)

                ceiling = int((SCREEN_HEIGHT / 2.0) - SCREEN_HEIGHT / float(corrected_dist if corrected_dist > 0.1 else 0.1))
                floor = SCREEN_HEIGHT - ceiling

                if corrected_dist <= 2.0: shade = SHADE_CHARS[0]
                elif corrected_dist <= 3.5: shade = SHADE_CHARS[1]
                elif corrected_dist <= 5.0: shade = SHADE_CHARS[2]
                elif corrected_dist <= 7.0: shade = SHADE_CHARS[3]
                elif corrected_dist <= 9.0: shade = SHADE_CHARS[4]
                elif corrected_dist <= 12.0: shade = SHADE_CHARS[5]
                else: shade = SHADE_CHARS[6]

                for y in range(SCREEN_HEIGHT):
                    if y <= ceiling:
                        buffer[y][x] = " "
                    elif ceiling < y <= floor:
                        buffer[y][x] = shade
                    else:
                        buffer[y][x] = "."

            # Minimap overlay
            for my in range(MAP_HEIGHT):
                for mx in range(MAP_WIDTH):
                    if int(player_y) == my and int(player_x) == mx:
                        buffer[my][mx] = "P"
                    else:
                        buffer[my][mx] = "#" if world_map[my][mx] == '1' else " "

            # HUD Shotgun
            gun_art = ["| |", "/ \\"]
            for gi, gline in enumerate(gun_art):
                start_x = (SCREEN_WIDTH // 2) - 1
                for gchar_idx, gchar in enumerate(gline):
                    buffer[SCREEN_HEIGHT - 2 + gi][start_x + gchar_idx] = gchar

            # Draw Frame
            output = []
            output.append(f"{C_RED}=== BOOS-DOOM ASCII v1.1 ==={C_RESET}")
            for row in buffer:
                output.append("".join(row))
            output.append(f"{C_CYAN}Controls: W/S/A/D (Move/Turn), E (Map Editor), Q (Quit){C_RESET}")
            
            clear_screen()
            sys.stdout.write("\n".join(output) + "\n")
            sys.stdout.flush()

            time.sleep(0.04)

    finally:
        if not IS_WINDOWS:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

run_boosdoom()