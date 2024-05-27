# Define Tile class to represent game pieces
class Tile:
    def __init__(self, suit, rank=None):
        self.suit = suit
        self.rank = rank

    def display(self):
        if self.rank:
            print(f"{self.rank} {self.suit}")
        else:
            print(f"{self.suit}")