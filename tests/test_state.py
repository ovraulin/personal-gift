from mascota.state import Mood, PetState


def test_default_state():
    pet = PetState()
    assert pet.hunger == 20
    assert pet.energy == 80
    assert pet.affection == 50


def test_tick_decays_stats():
    pet = PetState(hunger=20, energy=80, affection=50)
    pet.tick(60)
    assert pet.hunger > 20
    assert pet.energy < 80
    assert pet.affection < 50


def test_tick_clamps_hunger_at_max():
    pet = PetState(hunger=99, energy=80, affection=50)
    pet.tick(10_000)
    assert pet.hunger == 100


def test_tick_clamps_energy_and_affection_at_min():
    pet = PetState(hunger=20, energy=1, affection=1)
    pet.tick(10_000)
    assert pet.energy == 0
    assert pet.affection == 0


def test_feed_reduces_hunger_and_clamps():
    pet = PetState(hunger=20)
    pet.feed(amount=30)
    assert pet.hunger == 0

    pet2 = PetState(hunger=5)
    pet2.feed(amount=30)
    assert pet2.hunger == 0


def test_play_raises_affection_and_lowers_energy():
    pet = PetState(energy=80, affection=50)
    pet.play(affection_gain=15, energy_cost=10)
    assert pet.affection == 65
    assert pet.energy == 70


def test_rest_raises_energy_and_clamps():
    pet = PetState(energy=80)
    pet.rest(amount=40)
    assert pet.energy == 100


def test_mood_hungry_takes_priority():
    pet = PetState(hunger=90, energy=5, affection=90)
    assert pet.mood == Mood.HUNGRY


def test_mood_tired():
    pet = PetState(hunger=0, energy=10, affection=50)
    assert pet.mood == Mood.TIRED


def test_mood_sad():
    pet = PetState(hunger=0, energy=50, affection=5)
    assert pet.mood == Mood.SAD


def test_mood_excited():
    pet = PetState(hunger=0, energy=90, affection=90)
    assert pet.mood == Mood.EXCITED


def test_mood_happy():
    pet = PetState(hunger=0, energy=50, affection=90)
    assert pet.mood == Mood.HAPPY


def test_mood_neutral():
    pet = PetState(hunger=20, energy=50, affection=50)
    assert pet.mood == Mood.NEUTRAL
