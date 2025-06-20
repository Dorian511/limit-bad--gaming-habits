import time
import tkinter as tk
from tkinter import messagebox
import winsound

class BreakReminder:
    def __init__(self):
        self.no_count = 0
        self.running = False
        self.timeout = False

        self.init_root = tk.Tk()
        self.init_root.title("Game Break Reminder")
        self.init_root.geometry("300x150")

        tk.Label(self.init_root, text="Ready to launch your game?").pack(pady=10)
        tk.Button(self.init_root, text="Start Game", command=self.start_with_game).pack(pady=5)
        tk.Button(self.init_root, text="Start Without Game", command=self.start_without_game).pack(pady=5)
        tk.Button(self.init_root, text="Quit", command=self.quit_program).pack(pady=5)

        self.main_root = None

    def start_with_game(self):
        self.init_root.destroy()
        self.start_main_window()

    def start_without_game(self):
        self.init_root.destroy()
        self.start_main_window()

    def start_main_window(self):
        self.running = True
        self.main_root = tk.Tk()
        self.main_root.title("Break Reminder Running")
        self.main_root.geometry("300x150")

        self.status_label = tk.Label(self.main_root, text="Break reminder is running.")
        self.status_label.pack(pady=20)

        quit_btn = tk.Button(self.main_root, text="Quit", command=self.quit_program)
        quit_btn.pack(pady=10)

        self.last_prompt_time = time.time()
        self.warning_shown = False
        self.check_timer()

        self.main_root.mainloop()

    def quit_program(self):
        if self.main_root:
            self.main_root.destroy()
        if self.init_root:
            self.init_root.destroy()
        self.running = False

    def ask_break(self):
        popup = tk.Toplevel()
        popup.attributes('-fullscreen', True)
        popup.configure(bg='black')
        popup.title("Break Prompt")
        popup.protocol("WM_DELETE_WINDOW", lambda: None)
        popup.attributes('-topmost', True)
        popup.focus_force()

        label = tk.Label(
            popup,
            text="Do you want to take a break?",
            fg='white',
            bg='black',
            font=("Arial", 36)
        )
        label.pack(expand=True)

        def respond(yes):
            popup.destroy()
            if yes:
                self.no_count = 0
                self.show_break_screen(5, is_optional=True)
            else:
                self.no_count += 1
                if self.no_count >= 3:
                    self.timeout = True
                    self.show_break_screen(10, is_optional=False)

        button_frame = tk.Frame(popup, bg='black')
        button_frame.pack(pady=20)

        yes_btn = tk.Button(button_frame, text="Yes", font=("Arial", 20), width=10, command=lambda: respond(True))
        yes_btn.pack(side="left", padx=50)

        no_btn = tk.Button(button_frame, text="No", font=("Arial", 20), width=10, command=lambda: respond(False))
        no_btn.pack(side="right", padx=50)

        popup.grab_set()
        popup.focus_force()
        self.main_root.wait_window(popup)

    def show_break_screen(self, duration_seconds, is_optional=False):
        break_win = tk.Toplevel()
        break_win.attributes('-fullscreen', True)
        break_win.configure(bg='black')
        break_win.protocol("WM_DELETE_WINDOW", lambda: None)
        break_win.attributes('-topmost', True)

        label = tk.Label(
            break_win,
            text=f"Break Time! Please rest for {duration_seconds} seconds.",
            fg='white',
            bg='black',
            font=("Arial", 36)
        )
        label.pack(expand=True)

        def end_break():
            break_win.destroy()
            self.timeout = False
            self.no_count = 0
            self.continue_prompt()  # Timer resumes only after confirmation

        break_win.after(duration_seconds * 1000, end_break)
        break_win.mainloop()

    def continue_prompt(self):
        response = messagebox.askyesno("Continue?", "Do you want to continue using the reminder?")
        if not response:
            self.quit_program()
        else:
            self.last_prompt_time = time.time()
            self.warning_shown = False
            self.check_timer()  # Resume timer only after user agrees

    def check_timer(self):
        if not self.running:
            return

        current_time = time.time()

        # Warn 5 seconds before 15s timeout
        if (current_time - self.last_prompt_time >= 10) and not self.warning_shown:
            winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
            self.warning_shown = True

        # Trigger break after 15s
        if current_time - self.last_prompt_time >= 15:
            self.warning_shown = False
            if self.timeout:
                self.show_break_screen(10, is_optional=False)
            else:
                self.ask_break()
            return  # Stop check_timer loop after break; resume in continue_prompt()

        self.main_root.after(500, self.check_timer)

if __name__ == "__main__":
    app = BreakReminder()
    app.init_root.mainloop()
