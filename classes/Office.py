class Office:
    def __init__(self, address, area, desks):
        self.address = address
        self.area = area
        self.desks = desks

    def maximum_desks(self):
        total_area = 0
        for desk in self.desks:
            total_area += desk.get_area()
        if total_area == 0:
            return 0
        return int(self.area / total_area)

    def desks_quantity(self):
        return len(self.desks)

    def get_address(self):
        return self.address

    def get_area(self):
        return self.area

    def get_desks(self):
        return self.desks

    def set_address(self, address):
        self.address = address
        return self.address

    def set_area(self, area):
        self.area = area
        return self.area

    def set_desks(self, desks):
        self.desks = desks
        return self.desks
