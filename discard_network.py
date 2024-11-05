import torch
import torch.nn as nn

class DiscardNet(nn.Module):
    def __init__(self):
        super(DiscardNet, self).__init__()
        self.fc1 = nn.Linear(1832, 1024)
        self.fc2 = nn.Linear(1024, 512)
        self.fc3 = nn.Linear(512, 128)
        self.fc4 = nn.Linear(128, 14)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = torch.relu(self.fc3(x))
        x = self.fc4(x)
        return x
    

def calculate_reward(gamestate, player, discard_tile, previous_value, new_value):
    '''
    Calculates the reward for discarding discard_tile from player's hand

    Args:
    gamestate: state of the game
    player: 'player1', 'player2', etc.
    discard_tile: object of Tile class to be discarded
    previous_value: value of player's hand prior to discarding
    new_value: value of player's hand after discarding

    Returns:
    reward: reward value
    '''
    reward = 0

    # it's here that I realized that I want a way to evaluate a player's hand given the gamestate
    # once the evaluation network is finished, come back and plug it in here to calculate the reward
    # ^11-02-24

    return reward