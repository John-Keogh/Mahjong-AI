import unittest
from preprocessing import encode_tile, encode_tile_batch, Tile, GameState, np, torch, encode_macro_direction, encode_micro_direction

class TestIsSetFunction(unittest.TestCase):
    def test_encode_tile_with_rank(self):
        '''
        Test that a tile with a suit and rank is properly one-hot encoded using the encoded_tile function
        '''
        gamestate = GameState()
        tile = Tile('stick', 1)

        encoded_tile = encode_tile(gamestate, tile)
        correct_encoding = np.zeros(19) # 10 suits + 9 ranks
        correct_encoding[0] = 1 # encode suit: stick
        correct_encoding[9] = 1 # encode rank: 1

        result = (encoded_tile.all() == correct_encoding.all())
        self.assertTrue(result)


    def test_encode_tile_without_rank(self):
        '''
        Test that a tile with a suit but no rank is properly one-hot encoded using the encoded_tile function
        '''
        gamestate = GameState()
        tile = Tile('green')

        encoded_tile = encode_tile(gamestate, tile)
        correct_encoding = np.zeros(19) # 10 suits + 9 ranks
        correct_encoding[4] = 1 # encode suit: green

        result = (encoded_tile.all() == correct_encoding.all())
        self.assertTrue(result)


    def test_encode_tile_batch_player_hand(self):
        '''
        Test that a batch of tiles in a player's hand is properly encoded using encode_tile_batch function
        '''
        gamestate = GameState()
        player = 'player1'

        # Simulate a player's hand using only 3 tiles for simplicity
        manual_tiles = [
            Tile('stick', 1),
            Tile('stick', 2),
            Tile('stick', 3)
        ]

        for tile in manual_tiles:
            gamestate.add_tile_to_hand(tile, player)

        # Simulate pulling tiles from a player's hand
        tile_list = []
        for tile in gamestate.players[player]:
            tile_list.append(tile)
        
        # Run encode_tile_batch function using the list of tiles extracted from player's hand
        tile_encodings_tensor = encode_tile_batch(gamestate, tile_list)

        # Manually encode the expected encoding tensor
        encoded_tile1 = np.array([1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0])
        encoded_tile2 = np.array([1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0])
        encoded_tile3 = np.array([1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0])
        correct_encoding = np.hstack((encoded_tile1, encoded_tile2, encoded_tile3))
        correct_encoding_tensor = torch.from_numpy(correct_encoding).float()

        result = (tile_encodings_tensor.all() == correct_encoding_tensor.all())
        self.assertTrue(result)


    def test_encode_tile_batch_player_hand_1(self):
        '''
        Test that a batch of tiles in a player's hand is properly encoded using encode_tile_batch function
        '''
        gamestate = GameState()
        player = 'player1'

        # Simulate a player's hand using only 3 tiles for simplicity
        manual_tiles = [
            Tile('stick', 1),
            Tile('white'),
            Tile('north')
        ]

        for tile in manual_tiles:
            gamestate.add_tile_to_hand(tile, player)

        # Simulate pulling tiles from a player's hand
        tile_list = []
        for tile in gamestate.players[player]:
            tile_list.append(tile)
        
        # Run encode_tile_batch function using the list of tiles extracted from player's hand
        tile_encodings_tensor = encode_tile_batch(gamestate, tile_list)

        # Manually encode the expected encoding tensor
        encoded_tile1 = np.array([1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0])
        encoded_tile2 = np.array([0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        encoded_tile3 = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        correct_encoding = np.hstack((encoded_tile1, encoded_tile2, encoded_tile3))
        correct_encoding_tensor = torch.from_numpy(correct_encoding).float()

        result = (tile_encodings_tensor.all() == correct_encoding_tensor.all())
        self.assertTrue(result)


    def test_encode_tile_batch_player_hand_1(self):
        '''
        Test that a batch of tiles in a player's hand is properly encoded using encode_tile_batch function
        '''
        gamestate = GameState()
        player = 'player1'

        # Simulate a player's hand using only 3 tiles for simplicity
        manual_tiles = [
            Tile('stick', 1),
            Tile('white'),
            Tile('north')
        ]

        for tile in manual_tiles:
            gamestate.add_tile_to_hand(tile, player)

        # Simulate pulling tiles from a player's hand
        tile_list = []
        for tile in gamestate.players[player]:
            tile_list.append(tile)
        
        # Run encode_tile_batch function using the list of tiles extracted from player's hand
        tile_encodings_tensor = encode_tile_batch(gamestate, tile_list)

        # Manually encode the expected encoding tensor
        encoded_tile1 = np.array([1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0])
        encoded_tile2 = np.array([0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        encoded_tile3 = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        correct_encoding = np.hstack((encoded_tile1, encoded_tile2, encoded_tile3))
        correct_encoding_tensor = torch.from_numpy(correct_encoding).float()

        result = (tile_encodings_tensor.all() == correct_encoding_tensor.all())
        self.assertTrue(result)


    def test_encode_macro_direction(self):
        '''
        Test that the macro direction of the game is properly encoded using encode_macro_direction function

        Uses the default first direction: east
        '''
        gamestate = GameState()

        encoded_macro_direction = encode_macro_direction(gamestate)

        correct_encoding = torch.zeros(4)
        correct_encoding[0] = 1

        result = (encoded_macro_direction.all() == correct_encoding.all())
        self.assertTrue(result)


    def test_encode_micro_direction(self):
        '''
        Test that the micro direction of the game is properly encoded using encode_micro_direction function

        Uses the default first direction: east
        '''
        gamestate = GameState()

        encoded_micro_direction = encode_micro_direction(gamestate)

        correct_encoding = torch.zeros(4)
        correct_encoding[0] = 1

        result = (encoded_micro_direction.all() == correct_encoding.all())
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
