import pygame
import sys
import time
import copy
from src.models.board import Board
from src.ai.minimax import iterative_deepening_minimax
from src.ai.mcts import mcts_search
from src.gui import GUI

class Game:
    """Connect Four game controller."""
    
    # Constants
    HUMAN_PLAYER = 1
    AI_PLAYER = 2
    AI_THINKING_TIME = 2  # Delay in seconds
    
    def __init__(self, ai_type="minimax", first_ai=None, second_ai=None, first_player=1, difficulty="medium", first_ai_difficulty="medium", second_ai_difficulty="medium"):
        """
        Initialize the game.
        
        Args:
            ai_type: Type of AI to use ('minimax', 'mcts', or 'battle')
            first_ai: Type of first AI for battle mode ('minimax' or 'mcts')
            second_ai: Type of second AI for battle mode ('minimax' or 'mcts')
            first_player: Player who goes first (1 for human, 2 for AI)
            difficulty: Difficulty level ('easy', 'medium', 'hard')
        """
        self.board = Board()
        self.ai_type = ai_type
        self.current_player = first_player
        self.winner = None
        self.ai_thinking = False
        self.ai_start_time = 0
        self.difficulty = difficulty

        
        # For AI vs AI battle
        self.battle_mode = (ai_type == "battle")
        self.first_ai = first_ai
        self.second_ai = second_ai
        self.battle_delay = 1.0  # Delay between moves in battle mode (seconds)
        self.last_move_time = 0
        self.first_ai_difficulty = first_ai_difficulty
        self.second_ai_difficulty = second_ai_difficulty
        
        # Set up the GUI
        self.gui = GUI(self)
        
        # Set up the display
        self.screen = pygame.display.set_mode((self.gui.WIDTH, self.gui.HEIGHT))
        
        # Set the window caption based on game mode
        if self.battle_mode:
            pygame.display.set_caption(f'Connect Four: {self.first_ai.capitalize()} vs {self.second_ai.capitalize()}')
        else:
            pygame.display.set_caption(f'Connect Four: You vs {self.ai_type.capitalize()}')
            
        # If AI starts first, trigger AI thinking immediately
        if self.current_player == self.AI_PLAYER and not self.battle_mode:
            self.ai_thinking = True
            self.ai_start_time = time.time()
    
    def reset(self):
        """Reset the game to the initial state."""
        self.board = Board()
        self.current_player = self.HUMAN_PLAYER
        self.winner = None
        self.ai_thinking = False
    
    def make_move(self, col):
        """
        Make a move for the current player.
        
        Args:
            col: Column to place the piece in
            
        Returns:
            success: True if the move was made, False otherwise
        """
        if self.winner is not None or not self.board.is_valid_move(col):
            return False
        
        success = self.board.drop_piece(col, self.current_player)
        
        if success:
            # Check for win
            if self.board.is_winner(self.current_player):
                self.winner = self.current_player
            # Check for draw
            elif self.board.is_full():
                self.winner = 0  # 0 indicates draw
            else:
                self.switch_player()
        
        return success
    
    def ai_move(self):
        """Have the AI make a move."""
        if self.winner is not None:
            return False
        
        # Determine which AI and difficulty to use
        current_ai = self.ai_type
        current_difficulty = self.difficulty
        
        if self.battle_mode:
            if self.current_player == 1:
                current_ai = self.first_ai
                current_difficulty = self.first_ai_difficulty
            else:
                current_ai = self.second_ai
                current_difficulty = self.second_ai_difficulty
        
        # Get the move from the appropriate AI with appropriate difficulty
        col = None
        if current_ai == "minimax":
            # Set depth based on difficulty
            if current_difficulty == "easy":
                depth = 2
            elif current_difficulty == "medium":
                depth = 3
            else:  # "hard"
                depth = 5
            
            _, col = iterative_deepening_minimax(self.board, depth)
        elif current_ai == "mcts":
            # Set MCTS parameters based on difficulty
            if current_difficulty == "easy":
                iterations = 1000
                max_time = 0.5
            elif current_difficulty == "medium":
                iterations = 5000
                max_time = 2.0
            else:  # "hard"
                iterations = 10000
                max_time = 5.0
            
            col = mcts_search(self.board, iterations=iterations, max_time=max_time)
        
        if col is not None:
            return self.make_move(col)
        
        return False
    
    def switch_player(self):
        """Switch to the other player."""
        self.current_player = 3 - self.current_player  # Toggle between 1 and 2
        
        # If it's now AI's turn (or in battle mode), start the thinking timer
        if self.current_player == self.AI_PLAYER or self.battle_mode:
            self.ai_thinking = True
            self.ai_start_time = time.time()
    
    def handle_events(self):
        """Handle pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Human player's turn (if not in battle mode)
                if not self.battle_mode and self.current_player == self.HUMAN_PLAYER and self.winner is None:
                    col = event.pos[0] // self.gui.SQUARE_SIZE
                    self.make_move(col)
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Reset game
                    self.reset()
                elif event.key == pygame.K_ESCAPE:  # Exit to main menu
                    return False
        
        return True
    
    def run(self):
        """Main game loop."""
        clock = pygame.time.Clock()
        running = True
        
        while running:
            clock.tick(60)  # 60 FPS
            
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Human player's turn (if not in battle mode)
                    if not self.battle_mode and self.current_player == self.HUMAN_PLAYER and self.winner is None:
                        col = event.pos[0] // self.gui.SQUARE_SIZE
                        self.make_move(col)
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        if self.winner is not None:
                            # Game is over, return to menu
                            return True  # This will return to the main menu
                        else:
                            # Mid-game reset, just restart
                            self.reset()
                    elif event.key == pygame.K_ESCAPE:  # Exit to main menu
                        return True
            
            # AI's turn with delay
            current_time = time.time()
            
            if self.winner is None:
                if self.battle_mode:
                    # AI vs AI mode - add delay between moves
                    if current_time - self.last_move_time >= self.battle_delay:
                        self.ai_thinking = False
                        self.ai_move()
                        self.last_move_time = current_time
                elif self.current_player == self.AI_PLAYER:
                    # Human vs AI mode
                    if self.ai_thinking:
                        if current_time - self.ai_start_time >= self.AI_THINKING_TIME:
                            self.ai_thinking = False
                            self.ai_move()
            
            # Draw the game
            self.gui.draw(self.screen)
            
            # Update the display
            pygame.display.flip()
        
        return False  # This means exit the application