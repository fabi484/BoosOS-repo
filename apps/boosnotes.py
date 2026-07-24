import os
import sys
import json
from pathlib import Path

# Create 'BoosNotes' folder inside the user's main home folder
USER_HOME = Path.home()
NOTES_DIR = USER_HOME / "BoosNotes"
NOTES_FILE = NOTES_DIR / "notes.json"

def ensure_storage_exists():
    """Ensure the user's BoosNotes directory exists."""
    NOTES_DIR.mkdir(parents=True, exist_ok=True)

def load_notes():
    ensure_storage_exists()
    if NOTES_FILE.exists():
        try:
            with open(NOTES_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def save_notes(notes):
    ensure_storage_exists()
    with open(NOTES_FILE, "w", encoding="utf-8") as f:
        json.dump(notes, f, indent=2)

def run_boosnotes():
    # Enable ANSI escape sequences in Windows PowerShell/CMD
    if os.name == "nt":
        os.system("")

    # ANSI Colors
    C_GREEN  = "\033[92m"
    C_YELLOW = "\033[93m"
    C_CYAN   = "\033[96m"
    C_WHITE  = "\033[97m"
    C_RED    = "\033[91m"
    C_BOLD   = "\033[1m"
    C_RESET  = "\033[0m"

    notes = load_notes()

    def clear_screen():
        os.system("cls" if os.name == "nt" else "clear")

    while True:
        clear_screen()
        print(f"{C_BOLD}{C_YELLOW}===================================================={C_RESET}", flush=True)
        print(f"{C_BOLD}{C_CYAN}                BoosNotes App v1.1                  {C_RESET}", flush=True)
        print(f"{C_BOLD}{C_YELLOW}===================================================={C_RESET}", flush=True)
        print(f"{C_WHITE}Storage Path: {NOTES_FILE}{C_RESET}\n", flush=True)

        if not notes:
            print(f"{C_WHITE}No notes available. Create one using option '1'.{C_RESET}\n", flush=True)
        else:
            print(f"{C_BOLD}{C_WHITE}Your Saved Notes:{C_RESET}", flush=True)
            for idx, note in enumerate(notes, 1):
                print(f" {C_GREEN}[{idx}]{C_RESET} {C_BOLD}{note['title']}{C_RESET}", flush=True)
                print(f"     {C_WHITE}{note['content']}{C_RESET}\n", flush=True)

        print(f"{C_YELLOW}Options:{C_RESET}", flush=True)
        print(f" [{C_CYAN}1{C_RESET}] Add New Note", flush=True)
        print(f" [{C_CYAN}2{C_RESET}] Delete Note", flush=True)
        print(f" [{C_CYAN}3{C_RESET}] Exit", flush=True)

        try:
            choice = input(f"\n{C_CYAN}boosnotes> {C_RESET}").strip()

            if choice == "1":
                title = input(f"{C_WHITE}Enter note title: {C_RESET}").strip()
                if not title:
                    continue
                content = input(f"{C_WHITE}Enter note content: {C_RESET}").strip()
                notes.append({"title": title, "content": content})
                save_notes(notes)
                print(f"\n{C_GREEN}Note saved in {NOTES_DIR}!{C_RESET}", flush=True)
                input("Press Enter to continue...")

            elif choice == "2":
                if not notes:
                    print(f"\n{C_RED}No notes to delete!{C_RESET}", flush=True)
                    input("Press Enter to continue...")
                    continue
                
                note_num = input(f"{C_WHITE}Enter note number to delete: {C_RESET}").strip()
                if note_num.isdigit():
                    idx = int(note_num) - 1
                    if 0 <= idx < len(notes):
                        removed = notes.pop(idx)
                        save_notes(notes)
                        print(f"\n{C_RED}Deleted note: '{removed['title']}'{C_RESET}", flush=True)
                    else:
                        print(f"\n{C_RED}Invalid note number!{C_RESET}", flush=True)
                else:
                    print(f"\n{C_RED}Please enter a valid number!{C_RESET}", flush=True)
                input("Press Enter to continue...")

            elif choice in ["3", "exit", "quit", "q"]:
                print(f"\n{C_CYAN}Exiting BoosNotes...{C_RESET}", flush=True)
                break

        except (KeyboardInterrupt, EOFError):
            break

if __name__ == "__main__":
    run_boosnotes()