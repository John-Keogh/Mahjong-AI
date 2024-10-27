from preprocessing import prepare_input
from tile import Tile
from gamestate import GameState

gamestate = GameState()
player = 'player1'

gamestate.initialize_draw_pool()
gamestate.deal_tiles()

input_tensor = prepare_input(gamestate, player)
print(input_tensor)
print(len(input_tensor))