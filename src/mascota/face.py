# Pure-Python: no imports de MicroPython/hardware. Dibuja sobre cualquier
# objeto que implemente fill(color), fill_rect(x, y, w, h, color) y
# line(x0, y0, x1, y1, color) -- el mismo subset que expone el driver real
# (device/st7789py.py), así que esta lógica se testea en la compu con un
# canvas falso y corre sin cambios contra la pantalla.

from math import sqrt

from mascota.state import Mood

BLACK = 0x0000
WHITE = 0xFFFF

EYE_RADIUS_RATIO = 0.104
EYE_Y_RATIO = 0.38
EYE_OFFSET_X_RATIO = 0.22

MOUTH_WIDTH_RATIO = 0.4
MOUTH_Y_RATIO = 0.68
MOUTH_SEGMENTS = 8
OPEN_MOUTH_SIZE_RATIO = 0.08

# Positivo = sonrisa (centro de la boca más abajo que los bordes),
# negativo = mueca triste (centro más arriba), 0 = línea recta.
MOUTH_AMPLITUDE_RATIO = {
    Mood.HAPPY: 0.05,
    Mood.EXCITED: 0.09,
    Mood.SAD: -0.05,
    Mood.HUNGRY: 0.0,
    Mood.TIRED: 0.0,
    Mood.NEUTRAL: 0.0,
}


def draw_face(canvas, mood, width, height, bg_color=BLACK, fg_color=WHITE):
    canvas.fill(bg_color)
    _draw_eyes(canvas, mood, width, height, fg_color)
    _draw_mouth(canvas, mood, width, height, fg_color)


def _draw_eyes(canvas, mood, width, height, color):
    # El radio escala con el lado más chico de la pantalla (no con `width`
    # a secas) para que no se agranden desproporcionadamente en horizontal,
    # donde width >> height.
    radius = int(min(width, height) * EYE_RADIUS_RATIO)
    center_y = int(height * EYE_Y_RATIO)
    offset_x = int(width * EYE_OFFSET_X_RATIO)
    upper_half_only = mood == Mood.TIRED

    left_x = width // 2 - offset_x
    right_x = width // 2 + offset_x
    _draw_filled_circle(canvas, left_x, center_y, radius, color, upper_half_only)
    _draw_filled_circle(canvas, right_x, center_y, radius, color, upper_half_only)


def _draw_filled_circle(canvas, cx, cy, radius, color, upper_half_only=False):
    # Ojo "redondo": una fila (fill_rect de 1px de alto) por cada línea
    # horizontal del círculo, con el ancho que marca la ecuación del círculo.
    # TIRED solo dibuja la mitad de arriba -> ojo entrecerrado.
    for dy in range(-radius, radius + 1):
        if upper_half_only and dy > 0:
            continue
        half_w = int(sqrt(radius * radius - dy * dy))
        canvas.fill_rect(cx - half_w, cy + dy, 2 * half_w + 1, 1, color)


def _draw_mouth(canvas, mood, width, height, color):
    if mood == Mood.HUNGRY:
        _draw_open_mouth(canvas, width, height, color)
        return
    _draw_curved_mouth(canvas, mood, width, height, color)


def _draw_curved_mouth(canvas, mood, width, height, color):
    amplitude = width * MOUTH_AMPLITUDE_RATIO[mood]
    mouth_w = int(width * MOUTH_WIDTH_RATIO)
    base_y = int(height * MOUTH_Y_RATIO)
    left_x = width // 2 - mouth_w // 2
    right_x = width // 2 + mouth_w // 2

    prev_point = None
    for i in range(MOUTH_SEGMENTS + 1):
        t = -1 + 2 * i / MOUTH_SEGMENTS
        x = int(left_x + (right_x - left_x) * i / MOUTH_SEGMENTS)
        y = int(base_y + amplitude * (1 - t * t))
        if prev_point is not None:
            canvas.line(prev_point[0], prev_point[1], x, y, color)
        prev_point = (x, y)


def _draw_open_mouth(canvas, width, height, color):
    size = int(width * OPEN_MOUTH_SIZE_RATIO)
    x = width // 2 - size // 2
    y = int(height * MOUTH_Y_RATIO) - size // 2
    canvas.fill_rect(x, y, size, size, color)
