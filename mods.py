from collections import namedtuple


ModStat = namedtuple('ModStat', 'stat value')
AllowedModsets = ['speed', 'crit chance', 'crit damage', 'tenacity', 'offense', 'defense', 'health',
                  'potency']
AllowedPrimaries = ['speed', 'critical chance', 'critical damage', 'potency', 'tenacity', 'accuracy',
    'critical avoidance', 'offense', 'defense', 'health', 'protection']
AllowedSecondaries = ['speed', 'critical chance', 'potency', 'tenacity', 'offense', 'defense', 'health',
    'protection']


def modstat_to_str_list(modstat):
    return [modstat.stat, str(modstat.value)]


class CharReqs(object):
    def __init__(self, name, modsets, primaries, secondaries, minpips, minlevel):
        self.name = name
        for modset in modsets:
            if modset.lower().strip().rstrip('%') not in AllowedModsets:
                raise ValueError("Requested optimisation of modset {} not recognised - choose from {}".format(
                      modset, AllowedModsets))
        self.modsets = modsets
        for primary in primaries:
            if primary.lower().strip().rstrip('%') not in AllowedPrimaries:
                raise ValueError("Requested optimisation of primary {} not recognised - choose from {}".format(
                      primary, AllowedPrimaries))
        self.primaries = primaries
        for secondary in secondaries:
            if secondary.lower().strip().rstrip('%') not in AllowedSecondaries:
                raise ValueError("Requested optimisation of secondary {} not recognised - choose from {}".format(
                      secondary, AllowedSecondaries))
        self.secondaries = secondaries
        self.minpips = int(minpips)
        self.minlevel = int(minlevel)


class Mod(object):
    def __init__(self, current_toon, pips, level, modset, modshape, primary, secondaries):
        """
        Args
            current_toon (str)
            new_toon (str)
            pips (int)
            level (int)
            modset (str) - health, potency, etc
            modshape (str) - arrow, square etc.
            primary (modstat)
            secondaries (list of modstats)
        """
        self.current_toon = current_toon
        self.new_toon = None
        self.pips = pips
        self.level = level
        if modset.lower().strip().rstrip('%') not in AllowedModsets:
            raise ValueError("Tried to load mod with modset {} not recognised - choose from {}".format(
                  modset, AllowedModsets))
        self.modset = modset
        self.modshape = modshape
        if modshape.lower() == "transmitter":
            self.modshape = "square"
        if modshape.lower() == "processor":
            self.modshape = "diamond"
        if modshape.lower() == "data-bus":
            self.modshape = "circle"
        if modshape.lower() == "receiver":
            self.modshape = "arrow"
        if modshape.lower() == "holo-array":
            self.modshape = "triangle"
        if modshape.lower() == "multiplexer":
            self.modshape = "cross"
        if primary.stat.lower().strip().rstrip('%') not in AllowedPrimaries:
            raise ValueError("Tried to load mod with primary {} not recognised - choose from {}".format(
                  primary, AllowedPrimaries))
        self.primary = primary
        for secondary in secondaries:
            if secondary.stat.lower().strip().rstrip('%') not in AllowedSecondaries:
                raise ValueError("Trying to load mod with secondary {} not recognised - choose from {}".format(
                      secondary, AllowedSecondaries))
        self.secondaries = secondaries

    @staticmethod
    def header_xsv(delimeter=","):
        return delimeter.join(["current toon", "new toon", "number of dots", "level", "set",
                        "shape", "primary stat type", "primary stat value", "secondary stat type",
                        "secondary stat value", "secondary stat type", "secondary stat value",
                        "secondary stat type", "secondary stat value", "secondary stat type",
                        "secondary stat value"]) 

    def to_xsv(self, delimeter=","):
        new_toon = self.new_toon
        if not new_toon:
            new_toon = "TBD"
        things = [self.current_toon, new_toon, str(self.pips), str(self.level), self.modset,
                  self.modshape]
        things.extend(modstat_to_str_list(self.primary))
        for secondary in self.secondaries:
            things.extend(modstat_to_str_list(secondary))
        return delimeter.join(things)

    def rating(self, character):
        rating = 0
        for idx, target_primary in enumerate(character.primaries):
            if idx == 0:
                weight = 17
            elif idx == 1:
                weight = 7.5
            elif idx == 2:
                weight = 3
            if self.primary.stat.rstrip('%').lower() == target_primary.rstrip('%').lower():
                rating += weight * int(self.pips)   
        for idx, target_secondary in enumerate(character.secondaries):
            if idx == 0:
                weight = 100
            elif idx == 1:
                weight = 50
            elif idx == 2:
                weight = 20
            for mod_secondary in self.secondaries:
                if target_secondary.lower().rstrip('%') == mod_secondary.stat.lower().rstrip('%'):
                    rating += Mod.rating_for_stat(mod_secondary.stat, mod_secondary.value, weight)
        return rating

    @staticmethod
    def rating_for_stat(stat, value, weight):
        # Best possible secondary values from here:
        # https://forums.galaxy-of-heroes.starwars.ea.com/discussion/69479/what-are-the-max-secondary-stats-on-5-dot-mods
        if stat.lower() == 'speed':
            return weight * value / 30
        if stat.lower() == 'offense':
            return weight * value / 225
        if stat.lower() == 'offense%':
            return weight * value / 2.6
        if stat.lower() == 'defense':
            return weight * value / 45
        if stat.lower() == 'defense%':
            return weight * value / 7.8
        if stat.lower() == 'health':
            return weight * value / 2000
        if stat.lower() == 'health%':
            return weight * value / 5.6
        if stat.lower() == 'protection':
            return weight * value / 4000
        if stat.lower() == 'protection%':
            return weight * value / 10
        if stat.lower() == 'critical chance':
            return weight * value / 10
        if stat.lower() == 'potency':
            return weight * value / 10
        if stat.lower().rstrip('%') == 'tenacity':
            return weight * value / 225
        print("Got a weird one here for {} value {}".format(stat, value))


class Mods(object):
    def __init__(self):
        self.mods = []

    def add_mod(self, mod):
        self.mods.append(mod)

    def write_mods_to_file(self, file_path, delimeter):
        with open(file_path, 'w') as ouf:
            ouf.write(Mod.header_xsv(delimeter) + "\n")
            for mod in self.mods:
                ouf.write(mod.to_xsv(delimeter) + "\n")

    def load_mods_from_file(self, file_path, delimeter):
        with open(file_path) as inf:
            header = inf.readline()
            for line in inf:
                entries = line.strip().split(delimeter)
                current_toon = entries[0]
                new_toon = entries[1]
                pips = entries[2]
                level = entries[3]
                modset = entries[4]
                modshape = entries[5]
                primary = ModStat(entries[6], float(entries[7]))
                secondaries = []
                for i in range(8, len(entries), 2):
                    secondary = ModStat(entries[i], float(entries[i+1]))
                    secondaries.append(secondary)
                self.mods.append(Mod(current_toon, pips, level, modset, modshape, primary,
                                     secondaries))

    def filter_mods(self, pips=None, level=None, modsets=[], modshape=None):
        mods = [mod for mod in self.mods if not mod.new_toon]
        if pips:
            new_mods = [mod for mod in mods if int(mod.pips) >= pips]
            if new_mods:
                mods = new_mods
        if level:
            new_mods = [mod for mod in mods if int(mod.level) >= level]
            if new_mods:
                mods = new_mods
        if modsets:
            new_mods = [mod for mod in mods if mod.modset.strip('%').lower() in modsets]
            if new_mods:
                mods = new_mods
        if modshape:
            new_mods = [mod for mod in mods if mod.modshape.lower() == modshape.lower()]
            if new_mods:
                mods = new_mods
        return mods

    def assign_mods(self, character):
        """
        Sets new_toon for the character's optimised mods
        """
        arrow_mods = self.find_best_rating_mods(character, 'arrow')
        square_mods = self.find_best_rating_mods(character, 'square')
        diamond_mods = self.find_best_rating_mods(character, 'diamond')
        circle_mods = self.find_best_rating_mods(character, 'circle')
        triangle_mods = self.find_best_rating_mods(character, 'triangle')
        cross_mods = self.find_best_rating_mods(character, 'cross')
        mods = self.pick_optimal_combination(character, arrow_mods, square_mods, diamond_mods,
                                 circle_mods, triangle_mods, cross_mods) 
        print("New mods for {}".format(character.name))
        for mod in mods:
            print(mod.to_xsv())
        self.update_new_toon(mods, character)

    def pick_optimal_combination(self, character, arrow_mods, square_mods, diamond_mods,
                                 circle_mods, triangle_mods, cross_mods):
        # do an exhaustive search
        # give 1000000 rating points per match in the desired set
        # then sum the individual ratings
        target_modsets = []
        for modset in character.modsets:
            target_modsets.append(modset)
            target_modsets.append(modset)
        best_set = []
        best_rating = 0
        for arrow in arrow_mods:
            for square in square_mods:
                for diamond in diamond_mods:
                    for circle in circle_mods:
                        for triangle in triangle_mods:
                            for cross in cross_mods:
                                # start by checking for mod overlap
                                actual_modsets = [arrow.modset, square.modset, diamond.modset,
                                    circle.modset, triangle.modset, cross.modset]
                                overlap = self.find_modset_overlap(target_modsets, actual_modsets)
                                rating = 1000000 * overlap
                                # sum individual mod ratings
                                rating += arrow.rating(character) + square.rating(character) + \
                                    diamond.rating(character) + circle.rating(character) + \
                                    triangle.rating(character) + cross.rating(character)
                                if rating > best_rating:
                                    best_rating = rating
                                    best_set = [arrow, square, diamond, circle, triangle, cross]
        return best_set
                                
    def find_modset_overlap(self, target, actual):
        hit = {}
        for moda in actual:
            for modt in range(0,len(target)):
                if moda.lower() == target[modt].lower() and modt not in hit:
                    hit[modt] = True
                    break
        return len(hit)

    def update_new_toon(self, mods, character):
        for mod in mods:
            for rmod in self.mods:
                if mod.current_toon == rmod.current_toon and mod.modshape == rmod.modshape:
                    rmod.new_toon = character.name

    def find_best_rating_mods(self, character, modshape):
        mods = []
        for modset in set(character.modsets):
            possible_mods = self.filter_mods(pips=character.minpips, level=character.minlevel,
                modsets=[modset], modshape=modshape)
            if possible_mods:
                best = sorted(possible_mods, key=lambda obj: obj.rating(character))[-1]
                mods.append(best)
        return mods
