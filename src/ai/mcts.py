import numpy as np
import copy
import math
import random
import time

class MCTSNode:
    """Node in the Monte Carlo Tree Search."""
    
    def __init__(self, board, parent=None, move=None):
        self.board = board
        self.parent = parent
        self.move = move  # Move that led to this state
        self.children = {}  # Dictionary of {move: MCTSNode}
        self.visits = 0
        self.wins = 0
        self.untried_moves = board.get_valid_moves()
        self.player = 1 if parent and parent.player == 2 else 2  # Player who will make the next move
    
    def uct_select_child(self, exploration_weight=1.0):
        """Select a child node using the UCT formula."""
        # UCT = win_ratio + exploration_weight * sqrt(ln(parent_visits) / child_visits)
        log_visits = math.log(self.visits) if self.visits > 0 else 0
        
        # Find the child with the highest UCT score
        best_score = float('-inf')
        best_child = None
        
        for move, child in self.children.items():
            # Avoid division by zero
            if child.visits == 0:
                continue
                
            # Win ratio from the perspective of the player who made the move
            win_ratio = child.wins / child.visits
            
            # For the opposing player, we want the lowest win ratio
            if self.player != child.player:
                win_ratio = 1 - win_ratio
                
            # UCT formula
            exploration_term = exploration_weight * math.sqrt(log_visits / child.visits)
            uct_score = win_ratio + exploration_term
            
            if uct_score > best_score:
                best_score = uct_score
                best_child = child
        
        return best_child
    
    def add_child(self, move, board):
        """Add a child node for the given move."""
        child = MCTSNode(board, parent=self, move=move)
        self.children[move] = child
        self.untried_moves.remove(move)
        return child
    
    def update(self, result):
        """Update the node statistics with the simulation result."""
        self.visits += 1
        # Win is always tracked from the perspective of player 2 (AI)
        if result == 2:  # AI (player 2) won
            self.wins += 1


def mcts_search(board, iterations=1000, max_time=None):
    """
    Run Monte Carlo Tree Search to find the best move.
    
    Args:
        board: Current board state
        iterations: Maximum number of iterations to run
        max_time: Maximum search time in seconds (optional)
        
    Returns:
        best_move: The best move determined by MCTS
    """
    root = MCTSNode(copy.deepcopy(board))
    
    # Set time limit if specified
    end_time = None
    if max_time:
        end_time = time.time() + max_time
    
    # Run MCTS iterations
    for i in range(iterations):
        # Check time limit
        if end_time and time.time() > end_time:
            break
            
        # 1. Selection and Expansion
        node = _select_and_expand(root)
        
        # 2. Simulation
        simulation_board = copy.deepcopy(node.board)
        result = _simulate(simulation_board, node.player)
        
        # 3. Backpropagation
        _backpropagate(node, result)
    
    # Select the best move based on visit count
    best_move = None
    best_visits = -1
    
    for move, child in root.children.items():
        if child.visits > best_visits:
            best_visits = child.visits
            best_move = move
    
    return best_move


def _select_and_expand(node):
    """Select a node to expand using the UCT formula."""
    # Navigate down the tree until we reach a leaf node
    while node.untried_moves == [] and node.children:
        node = node.uct_select_child()
    
    # If we have untried moves, expand by trying one of them
    if node.untried_moves:
        move = random.choice(node.untried_moves)
        board_copy = copy.deepcopy(node.board)
        board_copy.drop_piece(move, node.player)
        node = node.add_child(move, board_copy)
    
    return node


def _simulate(board, player):
    """Simulate a random game from the current board state."""
    # Switch to the next player
    current_player = 3 - player  # Toggle between 1 and 2
    
    # Play until the game is over
    while True:
        # Check if the game is over
        if board.is_winner(1):
            return 1  # Human wins
        elif board.is_winner(2):
            return 2  # AI wins
        elif board.is_full():
            return 0  # Draw
        
        # Get valid moves
        valid_moves = board.get_valid_moves()
        
        # No valid moves left
        if not valid_moves:
            return 0  # Draw
        
        # Make a random move
        move = random.choice(valid_moves)
        board.drop_piece(move, current_player)
        
        # Switch player
        current_player = 3 - current_player


def _backpropagate(node, result):
    """Update the statistics for all nodes up to the root."""
    while node:
        node.update(result)
        node = node.parent