import time, os, sys

IS_WINDOWS = sys.platform.startswith("win")
if IS_WINDOWS:
    import msvcrt
else:
    import select, tty, termios

def clear():
    os.system("cls" if IS_WINDOWS else "clear")

def get_key():
    """Non-blocking keyboard check."""
    if IS_WINDOWS:
        if msvcrt.kbhit():
            return msvcrt.getch().decode('utf-8', errors='ignore').lower()
    else:
        if select.select([sys.stdin], [], [], 0)[0]:
            return sys.stdin.read(1).lower()
    return None

def live_clock():
    alarm_time = None
    print("\n--- Live Clock (Press 'a' to set alarm, 'q' to back) ---")
    
    # Simple terminal non-blocking setup for Linux/Mac
    if not IS_WINDOWS:
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        tty.setcbreak(fd)

    try:
        while True:
            current = time.strftime("%H:%M:%S")
            date_str = time.strftime("%A, %B %d, %Y")
            
            clear()
            print("========================================")
            print(f"         TIME: {current}")
            print(f"         DATE: {date_str}")
            if alarm_time:
                print(f"         ALARM SET FOR: {alarm_time}")
            print("========================================")
            print("[A] Set Alarm  |  [C] Clear Alarm  |  [Q] Main Menu")

            if alarm_time and current == alarm_time:
                print("\n" + "!"*40)
                print("   *** ALARM RINGING! BEEP BEEP! ***")
                print("!"*40)

            key = get_key()
            if key == 'q':
                break
            elif key == 'a':
                # Restore terminal settings briefly for text input
                if not IS_WINDOWS:
                    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
                print("\n")
                alarm_input = input("Set alarm time (HH:MM:SS format, e.g., 14:30:00): ").strip()
                if len(alarm_input) == 8:
                    alarm_time = alarm_input
                    print(f"Alarm set for {alarm_time}!")
                    time.sleep(1)
                else:
                    print("Invalid format. Use HH:MM:SS.")
                    time.sleep(1)
                if not IS_WINDOWS:
                    tty.setcbreak(fd)
            elif key == 'c':
                alarm_time = None

            time.sleep(0.2)
    finally:
        if not IS_WINDOWS:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

def stopwatch():
    print("\n--- Stopwatch ---")
    input("Press ENTER to start...")
    start_time = time.time()
    laps = []
    
    if not IS_WINDOWS:
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        tty.setcbreak(fd)

    try:
        while True:
            elapsed = time.time() - start_time
            mins, secs = divmod(elapsed, 60)
            hours, mins = divmod(mins, 60)
            time_str = f"{int(hours):02d}:{int(mins):02d}:{secs:05.2f}"
            
            clear()
            print("========================================")
            print(f"      STOPWATCH: {time_str}")
            print("========================================")
            print("[L] Lap  |  [Q] Stop & Exit")
            
            if laps:
                print("\nLaps:")
                for i, lap in enumerate(laps, 1):
                    print(f"  Lap {i}: {lap}")

            key = get_key()
            if key == 'q':
                break
            elif key == 'l':
                laps.append(time_str)

            time.sleep(0.05)
    finally:
        if not IS_WINDOWS:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

def countdown_timer():
    clear()
    print("--- Countdown Timer ---")
    try:
        seconds = int(input("Enter countdown time in seconds: "))
    except ValueError:
        print("Invalid number.")
        time.sleep(1)
        return

    while seconds > 0:
        mins, secs = divmod(seconds, 60)
        clear()
        print("========================================")
        print(f"      TIMER REMAINING: {mins:02d}:{secs:02d}")
        print("========================================")
        time.sleep(1)
        seconds -= 1

    clear()
    print("========================================")
    print("       *** TIME IS UP! ***")
    print("========================================")
    time.sleep(2)

def main():
    while True:
        clear()
        print("========================================")
        print("            BoosOS Clock App            ")
        print("========================================")
        print("1. Live Clock & Alarm")
        print("2. Stopwatch")
        print("3. Countdown Timer")
        print("4. Exit App")
        print("----------------------------------------")
        
        choice = input("Select an option (1-4): ").strip()
        
        if choice == '1':
            live_clock()
        elif choice == '2':
            stopwatch()
        elif choice == '3':
            countdown_timer()
        elif choice == '4':
            print("Closing Clock...")
            break

main()