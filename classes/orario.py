from classes.Paese import Paese
class Myclock:
    def __init__(self, hour, minutes):
        self.hour = hour
        self.minutes = minutes
    def get_hour(self):
        return self.hour
    def get_minutes(self):
        return self.minutes
    def set_hour(self, hour):
        self.hour = hour
        return self.hour
    def set_minutes(self, minutes):
        self.minutes = minutes
        return self.minutes
    def get_clock(self):
        return self.hour, self.minutes
    def set_clock(self, hour, minutes):
        self.hour = hour
        self.minutes = minutes
        return self.hour, self.minutes
    def fuso(self, country: Paese):
        return self.hour + country.get_fuso()
