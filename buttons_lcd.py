#!/usr/bin/env python3
import time
import RPi.GPIO as GPIO
from smbus2 import SMBus

I2C_ADDR = 0x27
I2C_BUS = 1
LCD_CHR = 1
LCD_CMD = 0
LCD_LINE_1 = 0x80
LCD_LINE_2 = 0xC0
ENABLE = 0b00000100
BACKLIGHT = 0b00001000
E_PULSE = 0.0005
E_DELAY = 0.0005

class LCD:
    def __init__(self):
        self.bus = SMBus(I2C_BUS)
        time.sleep(0.05)
        for cmd in (0x33,0x32,0x28,0x0C,0x06,0x01):
            self._send(cmd, LCD_CMD)
            time.sleep(0.002)

    def _write(self, data):
        self.bus.write_byte(I2C_ADDR, data | BACKLIGHT)

    def _pulse(self, data):
        time.sleep(E_DELAY)
        self._write(data | ENABLE)
        time.sleep(E_PULSE)
        self._write(data & ~ENABLE)
        time.sleep(E_DELAY)

    def _send(self, bits, mode):
        high = mode | (bits & 0xF0)
        low  = mode | ((bits << 4) & 0xF0)
        self._write(high); self._pulse(high)
        self._write(low);  self._pulse(low)

    def write_line(self, text, line):
        self._send(line, LCD_CMD)
        for ch in text.ljust(16):
            self._send(ord(ch), LCD_CHR)

    def clear(self):
        self._send(0x01, LCD_CMD)
        time.sleep(0.002)

lcd = LCD()
lcd.write_line("Ready...", LCD_LINE_1)
lcd.write_line("Press a button", LCD_LINE_2)

BUTTONS = {
    17: "Red Button",
    27: "Green Button",
    22: "Yellow Button",
    23: "Blue Button"
}

GPIO.setmode(GPIO.BCM)
for pin in BUTTONS:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def show(pin):
    lcd.clear()
    lcd.write_line("You pressed:", LCD_LINE_1)
    lcd.write_line(BUTTONS[pin], LCD_LINE_2)

for pin in BUTTONS:
    GPIO.add_event_detect(pin, GPIO.FALLING, callback=show, bouncetime=100)

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    lcd.clear()
    GPIO.cleanup()
