class KPD(object):
    def __init__(self, frags, deaths):
        self.frags = frags
        self.deaths = deaths

        if self.deaths > 0:
            self.value = float(self.frags) / float(self.deaths)
        else:
            self.value = Ellipsis

    def __str__(self):
        if self.deaths > 0:
            return "{0:.1f}".format(self.value)
        else:
            return "inf[{}]".format(self.frags)

    def __cmp__(self, other):
        c = cmp(self.value, other.value)

        if c != 0 or self.value is not Ellipsis:
            return c
        else:
            return cmp(self.frags, other.frags)
