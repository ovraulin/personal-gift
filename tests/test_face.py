import pytest

from mascota.face import BLACK, EYE_RADIUS_RATIO, draw_face
from mascota.state import Mood

WIDTH = 172
HEIGHT = 320


class FakeCanvas:
    def __init__(self):
        self.calls = []

    def fill(self, color):
        self.calls.append(("fill", color))

    def fill_rect(self, x, y, w, h, color):
        self.calls.append(("fill_rect", x, y, w, h, color))

    def line(self, x0, y0, x1, y1, color):
        self.calls.append(("line", x0, y0, x1, y1, color))


ALL_MOODS = [
    Mood.HAPPY,
    Mood.SAD,
    Mood.HUNGRY,
    Mood.TIRED,
    Mood.EXCITED,
    Mood.NEUTRAL,
]


@pytest.mark.parametrize("mood", ALL_MOODS)
def test_draw_face_clears_background_first(mood):
    canvas = FakeCanvas()
    draw_face(canvas, mood, WIDTH, HEIGHT)
    assert canvas.calls[0] == ("fill", BLACK)


def _radius():
    return int(WIDTH * EYE_RADIUS_RATIO)


def _eye_rows(canvas):
    # Los ojos se dibujan como filas de 1px de alto (fill_rect con h == 1);
    # la boca de HUNGRY es el único fill_rect con h != 1, así que esto los
    # separa sin ambigüedad.
    return [c for c in canvas.calls if c[0] == "fill_rect" and c[4] == 1]


@pytest.mark.parametrize("mood", [m for m in ALL_MOODS if m != Mood.TIRED])
def test_eyes_are_round_not_rectangular(mood):
    canvas = FakeCanvas()
    draw_face(canvas, mood, WIDTH, HEIGHT)
    radius = _radius()
    rows = _eye_rows(canvas)
    assert len(rows) == 2 * (2 * radius + 1)

    widths = [row[3] for row in rows]
    assert max(widths) == 2 * radius + 1  # fila del medio: diámetro completo
    assert min(widths) < max(widths)  # no es un rectángulo uniforme


def test_tired_eyes_only_draw_the_top_half():
    canvas = FakeCanvas()
    draw_face(canvas, Mood.TIRED, WIDTH, HEIGHT)
    radius = _radius()
    rows = _eye_rows(canvas)
    assert len(rows) == 2 * (radius + 1)  # mitad del círculo -> entrecerrado


def test_eyes_are_horizontally_symmetric():
    canvas = FakeCanvas()
    draw_face(canvas, Mood.HAPPY, WIDTH, HEIGHT)
    rows = _eye_rows(canvas)
    centers = sorted({row[1] + (row[3] - 1) // 2 for row in rows})
    assert len(centers) == 2
    left_cx, right_cx = centers
    assert left_cx < WIDTH // 2 < right_cx
    assert (WIDTH // 2 - left_cx) == (right_cx - WIDTH // 2)


def test_hungry_mouth_is_a_small_square_not_a_curve():
    canvas = FakeCanvas()
    draw_face(canvas, Mood.HUNGRY, WIDTH, HEIGHT)
    assert not any(c[0] == "line" for c in canvas.calls)
    mouth_candidates = [c for c in canvas.calls if c[0] == "fill_rect" and c[4] != 1]
    assert len(mouth_candidates) == 1
    mouth = mouth_candidates[0]
    assert mouth[3] == mouth[4]  # ancho == alto (cuadrado)


@pytest.mark.parametrize("mood", [Mood.HAPPY, Mood.SAD, Mood.EXCITED, Mood.NEUTRAL])
def test_mouth_is_drawn_as_line_segments(mood):
    canvas = FakeCanvas()
    draw_face(canvas, mood, WIDTH, HEIGHT)
    line_calls = [c for c in canvas.calls if c[0] == "line"]
    assert len(line_calls) > 0
    assert all(isinstance(coord, int) for c in line_calls for coord in c[1:5])


def _mouth_center_y(canvas):
    line_calls = [c for c in canvas.calls if c[0] == "line"]
    mid = len(line_calls) // 2
    return line_calls[mid][2]  # y0 del segmento del medio


def _mouth_edge_y(canvas):
    line_calls = [c for c in canvas.calls if c[0] == "line"]
    return line_calls[0][2]  # y0 del primer segmento (borde izquierdo)


def test_happy_mouth_dips_down_in_the_center():
    canvas = FakeCanvas()
    draw_face(canvas, Mood.HAPPY, WIDTH, HEIGHT)
    assert _mouth_center_y(canvas) > _mouth_edge_y(canvas)


def test_sad_mouth_rises_in_the_center():
    canvas = FakeCanvas()
    draw_face(canvas, Mood.SAD, WIDTH, HEIGHT)
    assert _mouth_center_y(canvas) < _mouth_edge_y(canvas)


def test_excited_mouth_dips_more_than_happy():
    happy_canvas = FakeCanvas()
    draw_face(happy_canvas, Mood.HAPPY, WIDTH, HEIGHT)
    happy_dip = _mouth_center_y(happy_canvas) - _mouth_edge_y(happy_canvas)

    excited_canvas = FakeCanvas()
    draw_face(excited_canvas, Mood.EXCITED, WIDTH, HEIGHT)
    excited_dip = _mouth_center_y(excited_canvas) - _mouth_edge_y(excited_canvas)

    assert excited_dip > happy_dip


def test_neutral_mouth_is_flat():
    canvas = FakeCanvas()
    draw_face(canvas, Mood.NEUTRAL, WIDTH, HEIGHT)
    assert _mouth_center_y(canvas) == _mouth_edge_y(canvas)
