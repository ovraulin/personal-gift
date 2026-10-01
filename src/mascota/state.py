# Este módulo es Python puro: nada de `machine`, `st7789py` ni imports
# específicos de MicroPython. También evita `enum.Enum`, `dataclasses`,
# `typing` y `match` statements, que tienen soporte parcial o nulo en
# MicroPython, para poder correr el mismo código en la compu (tests/lint)
# y en el ESP32-S3 sin modificaciones.

_MIN_STAT = 0
_MAX_STAT = 100


def _clamp(value):
    if value < _MIN_STAT:
        return _MIN_STAT
    if value > _MAX_STAT:
        return _MAX_STAT
    return value


class Mood:
    HAPPY = "happy"
    SAD = "sad"
    HUNGRY = "hungry"
    TIRED = "tired"
    EXCITED = "excited"
    NEUTRAL = "neutral"


class PetState:
    HUNGER_RATE_PER_SEC = 1.0 / 60
    ENERGY_RATE_PER_SEC = 1.0 / 90
    AFFECTION_RATE_PER_SEC = 1.0 / 120

    HUNGRY_THRESHOLD = 70
    TIRED_THRESHOLD = 30
    LOW_AFFECTION_THRESHOLD = 20
    HAPPY_AFFECTION_THRESHOLD = 60
    EXCITED_ENERGY_THRESHOLD = 70

    def __init__(self, hunger=20, energy=80, affection=50):
        self.hunger = _clamp(hunger)
        self.energy = _clamp(energy)
        self.affection = _clamp(affection)

    def tick(self, dt_seconds):
        self.hunger = _clamp(self.hunger + self.HUNGER_RATE_PER_SEC * dt_seconds)
        self.energy = _clamp(self.energy - self.ENERGY_RATE_PER_SEC * dt_seconds)
        self.affection = _clamp(
            self.affection - self.AFFECTION_RATE_PER_SEC * dt_seconds
        )

    def feed(self, amount=30):
        self.hunger = _clamp(self.hunger - amount)

    def play(self, affection_gain=15, energy_cost=10):
        self.affection = _clamp(self.affection + affection_gain)
        self.energy = _clamp(self.energy - energy_cost)

    def rest(self, amount=40):
        self.energy = _clamp(self.energy + amount)

    @property
    def mood(self):
        if self.hunger >= self.HUNGRY_THRESHOLD:
            return Mood.HUNGRY
        if self.energy <= self.TIRED_THRESHOLD:
            return Mood.TIRED
        if self.affection <= self.LOW_AFFECTION_THRESHOLD:
            return Mood.SAD
        if (
            self.affection >= self.HAPPY_AFFECTION_THRESHOLD
            and self.energy >= self.EXCITED_ENERGY_THRESHOLD
        ):
            return Mood.EXCITED
        if self.affection >= self.HAPPY_AFFECTION_THRESHOLD:
            return Mood.HAPPY
        return Mood.NEUTRAL
