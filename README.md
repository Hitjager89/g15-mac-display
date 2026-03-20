# G15 Mac Display

Control the Logitech G15 (v1) LCD display on macOS with Apple Silicon (M1/M2/M4).

No official Logitech software needed - pure Python via hidapi.

## Features
- Clock and date screen
- CPU and RAM stats (macOS-aware)
- Disk usage with progress bar
- Switch screens via display buttons
- Welcome screen on startup
- Autostart via LaunchDaemon

## Requirements
- macOS with Apple Silicon (M1/M2/M4)
- Homebrew
- Python 3 via Homebrew

## Installation

### 1. Install dependencies
```bash
brew install hidapi python3
python3 -m venv g15env
source g15env/bin/activate
pip install hid psutil pillow
```

### 2. Edit username
Open g15display.py and set your name:
```python
USER_NAME = "YourName"
```

### 3. Run manually
```bash
sudo ~/g15env/bin/python3 g15display.py
```

### 4. Autostart via LaunchDaemon
```bash
sudo cp de.Hitjager89.g15display.plist /Library/LaunchDaemons/
sudo chown root:wheel /Library/LaunchDaemons/de.Hitjager89.g15display.plist
sudo chmod 644 /Library/LaunchDaemons/de.Hitjager89.g15display.plist
sudo launchctl bootstrap system /Library/LaunchDaemons/de.Hitjager89.g15display.plist
```

## Button Mapping
| Button | Action |
|--------|--------|
| 1 | Clock and Date |
| 2 | CPU and RAM |
| 3 | Disk Usage |

## Why sudo?
macOS requires root access to open HID devices not claimed by a system driver.
