class Desk:
    def __init__(self, width, height, depth):
        self.width = width / 100  # Convert width to meters
        self.height = height / 100  # Convert height to meters
        self.depth = depth / 100  # Convert depth to meters

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def get_depth(self):
        return self.depth

    def get_dimensions(self):
        return self.width, self.height, self.depth

    def set_width(self, width):
        self.width = width / 100  # Convert width to meters
        return self.width

    def set_height(self, height):
        self.height = height / 100  # Convert height to meters
        return self.height

    def set_depth(self, depth):
        self.depth = depth / 100  # Convert depth to meters
        return self.depth

    def set_dimensions(self, width, height, depth):
        self.width = width / 100  # Convert width to meters
        self.height = height / 100  # Convert height to meters
        self.depth = depth / 100  # Convert depth to meters
        return self.width, self.height, self.depth

    def get_volume(self):
        return self.width * self.height * self.depth

    def get_area(self):
        return self.width * self.height