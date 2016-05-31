import random


def roll_dice(sides=6, num_die=1):
    """This function will roll a specified number of die with a
    specified number of sides, returning a list of the resulting rolls.
    """
    return [random.randint(0, sides) for ii in range(num_die)]


class Character(object):
    """The base character object for building the different classes
    """
    char_name = ""
    char_class = ""
    char_race = ""
    char_align = ""

    level = 1
    proficiency = 2
    experience = 0
    speed = 0
    max_hp = 0
    current_hp = 0
    tmp_hp = 0

    strength = 0
    dexterity = 0
    constitution = 0
    intelligence = 0
    wisdom = 0
    charisma = 0

    def ability_modifier(self, stat):
        mod = getattr(self, stat)
        return (mod - 10) // 2

    def increase_stat(self, stat, points=1):
        current = getattr(self, stat)
        setattr(self, stat, current + points)
        new = getattr(self, stat)
        retun "{} increased from {} to {}".format(char_name, current, new)
