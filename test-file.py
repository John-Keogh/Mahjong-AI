import random
import torch
import os
import sqlite3
import numpy as np
import time
import random

from evaluation_network import EvaluationNet
from tile_utils import compute_score
from gamestate import GameState

gamestate = GameState()

# print(gamestate.suit_to_idx)
# print(gamestate.idx_to_suit)
# print(gamestate.idx_to_rank)

for k in range(2):
    for i in range(0+k*19,10+k*19):
        print(f"i = {i}")

    for j in range(10+k*19, 19+k*19):
        print(f"j = {j}")
    print('')