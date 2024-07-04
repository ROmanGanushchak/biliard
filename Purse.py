class Purse:
    def __init__(self, start_number):
        self.number = start_number

    def get_number(self):
        return self.number

    def increase_number(self, number):
        self.number += number

    def digrease_number(self, number):
        self.number = max(self.number - number, 0)