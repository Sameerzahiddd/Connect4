import pygame
import sys
import time  # Add this import for the delay
from src.models.board import Board
from src.ai.minimax import iterative_deepening_minimax, decay_history_scores
from src.gui import GUI

class Game:
    """Connect Four game controller."""
    
    # Constants
    HUMAN_PLAYER = 1
    AI_PLAYER = 2
    AI_THINKING_TIME = 2  # Add this constant for the delay (in seconds)
    
    def __init__(self):
        """Initialize the game."""
        self.board = Board()
        self.current_player = self.HUMAN_PLAYER
        self.winner = None
        self.gui = GUI(self)
        self.ai_thinking = False  # Add this flag to track AI thinking state
        self.ai_start_time = 0    # Add this to track when AI started thinking
        
        # Set up the display
        self.screen = pygame.display.set_mode((self.gui.WIDTH, self.gui.HEIGHT))
        pygame.display.set_caption('Connect Four AI')
    
    def reset(self):
        """Reset the game to the initial state."""
        self.board = Board()
        self.current_player = self.HUMAN_PLAYER
        self.winner = None
        self.ai_thinking = False
        decay_history_scores()  # Decay history scores between games
    
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
        if self.current_player != self.AI_PLAYER or self.winner is not None:
            return False
        
        # Use minimax to find the best move
        _, col = iterative_deepening_minimax(self.board, 5)  # Depth 5 is usually good
        
        if col is not None:
            return self.make_move(col)
        
        return False
    
    def switch_player(self):
        """Switch to the other player."""
        self.current_player = self.AI_PLAYER if self.current_player == self.HUMAN_PLAYER else self.HUMAN_PLAYER
        
        # If it's now AI's turn, start the thinking timer
        if self.current_player == self.AI_PLAYER:
            self.ai_thinking = True
            self.ai_start_time = time.time()
    
    def handle_events(self):
        """Handle pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Human player's turn
                if self.current_player == self.HUMAN_PLAYER and self.winner is None:
                    col = event.pos[0] // self.gui.SQUARE_SIZE
                    self.make_move(col)
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Reset game
                    self.reset()
        
        return True
    
    def run(self):
        """Main game loop."""
        clock = pygame.time.Clock()
        running = True
        
        while running:
            clock.tick(60)  # 60 FPS
            
            # Handle events
            running = self.handle_events()
            
            # AI's turn with delay
            if self.current_player == self.AI_PLAYER and self.winner is None:
                current_time = time.time()
                
                if self.ai_thinking:
                    # Check if AI has "thought" long enough
                    if current_time - self.ai_start_time >= self.AI_THINKING_TIME:
                        self.ai_thinking = False
                        self.ai_move()
                
            # Draw the game
            self.gui.draw(self.screen)
            
            # Update the display
            pygame.display.flip()