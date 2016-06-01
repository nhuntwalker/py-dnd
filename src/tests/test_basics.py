import pytest


def test_dice_roll():
    """Test that the output of a dice roll is a list"""
    from main import roll_dice
    assert type(roll_dice()) == list


def test_many_dice():
    """Test that when 3 dice are rolled, three numbers come out"""
    from main import roll_dice
    assert len(roll_dice(num_die=3)) == 3


def test_dice_range():
    """Test that when multiple dice are rolled and a range is given,
    the total of the dice rolls is less than or equal to
    that limit multipled"""
    from main import roll_dice
    assert sum(roll_dice(20, 4)) <= 80


def char_setup():
    from main import Character
    bob = Character()
    bob.char_name = "Bob"
    bob.money = {
        "GP": 100, "SP": 100, "EP": 100, "CP": 100, "PP": 100
    }
    return bob

STATS_TABLE = [
    "strength", "dexterity", "charisma", "constitution",
    "intelligence", "wisdom"
]

STATS_MODIFIER_TABLE = [
    (1, -5), (2, -4), (3, -4), (4, -3), (5, -3), (6, -2), (7, -2),
    (8, -1), (9, -1), (10, 0), (11, 0), (12, 1), (13, 1), (14, 2), (15, 2),
    (16, 3), (17, 3), (18, 4), (19, 4), (20, 5), (21, 5), (22, 6), (23, 6),
    (24, 7), (25, 7), (26, 8), (27, 8), (28, 9), (29, 9), (30, 10)
]

STATS_CHANGE_TABLE = [
    ("strength", 1), ("strength", 5),
    ("strength", -3)
]

MONEY_TYPES = [
    "GP", "CP", "EP", "SP", "PP"
]

ADD_MONEY_TABLE = [
    ("GP", 5), ("GP", 1)
]

SPEND_MONEY_TABLE = [
    ("GP", 10, {"GP": 90, "SP": 100, "EP": 100, "CP": 100, "PP": 100}),
    ("SP", 10, {"GP": 100, "SP": 90, "EP": 100, "CP": 100, "PP": 100}),
    ("EP", 10, {"GP": 100, "SP": 100, "EP": 90, "CP": 100, "PP": 100}),
    ("CP", 10, {"GP": 100, "SP": 100, "EP": 100, "CP": 90, "PP": 100}),
    ("PP", 10, {"GP": 100, "SP": 100, "EP": 100, "CP": 100, "PP": 90}),
]

EXCHANGE_RATES = {
    "PP": {"GP": 10, "SP": 100, "EP": 20, "CP": 1000, "PP": 1},
    "GP": {"GP": 1, "SP": 10, "EP": 2, "CP": 100, "PP": 0.1},
    "EP": {"GP": 0.5, "SP": 5, "EP": 1, "CP": 50, "PP": 0.5},
    "SP": {"GP": 0.1, "SP": 1, "EP": 0.2, "CP": 10, "PP": 0.01},
    "CP": {"GP": 0.01, "SP": 0.1, "EP": 0.02, "CP": 1, "PP": 0.001},
}

EXCHANGE_TABLE = [
    ("GP", 1, "SP"), ("CP", 100, "GP"), ("SP", 50, "EP"),
    ("PP", 1, "CP"), ("EP", 20, "PP")
]

EXPERIENCE_TABLE = [
    (0, 1), (5, 1), (299, 1), (300, 2), (899, 2), (900, 3), (901, 3),
    (2700, 4), (6500, 5), (14000, 6), (23000, 7), (34000, 8),
    (48000, 9), (64000, 10), (85000, 11), (100000, 12), (120000, 13),
    (140000, 14), (165000, 15), (195000, 16), (225000, 17), (265000, 18),
    (305000, 19), (355000, 20), (355001, 20)
]

PROFICIENCY_TABLE = [
    (0, 2), (5, 2), (299, 2), (300, 4), (899, 4), (900, 6), (901, 6),
    (2700, 8), (6500, 11), (14000, 14), (23000, 17), (34000, 20),
    (48000, 24), (64000, 28), (85000, 32), (100000, 36), (120000, 41),
    (140000, 46), (165000, 51), (195000, 56), (225000, 62), (265000, 68),
    (305000, 74), (355000, 80), (355001, 80)
]


@pytest.mark.parametrize("stat", STATS_TABLE)
def test_char_has_stats(stat):
    bob = char_setup()
    assert hasattr(bob, stat)


@pytest.mark.parametrize("num, mod", STATS_MODIFIER_TABLE)
def test_char_test_modifier(num, mod):
    bob = char_setup()
    bob.strength = num
    assert bob.get_ability_modifier("strength") == mod


@pytest.mark.parametrize("stat, points", STATS_CHANGE_TABLE)
def test_change_stat(stat, points):
    bob = char_setup()
    bob.strength = 10
    old = bob.strength
    bob.change_stat(stat, points)
    assert bob.strength == old + points


def test_cant_change_stat():
    bob = char_setup()
    bob.strength = 10
    old = bob.strength
    assert bob.change_stat(
        "strength", -20) == "You can't decrease strength below 0\n(10 - 20 = -10)."


def test_has_money():
    bob = char_setup()
    assert type(bob.money) == dict


@pytest.mark.parametrize("money_type", MONEY_TYPES)
def test_has_money_types(money_type):
    bob = char_setup()
    assert money_type in bob.money.keys()


def test_show_money():
    bob = char_setup()
    print(bob.show_money())
    assert type(bob.show_money()) == str


@pytest.mark.parametrize("money_type, amt", ADD_MONEY_TABLE)
def test_add_money(money_type, amt):
    bob = char_setup()
    old_amt = bob.money[money_type]
    bob.add_money(money_type, amt)
    assert bob.money[money_type] == old_amt + amt


@pytest.mark.parametrize("money_type, amt, money_dict", SPEND_MONEY_TABLE)
def test_spend_money(money_type, amt, money_dict):
    bob = char_setup()
    bob.spend_money(money_type, amt)
    assert bob.money == money_dict


def test_cant_spend_money():
    bob = char_setup()
    assert bob.spend_money(
        "GP", 200) == "You don't have enough money for this."


def test_not_enough_to_make_change():
    bob = char_setup()
    assert bob.exchange_money(
        "GP", 200, "SP") == "You don't have enough GP for this exchange."


def test_cant_change_lt_1():
    bob = char_setup()
    assert bob.exchange_money(
        "GP", 1, "PP") == "You don't have enough GP for this exchange."


@pytest.mark.parametrize("cash_out, amt, cash_in", EXCHANGE_TABLE)
def test_exchange_money(cash_out, amt, cash_in):
    from copy import copy
    bob = char_setup()
    old = copy(bob.money)
    bob.exchange_money(cash_out, amt, cash_in)
    assert bob.money[cash_out] == old[cash_out] - amt
    assert bob.money[cash_in] == old[cash_in] + \
        EXCHANGE_RATES[cash_out][cash_in] * amt


def test_exchange_fractional():
    from copy import copy
    bob = char_setup()
    old = copy(bob.money)
    bob.exchange_money("GP", 22, "PP")
    assert bob.money["GP"] == old["GP"] - 20
    assert bob.money["PP"] == old["PP"] + 2


def test_add_experience():
    bob = char_setup()
    bob.gain_experience(100)
    assert bob.experience == 100


@pytest.mark.parametrize("xp, level", EXPERIENCE_TABLE)
def test_levelups(xp, level):
    bob = char_setup()
    bob.gain_experience(xp)
    assert bob.level == level


@pytest.mark.parametrize("xp, proficiency", PROFICIENCY_TABLE)
def test_proficiency_with_experience(xp, proficiency):
    bob = char_setup()
    bob.gain_experience(xp)
    assert bob.proficiency == proficiency

@pytest.mark.parametrize("this_stat", STATS_TABLE)
def test_roll_random_stats(this_stat):
    bob = char_setup()
    assert getattr(bob, this_stat) > 0 and getattr(bob, this_stat) < 20

def test_display_health():
    bob = char_setup()
    assert bob.current_hp == bob.max_hp‰
    out = bob.show_health()
    assert "Current HP: {}/{}".format(bob.current_hp, bob.max_hp) in out

def test_take_damage():
    bob = char_setup()
    bob.take_damage(1)
    assert bob.current_hp == bob.max_hp - 1

def test_take_critical_damage():
    bob = char_setup()
    bob.take_damage(10)
    assert bob.current_hp == 0

def test_heal_damage():
    bob = char_setup()
    bob.current_hp = bob.max_hp = 6
    bob.take_damage(3)
    bob.heal_damage(2)
    assert bob.current_hp == bob.max_hp - 1

def test_heal_more_than_max():
    bob = char_setup()
    bob.heal_damage(20)
    assert bob.current_hp == bob.max_hp

def test_carry_capacity():
    bob = char_setup()
    assert bob.carry_capacity == bob.strength * 15

def test_carry_capacity_changes_on_strength_change():
    """TODO: write a test where the strength changes and on that change
    the carry capacity changes."""
    assert False