# Define Tile class to represent game pieces
class Tile:
    # Iniitialization
    def __init__(self, suit, rank=None):
        self.suit = suit
        self.rank = rank
    
    # Customize representation for print statements to aid in debugging
    def __repr__(self):
        if self.rank:
            return f"{self.rank} {self.suit}"
        else:
            return f"{self.suit}"

    # Allow comparison of two Tile objects 
    def __eq__(self, other):
            if isinstance(other, Tile):
                if self.rank:
                    return self.suit == other.suit and self.rank == other.rank
                else:
                    return self.suit == other.suit
            return False

    # Allow tiles to be displayed via "tile.display()"
    def display(self):
        if self.rank:
            print(f"{self.rank} {self.suit}")
        else:
            print(f"{self.suit}")