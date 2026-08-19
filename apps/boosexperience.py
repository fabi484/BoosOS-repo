import tkinter as tk
from tkinter import scrolledtext, messagebox
import sys
import os
import threading
import queue

# Import your existing BoosOS core
try:
    from boos import BoosOS, safe_input
except ImportError:
    print("[FATAL] Could not find boos.py. Make sure it's in the same directory.")
    sys.exit(1)

class TerminalRedirector:
    """Redirects stdout/stderr to the Tkinter text widget."""
    def __init__(self, text_widget, tag="stdout"):
        self.text_widget = text_widget
        self.tag = tag

    def write(self, string):
        self.text_widget.after(0, self._append, string)

    def _append(self, string):
        self.text_widget.configure(state='normal')
        self.text_widget.insert(tk.END, string, (self.tag,))
        self.text_widget.see(tk.END)
        self.text_widget.configure(state='disabled')

    def flush(self):
        pass

class BoosExperienceGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("BoosExperience 0.1 Beta 4")
        self.root.geometry("900x600")
        self.root.minsize(700, 450)
        
        # Dark Mode Theme
        self.bg_color = "#1e1e1e"
        self.fg_color = "#d4d4d4"
        self.accent_color = "#007acc"
        self.term_bg = "#0c0c0c"
        
        self.root.configure(bg=self.bg_color)
        
        # Initialize BoosOS Core
        self.boos = BoosOS()
        self.output_queue = queue.Queue()
        
        # Layout Setup
        self.setup_desktop()
        self.setup_terminal()
        
        # Redirect prints to GUI
        sys.stdout = TerminalRedirector(self.terminal_output, "stdout")
        sys.stderr = TerminalRedirector(self.terminal_output, "stderr")
        
        # Override safe_input to use GUI prompt
        import builtins
        self._original_input = builtins.input
        builtins.input = self.gui_input
        
        # Initial boot message
        print(f"=== BoosExperience 0.1 Beta 4 ===")
        print(f"Loaded BoosOS v{self.boos.version}")
        print(f"User: {self.boos.current_user or 'guest'}@boos\n")

    def setup_desktop(self):
        """Creates the top panel with installed app icons."""
        desktop_frame = tk.Frame(self.root, bg=self.bg_color, pady=10)
        desktop_frame.pack(fill=tk.X, padx=10)
        
        tk.Label(
            desktop_frame, 
            text="📦 Installed Apps (Desktop)", 
            bg=self.bg_color, 
            fg=self.accent_color, 
            font=("Consolas", 12, "bold")
        ).pack(anchor=tk.W)
        
        apps_container = tk.Frame(desktop_frame, bg=self.bg_color)
        apps_container.pack(fill=tk.X, pady=5)
        
        self.refresh_desktop_apps(apps_container)
        
        # Separator
        tk.Frame(self.root, height=1, bg="#333").pack(fill=tk.X, padx=10, pady=5)

    def refresh_desktop_apps(self, container):
        """Scans installed_apps folder and creates clickable buttons."""
        for widget in container.winfo_children():
            widget.destroy()
            
        apps_dir = self.boos.get_apps_dir()
        installed = []
        if os.path.exists(apps_dir):
            installed = [f[:-3] for f in os.listdir(apps_dir) if f.endswith(".py")]
            
        if not installed:
            tk.Label(
                container, 
                text="No apps installed. Use 'pkg install <name>' in terminal.", 
                bg=self.bg_color, 
                fg="#666",
                font=("Consolas", 10)
            ).pack(anchor=tk.W)
            return
            
        for app in sorted(installed):
            btn = tk.Button(
                container,
                text=f"🚀 {app}",
                command=lambda a=app: self.run_app_threaded(a),
                bg="#2d2d2d",
                fg=self.fg_color,
                activebackground=self.accent_color,
                activeforeground="white",
                relief=tk.FLAT,
                padx=10,
                pady=5,
                font=("Consolas", 10),
                cursor="hand2"
            )
            btn.pack(side=tk.LEFT, padx=3)

    def setup_terminal(self):
        """Creates the embedded terminal at the bottom."""
        term_frame = tk.Frame(self.root, bg=self.term_bg)
        term_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        self.terminal_output = scrolledtext.ScrolledText(
            term_frame,
            wrap=tk.WORD,
            bg=self.term_bg,
            fg=self.fg_color,
            insertbackground=self.fg_color,
            font=("Consolas", 11),
            state='disabled',
            borderwidth=0,
            highlightthickness=0
        )
        self.terminal_output.pack(fill=tk.BOTH, expand=True)
        self.terminal_output.tag_configure("stdout", foreground=self.fg_color)
        
        # Command Entry
        entry_frame = tk.Frame(term_frame, bg=self.term_bg)
        entry_frame.pack(fill=tk.X)
        
        prompt_label = tk.Label(
            entry_frame, 
            text=f"{self.boos.current_user or 'guest'}@boos:> ", 
            bg=self.term_bg, 
            fg=self.accent_color,
            font=("Consolas", 11)
        )
        prompt_label.pack(side=tk.LEFT)
        
        self.cmd_entry = tk.Entry(
            entry_frame,
            bg=self.term_bg,
            fg=self.fg_color,
            insertbackground=self.fg_color,
            font=("Consolas", 11),
            borderwidth=0,
            highlightthickness=0
        )
        self.cmd_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.cmd_entry.bind("<Return>", self.execute_command)
        self.cmd_entry.focus_set()
        
        # Command History
        self.history = []
        self.history_index = -1
        self.cmd_entry.bind("<Up>", self.prev_history)
        self.cmd_entry.bind("<Down>", self.next_history)

    def execute_command(self, event=None):
        cmd = self.cmd_entry.get().strip()
        self.cmd_entry.delete(0, tk.END)
        
        if cmd:
            self.history.append(cmd)
            self.history_index = len(self.history)
            
        # Echo command to terminal
        self.terminal_output.configure(state='normal')
        self.terminal_output.insert(tk.END, f"{self.boos.current_user or 'guest'}@boos:> {cmd}\n")
        self.terminal_output.configure(state='disabled')
        self.terminal_output.see(tk.END)
        
        if cmd.lower() == "exit":
            self.root.destroy()
            return
            
        # Run in thread to prevent GUI freeze
        threading.Thread(target=self._run_boos_cmd, args=(cmd,), daemon=True).start()

    def _run_boos_cmd(self, cmd_string):
        """Parses and executes command using existing BoosOS logic."""
        try:
            ui = cmd_string.strip().split()
            if not ui: 
                return
                
            c = ui[0].lower()
            args = ui[1:]
            
            # Map commands just like in boos.py run() loop
            actions = {
                "sysinfo": self.boos.show_sysinfo,
                "clear": lambda: self.clear_terminal(),
                "help": self.boos.show_help,
                "pkg": lambda: self.boos.pkg_manager(args),
                "notes": self.boos.boos_notes.run,
                "boosfetch": self.boos.boos_fetch,
                "ping": lambda: self.boos.ping(args),
                "calc": lambda: self.boos.calculator(args),
                "top": self.boos.top_process,
                "tictactoe": self.boos.play_tictactoe,
                "snake": self.boos.play_snake,
                "register": self.boos.register,
                "login": self.handle_login,
                "whoami": lambda: print(f"Logged in as: {self.boos.current_user or 'guest'}")
            }
            
            if c in actions:
                actions[c]()
            elif c == "run" and args:
                self.boos.run_app(args[0])
                self._refresh_desktop_after_change()
            elif os.path.exists(os.path.join(self.boos.get_apps_dir(), f"{c}.py")):
                self.boos.run_app(c)
            else:
                sugg = self.boos.get_suggestion(c)
                if sugg:
                    print(f"Command '{c}' not found. Did you mean '{sugg}'?")
                else:
                    print(f"Command '{c}' not found. Type 'help' for available commands.")
                    
        except Exception as e:
            print(f"[GUI Error] {e}")

    def run_app_threaded(self, app_name):
        """Runs app from desktop button click."""
        print(f"\n[Desktop] Launching {app_name}...")
        threading.Thread(target=self.boos.run_app, args=(app_name,), daemon=True).start()

    def handle_login(self):
        """Special handler to refresh desktop after login."""
        self.boos.login()
        self._refresh_desktop_after_change()

    def _refresh_desktop_after_change(self):
        """Refreshes desktop icons when apps/users change."""
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Frame):
                for child in widget.winfo_children():
                    if isinstance(child, tk.Frame):
                        self.refresh_desktop_apps(child)
                        return

    def clear_terminal(self):
        self.terminal_output.configure(state='normal')
        self.terminal_output.delete(1.0, tk.END)
        self.terminal_output.configure(state='disabled')

    def gui_input(self, prompt=""):
        """Replaces built-in input() with a GUI dialog."""
        dialog = tk.Toplevel(self.root)
        dialog.title("BoosOS Input Required")
        dialog.geometry("400x120")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.configure(bg=self.bg_color)
        
        tk.Label(dialog, text=prompt, bg=self.bg_color, fg=self.fg_color, 
                 font=("Consolas", 10)).pack(pady=10)
        
        entry = tk.Entry(dialog, font=("Consolas", 11), width=40)
        entry.pack(pady=5)
        entry.focus_set()
        
        result = [None]
        
        def submit(event=None):
            result[0] = entry.get()
            dialog.destroy()
            
        entry.bind("<Return>", submit)
        tk.Button(dialog, text="Submit", command=submit, 
                  bg=self.accent_color, fg="white").pack(pady=10)
        
        self.root.wait_window(dialog)
        return result[0] or ""

    def prev_history(self, event):
        if self.history:
            self.history_index = max(0, self.history_index - 1)
            self.cmd_entry.delete(0, tk.END)
            self.cmd_entry.insert(0, self.history[self.history_index])
        return "break"

    def next_history(self, event):
        if self.history:
            self.history_index = min(len(self.history), self.history_index + 1)
            self.cmd_entry.delete(0, tk.END)
            if self.history_index < len(self.history):
                self.cmd_entry.insert(0, self.history[self.history_index])
        return "break"

if __name__ == "__main__":
    root = tk.Tk()
    app = BoosExperienceGUI(root)
    root.mainloop()