# Pomodoro Timer

A professional Pomodoro Timer application built with Python and ttkbootstrap that helps users maintain focus and productivity.

## Features

### Timer Display
- Large, clear digital numbers in HH:MM:SS format
- Default work session: 25 minutes
- Short break: 5 minutes
- Long break: 15 minutes

### Control Buttons
- Start button (primary color)
- Pause/Resume button (warning color)
- Reset button (danger color)
- All buttons have hover effects

### Session Management
- Tracks and displays completed Pomodoro cycles (0/4)
- Automatically suggests break type:
  - Short break after sessions 1-3
  - Long break after session 4
- Resets cycle count after 4 sessions

### User Interface
- Dark mode theme for reduced eye strain
- Progress bar showing current session progress
- Session type indicator (Work/Break)
- Centered layout with proper padding and spacing

### Notifications
- Plays a gentle sound alert when timer ends
- Displays a system notification
- Visual indication when session completes

### Additional Features
- Saves user preferences (theme, volume)
- Handles application closing gracefully
- Implements keyboard shortcuts (space for start/pause, r for reset)
- Ensures the timer runs accurately without drift

## Requirements

- Python 3.x
- ttkbootstrap
- plyer (for notifications)

## Installation

1. Clone this repository or download the source code
2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```
3. Run the application:
   ```
   python pomodoro_timer.py
   ```

## How to Use

1. Start the timer by clicking the "Start" button or pressing the space bar
2. Pause/Resume the timer by clicking the "Pause" button or pressing the space bar again
3. Reset the timer by clicking the "Reset" button or pressing "r"
4. The application will automatically suggest breaks after work sessions:
   - Short break (5 minutes) after sessions 1-3
   - Long break (15 minutes) after session 4
5. Change the theme using the dropdown menu in the settings section
6. Adjust the notification volume using the slider

## The Pomodoro Technique

The Pomodoro Technique is a time management method developed by Francesco Cirillo in the late 1980s. It uses a timer to break work into intervals, traditionally 25 minutes in length, separated by short breaks. These intervals are known as "pomodoros".

The basic steps are:
1. Decide on the task to be done
2. Set the timer for 25 minutes (one pomodoro)
3. Work on the task until the timer rings
4. Take a short break (5 minutes)
5. After four pomodoros, take a longer break (15-30 minutes)

This application helps you implement this technique effectively to improve productivity and focus.

## License

This project is licensed under the MIT License - see the LICENSE file for details.