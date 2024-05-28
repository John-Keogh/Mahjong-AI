print('Test file for Mahjong AI.')
print('')
print('This update is to test out creating a new branch.')

players_dict = {
    'player1': [],
    'player2': [],
    'player3': [],
    'player4': []
}

categories_dict = {
    'draw_pool': [1],
    'discard_pool': [2],
    **players_dict
}
print(categories_dict)