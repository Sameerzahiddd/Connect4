import json
import os
from copy import deepcopy

# History scores file path
HISTORY_FILE = 'data/history_scores.json'

# Ensure data directory exists
os.makedirs('data', exist_ok=True)

# Load history scores
def load_history_scores():
    """Load history scores from file or create empty dict if file doesn't exist."""
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {}
    return {}

# Save history scores
def save_history_scores(history_scores):
    """Save history scores to file."""
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history_scores, f)

# Global history scores
history_scores = load_history_scores()

def iterative_deepening_minimax(board, max_depth):
    """
    Perform iterative deepening minimax to find the best move.
    
    Args:
        board: Current board state
        max_depth: Maximum depth to search
        
    Returns:
        (value, column): Best move with its evaluation
    """
    global history_scores
    
    best_score = float('-inf')
    best_col = None
    
    # Start with depth 1 and increase
    for depth in range(1, max_depth + 1):
        score, col = minimax(board, depth, float('-inf'), float('inf'), True)
        
        if score > best_score:
            best_score = score
            best_col = col
    
    # Make sure to save the history scores after each search
    save_history_scores(history_scores)
    
    return best_score, best_col

def minimax(board, depth, alpha, beta, maximizing_player):
    """
    Minimax algorithm with alpha-beta pruning.
    
    Args:
        board: Current board state
        depth: Current search depth
        alpha: Alpha value for pruning
        beta: Beta value for pruning
        maximizing_player: True if maximizing (AI), False if minimizing (human)
        
    Returns:
        (value, column): Best move with its evaluation
    """
    global history_scores
    
    from src.ai.evaluation import evaluate_position
    
    # Terminal conditions
    if board.is_winner(2):  # AI wins
        return (1000000, None)
    elif board.is_winner(1):  # Human wins
        return (-1000000, None)
    elif board.is_full() or depth == 0:  # Draw or max depth
        score = evaluate_position(board, 2)  # Evaluate for AI
        return (score, None)
    
    valid_moves = board.get_valid_moves()
    
    # Sort moves by history score for better pruning
    move_scores = []
    for col in valid_moves:
        move_key = str(col)
        score = history_scores.get(move_key, 0)
        move_scores.append((col, score))
    
    # Sort by score (descending)
    move_scores.sort(key=lambda x: x[1], reverse=True)
    
    if maximizing_player:  # AI's turn
        value = float('-inf')
        column = valid_moves[0] if valid_moves else None
        
        for col, _ in move_scores:
            temp_board = deepcopy(board)
            temp_board.drop_piece(col, 2)  # AI player
            
            new_score, _ = minimax(temp_board, depth - 1, alpha, beta, False)
            
            if new_score > value:
                value = new_score
                column = col
            
            alpha = max(alpha, value)
            
            if alpha >= beta:
                # Store successful pruning move
                move_key = str(column)
                history_scores[move_key] = history_scores.get(move_key, 0) + (2 ** depth)
                break
        
        return value, column
    
    else:  # Human's turn
        value = float('inf')
        column = valid_moves[0] if valid_moves else None
        
        for col, _ in move_scores:
            temp_board = deepcopy(board)
            temp_board.drop_piece(col, 1)  # Human player
            
            new_score, _ = minimax(temp_board, depth - 1, alpha, beta, True)
            
            if new_score < value:
                value = new_score
                column = col
            
            beta = min(beta, value)
            
            if alpha >= beta:
                # Store successful pruning move
                move_key = str(column)
                history_scores[move_key] = history_scores.get(move_key, 0) + (2 ** depth)
                break
        
        return value, column

def decay_history_scores():
    """Decay history scores to prevent inflation over time."""
    global history_scores
    
    decay_factor = 0.95
    for key in history_scores:
        history_scores[key] *= decay_factor