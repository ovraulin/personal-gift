# Entry point para la ESP32-S3 (Waveshare ESP32-S3-LCD-1.47, 172x320 ST7789,
# usada en horizontal: rotation=1 -> 320x172).
# Para deployar: copiar este archivo + st7789py.py (ambos de este directorio)
# y la carpeta src/mascota/ a la raíz del filesystem del device.

import time

import neopixel
import st7789py
from machine import SPI, Pin

from mascota.face import draw_face
from mascota.mood_color import color_for_mood
from mascota.state import Mood

WIDTH = 320
HEIGHT = 172
MOOD_DELAY_SECONDS = 4
RGB_LED_PIN = 38

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
        xstart=0,
        ystart=34,
    )
    display.init(rotation=1)
    display.backlight(1)
    return display


def make_rgb_led():
    return neopixel.NeoPixel(Pin(RGB_LED_PIN), 1)


def set_rgb_led(led, color):
    # Esta placa manda los canales invertidos: pedís (r, g, b) y sale en
    # pantalla como si fuera (g, r, b). Lo compensamos acá al escribir.
    r, g, b = color
    led[0] = (g, r, b)
    led.write()


def main():
    display = make_display()
    led = make_rgb_led()
    while True:
        for mood in MOODS:
            draw_face(display, mood, WIDTH, HEIGHT)
            set_rgb_led(led, color_for_mood(mood))
            time.sleep(MOOD_DELAY_SECONDS)


if __name__ == "__main__":
    main()
