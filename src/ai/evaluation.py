def evaluate_position(board, player):
    """
    Evaluate the current board position for the given player.
    
    Args:
        board: The board to evaluate
        player: The player (1 for human, 2 for AI)
        
    Returns:
        score: A numerical score representing how good the position is for the player
    """
    score = 0
    opponent = 1 if player == 2 else 2
    
    # Score center column (controlling center is advantageous)
    center_column = [board.get_cell(r, board.cols // 2) for r in range(board.rows)]
    center_count = center_column.count(player)
    score += center_count * 3
    
    # Check horizontal, vertical, and diagonal patterns
    # Horizontal
    for r in range(board.rows):
        for c in range(board.cols - 3):
            window = [board.get_cell(r, c + i) for i in range(4)]
            score += _evaluate_window(window, player, opponent)
    
    # Vertical
    for c in range(board.cols):
        for r in range(board.rows - 3):
            window = [board.get_cell(r + i, c) for i in range(4)]
            score += _evaluate_window(window, player, opponent)
    
    # Positive diagonal (/)
    for r in range(board.rows - 3):
        for c in range(board.cols - 3):
            window = [board.get_cell(r + i, c + i) for i in range(4)]
            score += _evaluate_window(window, player, opponent)
    
    # Negative diagonal (\)
    for r in range(3, board.rows):
        for c in range(board.cols - 3):
            window = [board.get_cell(r - i, c + i) for i in range(4)]
            score += _evaluate_window(window, player, opponent)
    
    return score

def _evaluate_window(window, player, opponent):
    """
    Evaluate a window of 4 positions.
    
    Args:
        window: List of 4 positions to evaluate
        player: The player (1 or 2)
        opponent: The opponent (1 or 2)
        
    Returns:
        score: Points for this window
    """
    # Empty cells
    empty = 0
    
    # Count pieces
    player_count = window.count(player)
    opponent_count = window.count(opponent)
    empty_count = window.count(empty)
    
    # Scoring logic
    if player_count == 4:  # Winning position
        return 100
    elif player_count == 3 and empty_count == 1:  # Strong threat
        return 5
    elif player_count == 2 and empty_count == 2:  # Developing position
        return 2
    
    # Defensive scoring - block opponent threats
    if opponent_count == 3 and empty_count == 1:
        return -4  # Block immediate threat
    
    return 0  # Neutral position