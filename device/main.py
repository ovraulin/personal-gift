# Entry point para la ESP32-S3 (Waveshare ESP32-S3-LCD-1.47, 172x320 ST7789).
# Para deployar: copiar este archivo + st7789py.py (ambos de este directorio)
# y la carpeta src/mascota/ a la raíz del filesystem del device.

import time

import st7789py
from machine import SPI, Pin

from mascota.face import draw_face
from mascota.state import Mood

WIDTH = 172
HEIGHT = 320
MOOD_DELAY_SECONDS = 4

# Demo: itera todas las expresiones indefinidamente. Cuando haya lógica real
# de interacción, esto se reemplaza por el loop de PetState.tick() + redibujo
# solo cuando cambia el mood.
MOODS = [
    Mood.NEUTRAL,
    Mood.HAPPY,
    Mood.SAD,
    Mood.HUNGRY,
    Mood.TIRED,
    Mood.EXCITED,
]


def make_display():
    spi = SPI(2, baudrate=40_000_000, sck=Pin(40), mosi=Pin(45))
    display = st7789py.ST7789(
        spi,
        WIDTH,
        HEIGHT,
        reset=Pin(39, Pin.OUT),
        cs=Pin(42, Pin.OUT),
        dc=Pin(41, Pin.OUT),
        backlight=Pin(46, Pin.OUT),
        xstart=34,
        ystart=0,
    )
    display.init()
    display.backlight(1)
    return display


def main():
    display = make_display()
    while True:
        for mood in MOODS:
            draw_face(display, mood, WIDTH, HEIGHT)
            time.sleep(MOOD_DELAY_SECONDS)


if __name__ == "__main__":
    main()
