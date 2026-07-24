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
    # Screen resolution in terminal characters
    SCREEN_WIDTH = 60
    SCREEN_HEIGHT = 20
    FOV = math.pi / 3  # 60 degrees Field of View

    # World Map (1 = Wall, 0 = Empty Space)
    MAP_WIDTH = 12
    MAP_HEIGHT = 12
    WORLD_MAP = [
        "111111111111",
        "100000000001",
        "101111011101",
        "101000000101",
        "101011110101",
        "100010010001",
        "101010010101",
        "101011010101",
        "101000000101",
        "101111111101",
        "100000000001",
        "111111111111"
    ]

    # Player initial state
    player_x = 2.0
    player_y = 2.0
    player_angle = 0.0

    # ANSI Colors
    C_GREEN = "\033[92m"
    C_RED   = "\033[91m"
    C_CYAN  = "\033[96m"
    C_RESET = "\033[0m"

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
            # 1. Handle Input
            key = get_input()
            if key == 'q':
                running = False
                break

            move_speed = 0.25
            rot_speed = 0.15

            if key == 'w':
                nx = player_x + math.cos(player_angle) * move_speed
                ny = player_y + math.sin(player_angle) * move_speed
                if WORLD_MAP[int(ny)][int(nx)] == '0':
                    player_x, player_y = nx, ny
            elif key == 's':
                nx = player_x - math.cos(player_angle) * move_speed
                ny = player_y - math.sin(player_angle) * move_speed
                if WORLD_MAP[int(ny)][int(nx)] == '0':
                    player_x, player_y = nx, ny
            elif key == 'a':
                player_angle -= rot_speed
            elif key == 'd':
                player_angle += rot_speed

            # Keep angle within 0 - 2PI
            player_angle %= (2 * math.pi)

            # 2. Raycasting Engine
            buffer = [[" " for _ in range(SCREEN_WIDTH)] for _ in range(SCREEN_HEIGHT)]

            for x in range(SCREEN_WIDTH):
                # Calculate ray angle
                ray_angle = (player_angle - FOV / 2.0) + (x / float(SCREEN_WIDTH)) * FOV
                
                distance_to_wall = 0.0
                hit_wall = False

                eye_x = math.cos(ray_angle)
                eye_y = math.sin(ray_angle)

                # Ray step checking
                while not hit_wall and distance_to_wall < 16.0:
                    distance_to_wall += 0.08
                    test_x = int(player_x + eye_x * distance_to_wall)
                    test_y = int(player_y + eye_y * distance_to_wall)

                    if test_x < 0 or test_x >= MAP_WIDTH or test_y < 0 or test_y >= MAP_HEIGHT:
                        hit_wall = True
                        distance_to_wall = 16.0
                    else:
                        if WORLD_MAP[test_y][test_x] == '1':
                            hit_wall = True

                # Fisheye lens correction
                corrected_dist = distance_to_wall * math.cos(ray_angle - player_angle)

                # Calculate ceiling and floor boundaries
                ceiling = int((SCREEN_HEIGHT / 2.0) - SCREEN_HEIGHT / float(corrected_dist if corrected_dist > 0.1 else 0.1))
                floor = SCREEN_HEIGHT - ceiling

                # Choose texture shade based on distance
                if corrected_dist <= 2.0: shade = SHADE_CHARS[0]
                elif corrected_dist <= 3.5: shade = SHADE_CHARS[1]
                elif corrected_dist <= 5.0: shade = SHADE_CHARS[2]
                elif corrected_dist <= 7.0: shade = SHADE_CHARS[3]
                elif corrected_dist <= 9.0: shade = SHADE_CHARS[4]
                elif corrected_dist <= 12.0: shade = SHADE_CHARS[5]
                else: shade = SHADE_CHARS[6]

                # Fill screen column
                for y in range(SCREEN_HEIGHT):
                    if y <= ceiling:
                        buffer[y][x] = " "  # Sky
                    elif ceiling < y <= floor:
                        buffer[y][x] = shade  # Wall
                    else:
                        buffer[y][x] = "."  # Floor

            # Render Minimap overlay (Top-Left Corner)
            for my in range(MAP_HEIGHT):
                for mx in range(MAP_WIDTH):
                    if int(player_y) == my and int(player_x) == mx:
                        buffer[my][mx] = "P"
                    else:
                        buffer[my][mx] = "#" if WORLD_MAP[my][mx] == '1' else " "

            # Render HUD Shotgun at bottom center
            gun_art = ["| |", "/ \\"]
            for gi, gline in enumerate(gun_art):
                start_x = (SCREEN_WIDTH // 2) - 1
                for gchar_idx, gchar in enumerate(gline):
                    buffer[SCREEN_HEIGHT - 2 + gi][start_x + gchar_idx] = gchar

            # 3. Draw Frame to Terminal
            output = []
            output.append(f"{C_RED}=== BOOS-DOOM ASCII v1.0 ==={C_RESET}")
            for row in buffer:
                output.append("".join(row))
            output.append(f"{C_CYAN}Controls: W (Forward), S (Back), A/D (Rotate), Q (Quit){C_RESET}")
            
            clear_screen()
            sys.stdout.write("\n".join(output) + "\n")
            sys.stdout.flush()

            time.sleep(0.03)

    finally:
        if not IS_WINDOWS:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

run_boosdoom()