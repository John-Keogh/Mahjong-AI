import numpy as np
import torch

def get_last_game_id(conn):
    """
    Retrieve the last game_id from the database
    
    Args:
        conn (sqlite3.Connection): SQLite connection object
    
    Returns:
        int: Last game_id if exists, otherwise 0
    """
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(game_id) FROM winner_history")
    last_game_id = cursor.fetchone()[0]
    return last_game_id if last_game_id is not None else 0  # Start from 0 if no data is present


def load_and_inspect_winner_data(conn, game_id):
    cursor = conn.cursor()
    cursor.execute('SELECT player, turn, gamestate_tensor, final_score FROM winner_history WHERE game_id = ?', (game_id,))
    rows = cursor.fetchall()

    # Convert and display each row's data
    for row in rows:
        player, turn, tensor_blob, final_score = row
        # Convert the BLOB back to a PyTorch tensor
        gamestate_tensor = torch.from_numpy(np.frombuffer(tensor_blob, dtype=np.float32))

        print(f"Game ID: {game_id}")
        print(f"Player: {player}")
        print(f"Turn: {turn}")
        print(f"Final Score: {final_score}")
        print(f"Gamestate Tensor: {gamestate_tensor}\n")  # This will show the tensor for each turn


def load_winner_history(conn, game_id):
    """
    Load winner history for a specific game
    
    Args:
        conn (sqlite3.Connection): SQLite connection object
        game_id (int): Unique identifier for each game
    
    Returns:
        list: List of (player, turn, gamestate_tensor) tuples
    """
    cursor = conn.cursor()
    cursor.execute('SELECT game_id, player, turn, gamestate_tensor, final_score FROM winner_history WHERE game_id = ?', (game_id,))
    rows = cursor.fetchall()

    winner_history = []
    for row in rows:
        game_id, player, turn, tensor_blob, final_score = row
        # Convert the BLOB back to a PyTorch tensor
        gamestate_tensor = torch.from_numpy(np.frombuffer(tensor_blob, dtype=np.float32).copy())
        winner_history.append((game_id, player, turn, gamestate_tensor, final_score))

    return winner_history

def save_winner_data(conn, game_id, winner_history, player, score):
    """
    Save winning player history and score to the database
    
    Args:
        conn (sqlite3.Connection): SQLite connection object
        game_id (int): Unique identifier for each game
        winner_history (torch.Tensor): Tensor of winner's gamestate history
        player (str): Player identifier (e.g., 'player1')
        score (int): Final winning score
    """
    cursor = conn.cursor()
    for turn, gamestate_tensor in enumerate(winner_history):
        gamestate_blob = gamestate_tensor.numpy().tobytes()  # Convert tensor to bytes for SQLite storage
        cursor.execute("INSERT INTO winner_history (game_id, player, turn, gamestate_tensor, final_score) VALUES (?, ?, ?, ?, ?)",
                       (game_id, player, turn, gamestate_blob, score))
    conn.commit()

def load_training_data(conn, decay=0.95):
    """
    Load training data from the database and apply a decaying score factor to earlier turns.
    
    Args:
    conn (sqlite3.Connection): SQLite database connection
    decay (float): Decay factor to apply to earlier turns' scores

    Returns:
    tuple: (data, targets) where data is a tensor of game states and targets are their corresponding scores.
    """
    cursor = conn.cursor()
    cursor.execute('SELECT game_id, turn, gamestate_tensor, final_score FROM winner_history ORDER BY game_id, turn')
    rows = cursor.fetchall()

    data = []
    targets = []
    current_game_id = None
    turn_count = 0

    for row in rows:
        game_id, turn, tensor_blob, final_score = row

        # Reset turn count for each new game
        if game_id != current_game_id:
            current_game_id = game_id
            turn_count = cursor.execute('SELECT COUNT(*) FROM winner_history WHERE game_id = ?', (game_id,)).fetchone()[0]

        # Apply decay based on how far the turn is from the final turn
        adjusted_score = final_score * (decay ** (turn_count - turn - 1))

        # Convert the tensor BLOB back to a PyTorch tensor
        gamestate_tensor = torch.from_numpy(np.frombuffer(tensor_blob, dtype=np.float32).copy())
        data.append(gamestate_tensor)
        targets.append(adjusted_score)

    # Stack all the tensors for efficient batch processing
    data = torch.stack(data)
    targets = torch.tensor(targets, dtype=torch.float32)
    
    return data, targets