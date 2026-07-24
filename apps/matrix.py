import time, random, os

os.system("clear" if os.name != "nt" else "cls")
print("=== Matrix Digital Rain (Press Ctrl+C to exit) ===")
time.sleep(1)

chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ@#$%^&*"
try:
    while True:
        line = "".join(random.choice(chars) if random.random() > 0.3 else " " for _ in range(60))
        print(f"\033[32m{line}\033[0m")
        time.sleep(0.05)
except KeyboardInterrupt:
    print("\n[Matrix Terminated]")