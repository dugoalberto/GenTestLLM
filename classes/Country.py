class Country:
    def __init__(self, name, timezone):
        self.name = name
        self.timezone = timezone

    def get_name(self):
        return self.name

    def get_timezone(self):
        return self.timezone

    def set_name(self, name):
        self.name = name
        return self.name

    def set_timezone(self, timezone):
        self.timezone = timezone
        return self.timezone

    def get_country(self):
        return self.name, self.timezone

    def set_country(self, name, timezone):
        self.name = name
        self.timezone = timezone
        return self.name, self.timezone

    def __str__(self):
        return self.name + " " + str(self.timezone)

    def __eq__(self, other):
        return self.name == other.name and self.timezone == other.timezone

    def equals(self, other):
        return self.__eq__(other)

    def semi_equals(self):
        return self.name == "Italy"
