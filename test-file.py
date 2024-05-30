from tile import Tile
import logging
from gamestate import GameState
gamestate = GameState()

manual_tiles = [
    Tile('stick', 1),
    Tile('stick', 2),
    Tile('stick', 3),
    Tile('east'),
    Tile('east'),
    Tile('east'),
    Tile('stick', 8),
    Tile('stick', 8),
    Tile('stick', 8),
    Tile('stick', 9),
    Tile('stick', 9),
    Tile('stick', 9),
    Tile('circle', 4),
    Tile('circle', 3)
]

for tile in manual_tiles:
    gamestate.add_tile_to_hand(tile, 'player1')

gamestate.print_player_hand('player1')