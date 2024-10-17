from tile_utils import is_set, is_run, is_winning_hand, compute_score, Tile, GameState

gamestate = GameState()
player = 'player1'

manual_tiles = [
    Tile('stick', 1),
    Tile('stick', 2),
    Tile('stick', 3),
    Tile('10k', 1),
    Tile('10k', 1),
    Tile('10k', 1),
    Tile('stick', 8),
    Tile('stick', 8),
    Tile('stick', 8),
    Tile('stick', 9),
    Tile('stick', 9),
    Tile('stick', 9),
    Tile('circle', 4),
    Tile('circle', 4)
]

for tile in manual_tiles:
    gamestate.add_tile_to_hand(tile, player)

is_winning, combination = is_winning_hand(gamestate, player)
print(f"is_winning: {is_winning}")
print('')

score = compute_score(gamestate, player)
print(f"score: {score}")