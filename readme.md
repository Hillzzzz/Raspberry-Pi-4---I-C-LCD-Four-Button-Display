# Raspberry Pi 4 - I²C 1602 LCD + Button Display Project

This project demonstrates how to connect a 1602 I²C LCD and four push-buttons to a Raspberry Pi 4.  
When a button is pressed, the LCD displays the name (or color) of the button.

---

## 🧰 Hardware Used
- Raspberry Pi 4
- 1602 LCD with I²C backpack (PCF8574)
- 4x push buttons (4-pin tactile switches)
- Jumper wires
- Breadboard

---

## 🔌 Wiring

### LCD (I²C)
| LCD Pin | Raspberry Pi Pin |
|--------|------------------|
| VCC    | 5V (pin 4)       |
| GND    | GND (pin 6)      |
| SDA    | GPIO2 SDA (pin 3)|
| SCL    | GPIO3 SCL (pin 5)|

### Buttons (using internal pull-up)
Each button has *two legs on each internal side* — only one side is used.

| Button Color | GPIO Pin | Pi Header | Other Leg → GND |
|------------|---------|-----------|-----------------|
| Red        | GPIO17  | pin 11    | GND             |
| Green      | GPIO27  | pin 13    | GND             |
| Yellow     | GPIO22  | pin 15    | GND             |
| Blue       | GPIO23  | pin 16    | GND             |

---

## 🎛 Enable I²C
```bash
sudo raspi-config
# Interface Options → I2C → Enable
sudo reboot
