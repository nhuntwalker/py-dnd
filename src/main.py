import random


def roll_dice(sides=6, num_die=1):
    """This function will roll a specified number of die with a
    specified number of sides, returning a list of the resulting rolls.
    """
    if sides <= 2:
        return "Your dice have too few sides. You need at least 3 sides."
    if num_die < 1:
        return "You need to roll at least one die"

    return [random.randint(1, sides) for ii in range(num_die)]

EXCHANGE_RATES = {
    "PP": {"GP": 10, "SP": 100, "EP": 20, "CP": 1000, "PP": 1},
    "GP": {"GP": 1, "SP": 10, "EP": 2, "CP": 100, "PP": 0.1},
    "EP": {"GP": 0.5, "SP": 5, "EP": 1, "CP": 50, "PP": 0.5},
    "SP": {"GP": 0.1, "SP": 1, "EP": 0.2, "CP": 10, "PP": 0.01},
    "CP": {"GP": 0.01, "SP": 0.1, "EP": 0.02, "CP": 1, "PP": 0.001},
}

LEVEL_THRESHOLDS = [
    0, 300, 900, 2700, 6500, 14000, 23000, 34000, 48000, 64000, 85000,
    100000, 120000, 140000, 165000, 195000, 225000, 265000, 305000,
    355000
]

PROFICIENCY_ARR = [
    2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6
]


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

    carry_weight = 0
    carry_capacity = 0

    strength = 0
    dexterity = 0
    constitution = 0
    intelligence = 0
    wisdom = 0
    charisma = 0

    money = {
        "GP": 0, "SP": 0, "EP": 0, "CP": 0, "PP": 0
    }

    ideals = []
    skills = []
    bonds = []
    flaws = []
    traits = []
    treasure = []

    weight = 0
    height = 0

    attacks_spellcasting = {}
    spells_list = {}

    hit_die = 1
    hit_die_sides = 6

    def __init__(self):
        self.roll_random_stats()
        self.max_hp = sum(roll_dice(self.hit_die_sides, self.hit_die)
                          ) + self.get_ability_modifier("constitution")
        self.current_hp = self.max_hp
        self.set_carry_capacity()

    def get_ability_modifier(self, stat):
        """This method gets the ability modifier number for a given ability.
        Given an ability score, the ability modifier is that (score - 10) / 2,
        rounded down."""
        mod = getattr(self, stat)
        return (mod - 10) // 2

    def change_stat(self, stat, points=1):
        """This method changes the value of a given statistic, either 
        increasing it or decreasing it by the amount specified."""
        current = getattr(self, stat)
        if current + points < 0:
            output = "You can't decrease {} below 0\n({} - {} = {})."
            return output.format(stat, current, abs(points), current + points)

        setattr(self, stat, current + points)
        new = getattr(self, stat)
        if points < 0:
            print("{} decreased from {} to {}.".format(
                self.char_name, current, new))
        else:
            print("{} increased from {} to {}.".format(
                self.char_name, current, new))

    def add_money(self, piece_type, amt):
        """This method adds money of one type to the character's overall
        stash of money.

        TODO: Allow for the addition of multiple types of coins."""
        self.money[piece_type] += amt

    def spend_money(self, piece_type, amt):
        """This method removes money from the character's overall stash
        by the amount specified. If the character doesn't have enough of
        the specified type, no change is committed."""
        if self.money[piece_type] - amt < 0:
            return "You don't have enough money for this."
        self.money[piece_type] -= amt

    def show_money(self):
        """A simple display of all of the money this character has."""
        output = "===================\n"
        output += "Your current money:\n|"
        for key, val in self.money.items():
            output += " {}: {} |".format(key, val)
        output += "\n==================="
        return output

    def exchange_money(self, exchange_this, amt, for_this):
        """This method exchanges a specified amount of one type of
        money for the equivalent amount of the other."""
        the_rate = EXCHANGE_RATES[exchange_this][for_this]
        if (amt * the_rate < 1) or (self.money[exchange_this] - amt < 0):
            output = "You don't have enough {} for this exchange."
            return output.format(exchange_this)
        new_amt = the_rate * amt
        if int(new_amt) != float(new_amt):
            new_amt = int(new_amt)
            amt = new_amt / the_rate
        self.money[exchange_this] -= amt
        self.money[for_this] += new_amt

    def gain_experience(self, new_xp):
        """This method will add experience to this character, increasing
        the character's level if the character's total experience is above
        the next threshold."""
        self.experience += new_xp
        ii = 0
        if self.experience >= 300:
            for xp in LEVEL_THRESHOLDS:
                ii += 1
                if self.experience < xp:
                    break

            self.level = ii - 1
            self.proficiency = sum(PROFICIENCY_ARR[:ii - 1])

        if self.experience >= LEVEL_THRESHOLDS[-1]:
            self.level = 20
            self.proficiency = sum(PROFICIENCY_ARR)

    def show_health(self):
        """A simple method for displaying the current and maximum HP for
        this character."""
        output = "===================\n"
        output += "Current HP: {}/{}".format(self.current_hp, self.max_hp)
        output += "\n==================="
        return output

    def take_damage(self, amt):
        """This method adds damage to the character, subtracting the 
        appropriate amount of health. If the character's health reaches
        zero, their health will not go below that amount and they will
        be notified that they have died.

        TODO: Change the print message to a status change."""
        self.current_hp -= amt
        if self.current_hp < 0:
            self.current_hp = 0
            print("You have died.")
        self.show_health()

    def heal_damage(self, amt):
        """This method removes damage from the character, adding the 
        approrpiate amount of health. If the character's health reaches
        their maximum, their health will not increase above that max."""
        self.current_hp += amt
        if self.current_hp > self.max_hp:
            self.current_hp = self.max_hp
            print("You are fully healed.")
        self.show_health()

    def roll_random_stats(self):
        """A method for rolling stats at random. To be used only on 
        character initialization."""
        stats = [sum(sorted(roll_dice(6, 4)[1:])) for jj in range(6)]
        self.strength, self.dexterity, self.constitution, self.intelligence, self.wisdom, self.charisma = stats

    def set_carry_capacity(self):
        """A method for setting this character's carry capacity. This 
        method is to be called either during initialization or upon a change
        in the character's strength."""
        self.carry_capacity = 15 * self.strength
