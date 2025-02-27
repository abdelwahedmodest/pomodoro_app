import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
import threading
import time
import json
import os
from plyer import notification
import sys

class PomodoroTimer:
    def __init__(self, root):
        self.root = root
        self.root.title("Pomodoro Timer")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
        # Timer durations in seconds
        self.durations = {
            "work": 25 * 60,
            "short_break": 5 * 60,
            "long_break": 15 * 60
        }
        
        # Timer state variables
        self.timer_running = False
        self.timer_paused = False
        self.current_timer_type = "work"
        self.time_remaining = self.durations["work"]
        self.timer_thread = None
        self.stop_thread = threading.Event()
        
        # Session tracking
        self.completed_sessions = 0
        self.total_sessions = 4
        
        # User preferences
        self.theme = "darkly"  # Default dark theme
        self.volume = 50  # Default volume (0-100)
        
        # Load saved preferences
        self.load_preferences()
        
        # Apply theme
        self.style = ttk.Style(theme=self.theme)
        
        # Create UI elements
        self.create_widgets()
        
        # Bind keyboard shortcuts
        self.root.bind("<space>", lambda event: self.toggle_timer())
        self.root.bind("r", lambda event: self.reset_timer())
        
        # Handle window close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def create_widgets(self):
        # Main container with padding
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(fill=BOTH, expand=YES)
        
        # Header with title and session info
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=X, pady=(0, 20))
        
        title_label = ttk.Label(header_frame, text="Pomodoro Timer", font=("TkDefaultFont", 24, "bold"))
        title_label.pack(side=LEFT)
        
        # Session tracking display
        self.session_label = ttk.Label(
            header_frame, 
            text=f"Sessions: {self.completed_sessions}/{self.total_sessions}", 
            font=("TkDefaultFont", 12)
        )
        self.session_label.pack(side=RIGHT, padx=10)
        
        # Session type indicator
        self.session_type_frame = ttk.Frame(main_frame)
        self.session_type_frame.pack(fill=X, pady=(0, 10))
        
        self.session_type_label = ttk.Label(
            self.session_type_frame,
            text="WORK SESSION",
            font=("TkDefaultFont", 12, "bold"),
            bootstyle=SUCCESS
        )
        self.session_type_label.pack()
        
        # Timer display
        timer_frame = ttk.Frame(main_frame)
        timer_frame.pack(fill=X, pady=10)
        
        self.timer_display = ttk.Label(
            timer_frame,
            text=self.format_time(self.time_remaining),
            font=("TkDefaultFont", 48, "bold"),
            anchor=CENTER
        )
        self.timer_display.pack(fill=X)
        
        # Progress bar
        progress_frame = ttk.Frame(main_frame)
        progress_frame.pack(fill=X, pady=20)
        
        self.progress_bar = ttk.Progressbar(
            progress_frame,
            bootstyle=SUCCESS,
            length=100,
            mode="determinate",
            value=0
        )
        self.progress_bar.pack(fill=X)
        
        # Control buttons
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(fill=X, pady=20)
        
        # Start button
        self.start_button = ttk.Button(
            buttons_frame,
            text="Start",
            bootstyle=SUCCESS,
            command=self.start_timer,
            width=15
        )
        self.start_button.pack(side=LEFT, padx=10)
        
        # Pause button
        self.pause_button = ttk.Button(
            buttons_frame,
            text="Pause",
            bootstyle=WARNING,
            command=self.pause_timer,
            width=15,
            state=DISABLED
        )
        self.pause_button.pack(side=LEFT, padx=10)
        
        # Reset button
        self.reset_button = ttk.Button(
            buttons_frame,
            text="Reset",
            bootstyle=DANGER,
            command=self.reset_timer,
            width=15
        )
        self.reset_button.pack(side=LEFT, padx=10)
        
        # Settings frame
        settings_frame = ttk.LabelFrame(main_frame, text="Settings", padding=10)
        settings_frame.pack(fill=X, pady=20)
        
        # Theme toggle
        theme_frame = ttk.Frame(settings_frame)
        theme_frame.pack(fill=X, pady=5)
        
        theme_label = ttk.Label(theme_frame, text="Theme:")
        theme_label.pack(side=LEFT, padx=(0, 10))
        
        self.theme_var = tk.StringVar(value=self.theme)
        theme_combo = ttk.Combobox(
            theme_frame,
            textvariable=self.theme_var,
            values=["darkly", "superhero", "solar", "cyborg", "vapor"],
            width=15,
            state="readonly"
        )
        theme_combo.pack(side=LEFT)
        theme_combo.bind("<<ComboboxSelected>>", self.change_theme)
        
        # Volume control
        volume_frame = ttk.Frame(settings_frame)
        volume_frame.pack(fill=X, pady=5)
        
        volume_label = ttk.Label(volume_frame, text="Volume:")
        volume_label.pack(side=LEFT, padx=(0, 10))
        
        self.volume_var = tk.IntVar(value=self.volume)
        volume_scale = ttk.Scale(
            volume_frame,
            from_=0,
            to=100,
            variable=self.volume_var,
            command=self.update_volume
        )
        volume_scale.pack(side=LEFT, fill=X, expand=YES)
        
        self.volume_label = ttk.Label(volume_frame, text=f"{self.volume}%", width=5)
        self.volume_label.pack(side=LEFT, padx=10)
        
        # Keyboard shortcuts info
        shortcuts_frame = ttk.Frame(main_frame)
        shortcuts_frame.pack(fill=X, pady=(20, 0))
        
        shortcuts_label = ttk.Label(
            shortcuts_frame,
            text="Keyboard Shortcuts: Space (Start/Pause), R (Reset)",
            font=("TkDefaultFont", 9),
            foreground="gray"
        )
        shortcuts_label.pack()
    
    def format_time(self, seconds):
        """Format seconds into HH:MM:SS"""
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    
    def start_timer(self):
        """Start the timer"""
        if self.timer_paused:
            # Resume timer
            self.timer_paused = False
            self.timer_running = True
        else:
            # Start new timer
            self.timer_running = True
            self.stop_thread.clear()
            
            # Create and start timer thread
            self.timer_thread = threading.Thread(target=self.run_timer)
            self.timer_thread.daemon = True
            self.timer_thread.start()
        
        # Update button states
        self.start_button.config(state=DISABLED)
        self.pause_button.config(state=NORMAL)
    
    def pause_timer(self):
        """Pause the timer"""
        self.timer_paused = True
        self.timer_running = False
        
        # Update button states
        self.start_button.config(state=NORMAL, text="Resume")
        self.pause_button.config(state=DISABLED)
    
    def reset_timer(self):
        """Reset the timer"""
        # Stop current timer
        if self.timer_running or self.timer_paused:
            self.stop_thread.set()
            if self.timer_thread and self.timer_thread.is_alive():
                self.timer_thread.join(0.1)
        
        # Reset timer state
        self.timer_running = False
        self.timer_paused = False
        self.current_timer_type = "work"
        self.time_remaining = self.durations["work"]
        
        # Update UI
        self.timer_display.config(text=self.format_time(self.time_remaining))
        self.progress_bar.config(value=0, bootstyle=SUCCESS)
        self.session_type_label.config(text="WORK SESSION", bootstyle=SUCCESS)
        
        # Reset button states
        self.start_button.config(state=NORMAL, text="Start")
        self.pause_button.config(state=DISABLED)
    
    def toggle_timer(self):
        """Toggle between start and pause (for keyboard shortcut)"""
        if self.timer_running:
            self.pause_timer()
        else:
            self.start_timer()
    
    def run_timer(self):
        """Run the timer in a separate thread"""
        start_time = time.time()
        original_duration = self.durations[self.current_timer_type]
        elapsed_paused_time = 0
        last_update_time = start_time
        
        while self.time_remaining > 0 and not self.stop_thread.is_set():
            if self.timer_paused:
                # Track paused time
                if not elapsed_paused_time:
                    elapsed_paused_time = time.time()
                time.sleep(0.1)
                continue
            
            # If we were paused, adjust the start time
            if elapsed_paused_time:
                paused_duration = time.time() - elapsed_paused_time
                start_time += paused_duration
                elapsed_paused_time = 0
            
            # Calculate time remaining
            elapsed = time.time() - start_time
            self.time_remaining = max(0, original_duration - int(elapsed))
            
            # Update UI every 0.1 seconds
            if time.time() - last_update_time >= 0.1:
                self.update_ui()
                last_update_time = time.time()
            
            time.sleep(0.05)  # Small sleep to prevent high CPU usage
        
        # Timer completed
        if not self.stop_thread.is_set() and self.time_remaining <= 0:
            self.time_remaining = 0
            self.update_ui()
            self.timer_completed()
    
    def update_ui(self):
        """Update the UI elements with current timer state"""
        # Update timer display
        self.root.after(0, lambda: self.timer_display.config(text=self.format_time(self.time_remaining)))
        
        # Update progress bar
        progress = 100 - (self.time_remaining / self.durations[self.current_timer_type] * 100)
        self.root.after(0, lambda: self.progress_bar.config(value=progress))
    
    def timer_completed(self):
        """Handle timer completion"""
        # Play sound alert
        self.play_sound()
        
        # Show visual indication
        self.flash_timer_display()
        
        # Reset timer state
        self.timer_running = False
        self.timer_paused = False
        
        # Update button states
        self.root.after(0, lambda: self.start_button.config(state=NORMAL, text="Start"))
        self.root.after(0, lambda: self.pause_button.config(state=DISABLED))
        
        # Handle session completion
        if self.current_timer_type == "work":
            # Increment completed sessions
            self.completed_sessions += 1
            self.root.after(0, lambda: self.session_label.config(
                text=f"Sessions: {self.completed_sessions}/{self.total_sessions}"
            ))
            
            # Determine next break type
            if self.completed_sessions % self.total_sessions == 0:
                # Long break after 4 sessions
                self.current_timer_type = "long_break"
                self.time_remaining = self.durations["long_break"]
                self.root.after(0, lambda: self.session_type_label.config(
                    text="LONG BREAK", bootstyle=INFO
                ))
                self.root.after(0, lambda: self.progress_bar.config(bootstyle=INFO))
                
                # Show notification
                self.show_notification(
                    "Time for a long break!",
                    "Take 15 minutes to relax and recharge."
                )
            else:
                # Short break after sessions 1-3
                self.current_timer_type = "short_break"
                self.time_remaining = self.durations["short_break"]
                self.root.after(0, lambda: self.session_type_label.config(
                    text="SHORT BREAK", bootstyle=WARNING
                ))
                self.root.after(0, lambda: self.progress_bar.config(bootstyle=WARNING))
                
                # Show notification
                self.show_notification(
                    "Time for a short break!",
                    "Take 5 minutes to relax."
                )
        else:
            # After break, go back to work
            self.current_timer_type = "work"
            self.time_remaining = self.durations["work"]
            self.root.after(0, lambda: self.session_type_label.config(
                text="WORK SESSION", bootstyle=SUCCESS
            ))
            self.root.after(0, lambda: self.progress_bar.config(bootstyle=SUCCESS))
            
            # Show notification
            self.show_notification(
                "Break finished!",
                "Time to get back to work."
            )
        
        # Update timer display with new time
        self.root.after(0, lambda: self.timer_display.config(text=self.format_time(self.time_remaining)))
    
    def play_sound(self):
        """Play a sound alert when timer ends"""
        try:
            # Use system bell as a simple alert
            self.root.bell()
        except:
            pass
    
    def flash_timer_display(self):
        """Flash the timer display as a visual indication"""
        original_bg = self.timer_display.cget("background")
        original_fg = self.timer_display.cget("foreground")
        
        # Flash 3 times
        for _ in range(3):
            # Change to alert color
            self.root.after(0, lambda: self.timer_display.config(
                background=self.style.colors.danger,
                foreground="white"
            ))
            self.root.update()
            time.sleep(0.3)
            
            # Change back to original color
            self.root.after(0, lambda: self.timer_display.config(
                background=original_bg,
                foreground=original_fg
            ))
            self.root.update()
            time.sleep(0.3)
    
    def show_notification(self, title, message):
        """Show a system notification"""
        try:
            notification.notify(
                title=title,
                message=message,
                app_name="Pomodoro Timer",
                timeout=10
            )
        except Exception as e:
            print(f"Notification error: {e}")
    
    def change_theme(self, event=None):
        """Change the application theme"""
        selected_theme = self.theme_var.get()
        self.theme = selected_theme
        self.style = ttk.Style(theme=selected_theme)
        self.save_preferences()
    
    def update_volume(self, event=None):
        """Update the volume level"""
        self.volume = self.volume_var.get()
        self.volume_label.config(text=f"{self.volume}%")
        self.save_preferences()
    
    def load_preferences(self):
        """Load user preferences from file"""
        try:
            if os.path.exists("preferences.json"):
                with open("preferences.json", "r") as f:
                    prefs = json.load(f)
                    self.theme = prefs.get("theme", self.theme)
                    self.volume = prefs.get("volume", self.volume)
        except Exception as e:
            print(f"Error loading preferences: {e}")
    
    def save_preferences(self):
        """Save user preferences to file"""
        try:
            prefs = {
                "theme": self.theme,
                "volume": self.volume
            }
            with open("preferences.json", "w") as f:
                json.dump(prefs, f)
        except Exception as e:
            print(f"Error saving preferences: {e}")
    
    def on_closing(self):
        """Handle application closing"""
        if self.timer_running or self.timer_paused:
            # Ask for confirmation if timer is running
            confirm = Messagebox.yesno(
                "Confirm Exit",
                "Timer is still running. Are you sure you want to exit?",
                parent=self.root
            )
            if not confirm:
                return
        
        # Stop timer thread
        self.stop_thread.set()
        if self.timer_thread and self.timer_thread.is_alive():
            self.timer_thread.join(0.1)
        
        # Save preferences
        self.save_preferences()
        
        # Close application
        self.root.destroy()
        sys.exit(0)

def main():
    # Create root window
    root = ttk.Window(themename="darkly")
    
    # Create Pomodoro Timer
    app = PomodoroTimer(root)
    
    # Start main loop
    root.mainloop()

if __name__ == "__main__":
    main()