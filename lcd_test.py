
import time
from smbus2 import SMBus

ADDR = 0x27
BUS  = 1

LCD_CHR = 1
LCD_CMD = 0
LCD_LINE_1 = 0x80
LCD_LINE_2 = 0xC0
ENABLE = 0b00000100
BACKLIGHT = 0b00001000
E_PULSE = 0.0005
E_DELAY = 0.0005

def write(bus, data):
    bus.write_byte(ADDR, data | BACKLIGHT)

def toggle(bus, data):
    time.sleep(E_DELAY)
    write(bus, data | ENABLE)
    time.sleep(E_PULSE)
    write(bus, data & ~ENABLE)
    time.sleep(E_DELAY)

def send(bus, bits, mode):
    high = mode | (bits & 0xF0)
    low  = mode | ((bits << 4) & 0xF0)
    write(bus, high); toggle(bus, high)
    write(bus, low);  toggle(bus, low)

def lcd_init(bus):
    time.sleep(0.05)
    for cmd in (0x33,0x32,0x28,0x0C,0x06,0x01):
        send(bus, cmd, LCD_CMD)
        time.sleep(0.002)

def lcd_write_line(bus, text, line):
    send(bus, line, LCD_CMD)
    for c in text.ljust(16):
        send(bus, ord(c), LCD_CHR)

with SMBus(BUS) as bus:
    lcd_init(bus)
    lcd_write_line(bus, "Hello, LCD!", LCD_LINE_1)
    lcd_write_line(bus, "I2C=0x27 OK", LCD_LINE_2)
    while True:
        time.sleep(1)
