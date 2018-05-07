from collections import namedtuple


ModStat = namedtuple('ModStat', 'stat value')


def modstat_to_list(modstat):
    return [modstat.stat, modstat.value]


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
        self.modset = modset
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
        self.primary = primary
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
        things.extend(modstat_to_list(self.primary))
        for secondary in self.secondaries:
            things.extend(modstat_to_list(secondary))
        return delimeter.join(things)

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
