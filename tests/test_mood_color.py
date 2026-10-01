import pytest

from mascota.mood_color import color_for_mood
from mascota.state import Mood

ALL_MOODS = [
    Mood.NEUTRAL,
    Mood.HAPPY,
    Mood.SAD,
    Mood.HUNGRY,
    Mood.TIRED,
    Mood.EXCITED,
]


@pytest.mark.parametrize("mood", ALL_MOODS)
def test_every_mood_has_a_valid_rgb_color(mood):
    color = color_for_mood(mood)
    assert len(color) == 3
    assert all(isinstance(channel, int) for channel in color)
    assert all(0 <= channel <= 255 for channel in color)


def test_moods_map_to_distinct_colors():
    colors = [color_for_mood(mood) for mood in ALL_MOODS]
    assert len(set(colors)) == len(colors)
