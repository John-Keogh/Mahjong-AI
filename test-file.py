from tile import Tile
import logging
from gamestate import GameState
gamestate = GameState()

tile1 = Tile(suit='stick', rank=1)
tile2 = Tile(suit='stick', rank=1)
tile3 = Tile(suit='stick', rank=1)
group = [tile1, tile2, tile3]

print(type(group))
print('')
print(isinstance(group, tuple))