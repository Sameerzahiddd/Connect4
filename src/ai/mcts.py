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
        # Important: Set player correctly based on the board state or parent
        self.player = board.current_player if hasattr(board, 'current_player') else (1 if parent and parent.player == 2 else 2)
    
    def uct_select_child(self, exploration_weight=1.41):  # sqrt(2) is a common value
        """Select a child node using the UCT formula."""
        # UCT = win_ratio + exploration_weight * sqrt(ln(parent_visits) / child_visits)
        log_visits = math.log(self.visits) if self.visits > 0 else 0
        
        # Find the child with the highest UCT score
        best_score = float('-inf')
        best_child = None
        
        for move, child in self.children.items():
            # Avoid division by zero
            if child.visits == 0:
                return child
                
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
        
        # Update wins based on the player's perspective
        if result == self.player:
            self.wins += 1
        elif result == 0:  # Draw
            self.wins += 0.5  # Count draws as half-wins


def mcts_search(board, iterations=1000, max_time=2.0):
    """
    Run Monte Carlo Tree Search to find the best move.
    
    Args:
        board: Current board state
        iterations: Maximum number of iterations to run
        max_time: Maximum search time in seconds
        
    Returns:
        best_move: The best move determined by MCTS
    """
    # Create a deep copy to avoid modifying the original board
    root = MCTSNode(copy.deepcopy(board))
    
    # Store whose turn it is at the root (important for simulation)
    root_player = root.player
    
    # Set time limit
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
    
    # Debug information
    total_simulations = sum(child.visits for child in root.children.values())
    print(f"MCTS completed {total_simulations} simulations across {len(root.children)} moves")
    
    # Select the best move based on most visits (more robust than win ratio)
    best_move = None
    best_visits = -1
    
    for move, child in root.children.items():
        print(f"Move {move}: {child.wins}/{child.visits} = {child.wins/child.visits if child.visits > 0 else 0:.3f}")
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
    # Start with the next player (opponent of the player who just moved)
    current_player = 3 - player  # Toggle between 1 and 2
    
    # Play until the game is over
    while True:
        # Check if the game is over
        if board.is_winner(1):
            return 1  # Human/Player 1 wins
        elif board.is_winner(2):
            return 2  # AI/Player 2 wins
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