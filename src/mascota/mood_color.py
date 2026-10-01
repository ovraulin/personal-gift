# Pure-Python: no imports de MicroPython/hardware. Mapea cada Mood a un
# color RGB (0-255 por canal). El wiring con el LED RGB físico (pin, orden
# de canales de esta placa) vive en device/main.py.

from mascota.state import Mood

MOOD_COLORS = {
    Mood.NEUTRAL: (40, 40, 40),
    Mood.HAPPY: (0, 255, 0),
    Mood.SAD: (0, 0, 255),
    Mood.HUNGRY: (255, 100, 0),
    Mood.TIRED: (80, 0, 120),
    Mood.EXCITED: (255, 220, 0),
}


def color_for_mood(mood):
    return MOOD_COLORS[mood]
