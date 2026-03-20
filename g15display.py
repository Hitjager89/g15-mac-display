import hid
import time
import psutil
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

VENDOR   = 0x046d
LCD_PID  = 0xc227
WIDTH    = 160
HEIGHT   = 43
USER_NAME = "User Name"

def render_to_buffer(img):
    pixels = img.load()
    buf = bytearray(992)
    buf[0] = 0x03
    for col in range(WIDTH):
        for page in range(6):
            byte = 0
            for bit in range(8):
                row = page * 8 + bit
                if row < HEIGHT and pixels[col, row] == 0:
                    byte |= (1 << bit)
            buf[32 + page * WIDTH + col] = byte
    return bytes(buf)

def new_img():
    img = Image.new("1", (WIDTH, HEIGHT), 1)
    return img, ImageDraw.Draw(img), ImageFont.load_default()

def screen_welcome():
    img, draw, font = new_img()
    draw.text((35, 2),  "G15 Display", font=font, fill=0)
    draw.line([(0, 12), (WIDTH, 12)], fill=0)
    draw.text((20, 16), f"Willkommen, {USER_NAME}!", font=font, fill=0)
    draw.line([(0, 27), (WIDTH, 27)], fill=0)
    draw.text((30, 31), "System gestartet", font=font, fill=0)
    return render_to_buffer(img)

def screen_clock():
    img, draw, font = new_img()
    now = datetime.now()
    draw.text((20, 2),  now.strftime("%H:%M:%S"), font=font, fill=0)
    draw.text((10, 14), now.strftime("%A, %d.%m.%Y"), font=font, fill=0)
    draw.line([(0, 25), (WIDTH, 25)], fill=0)
    draw.text((15, 30), "1:Uhr  2:System  3:Disk", font=font, fill=0)
    return render_to_buffer(img)

def screen_system():
    img, draw, font = new_img()
    cpu      = psutil.cpu_percent(interval=None)
    mem      = psutil.virtual_memory()
    used_gb  = mem.used  / 1024**3
    total_gb = mem.total / 1024**3
    wired_gb = mem.wired / 1024**3
    draw.text((0, 0),  "-- System --", font=font, fill=0)
    draw.text((0, 10), f"CPU:   {cpu:5.1f}%", font=font, fill=0)
    draw.text((0, 20), f"RAM:   {used_gb:.1f} / {total_gb:.0f} GB", font=font, fill=0)
    draw.text((0, 30), f"Wired: {wired_gb:.1f} GB", font=font, fill=0)
    return render_to_buffer(img)

def screen_disk():
    img, draw, font = new_img()
    disk      = psutil.disk_usage("/")
    used_gb   = disk.used  / 1024**3
    total_gb  = disk.total / 1024**3
    free_gb   = disk.free  / 1024**3
    bar_width = int((WIDTH - 4) * disk.percent / 100)
    draw.text((0, 0),  "-- Festplatte --", font=font, fill=0)
    draw.text((0, 10), f"Gesamt:  {total_gb:.0f} GB", font=font, fill=0)
    draw.text((0, 20), f"Belegt:  {used_gb:.1f} GB", font=font, fill=0)
    draw.text((0, 30), f"Frei:    {free_gb:.1f} GB", font=font, fill=0)
    draw.rectangle([(2, 40), (WIDTH-2, 42)], outline=0)
    draw.rectangle([(2, 40), (2 + bar_width, 42)], fill=0)
    return render_to_buffer(img)

SCREENS = [screen_clock, screen_system, screen_disk]
BUTTON_MAP = {
    0x02: 0,
    0x04: 1,
    0x08: 2,
}
current_screen = 0

lcd = hid.Device(VENDOR, LCD_PID)
psutil.cpu_percent(interval=None)

print("G15 Display gestartet.")
lcd.write(screen_welcome())
time.sleep(3)

print("Taste 1=Uhr  2=System  3=Disk")
try:
    while True:
        lcd.nonblocking = True
        data = lcd.read(8)
        if data and len(data) >= 3 and data[2] != 0:
            if data[2] in BUTTON_MAP:
                current_screen = BUTTON_MAP[data[2]]
                print(f"-> Screen {current_screen}")

        lcd.nonblocking = False
        lcd.write(SCREENS[current_screen]())
        time.sleep(0.5)

except KeyboardInterrupt:
    print("Beendet.")
finally:
    lcd.close()
