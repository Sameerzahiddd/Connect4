import pygame

class GUI:
    """GUI for the Connect Four game."""
    
    # Colors
    BLUE = (0, 0, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    YELLOW = (255, 255, 0)
    WHITE = (255, 255, 255)
    
    # Dimensions
    SQUARE_SIZE = 100
    
    def __init__(self, game):
        """Initialize the GUI."""
        self.game = game
        
        # Calculate dimensions
        self.WIDTH = game.board.cols * self.SQUARE_SIZE
        self.HEIGHT = (game.board.rows + 1) * self.SQUARE_SIZE  # +1 for the top row
        
        # Load fonts
        pygame.font.init()
        self.font = pygame.font.SysFont('Comic Sans MS', 30)
        self.large_font = pygame.font.SysFont('Comic Sans MS', 60)
    
    def draw_board(self, screen):
        """Draw the game board."""
        # Draw blue background
        pygame.draw.rect(
            screen, 
            self.BLUE, 
            (0, self.SQUARE_SIZE, self.WIDTH, self.HEIGHT - self.SQUARE_SIZE)
        )
        
        # Draw empty circles for the grid
        for row in range(self.game.board.rows):
            for col in range(self.game.board.cols):
                # Calculate the center position of each circle
                x = col * self.SQUARE_SIZE + self.SQUARE_SIZE // 2
                y = (row + 1) * self.SQUARE_SIZE + self.SQUARE_SIZE // 2
                
                # Default color is black (empty)
                color = self.BLACK
                
                # Check if a piece exists at this position
                piece = self.game.board.get_cell(row, col)
                if piece == 1:  # Human player
                    color = self.RED
                elif piece == 2:  # AI player
                    color = self.YELLOW
                
                # Draw the circle
                pygame.draw.circle(
                    screen, 
                    color, 
                    (x, y), 
                    self.SQUARE_SIZE // 2 - 5
                )
    
    def draw_piece_preview(self, screen):
        """Draw a preview of where the piece will be placed."""
        if self.game.current_player == self.game.HUMAN_PLAYER and self.game.winner is None:
            # Get mouse position
            mouse_x, _ = pygame.mouse.get_pos()
            col = mouse_x // self.SQUARE_SIZE
            
            # Draw the preview piece at the top
            if 0 <= col < self.game.board.cols and self.game.board.is_valid_move(col):
                x = col * self.SQUARE_SIZE + self.SQUARE_SIZE // 2
                y = self.SQUARE_SIZE // 2
                
                pygame.draw.circle(
                    screen, 
                    self.RED, 
                    (x, y), 
                    self.SQUARE_SIZE // 2 - 5
                )
    
    def draw_winner_message(self, screen):
        """Draw the winner message above the board."""
        if self.game.winner is not None:
            # Background for the message - place it above the board
            pygame.draw.rect(
                screen,
                (200, 200, 200),
                (0, 0, self.WIDTH, self.SQUARE_SIZE),
                border_radius=0
            )
            
            # Winner message
            if self.game.winner == 0:
                text = self.font.render("Game Over: Draw!", True, self.BLACK)
            elif self.game.winner == 1:
                if self.game.battle_mode:
                    text = self.font.render(f"Game Over: {self.game.first_ai.capitalize()} Wins!", True, self.RED)
                else:
                    text = self.font.render("Game Over: You Win!", True, self.RED)
            else:
                if self.game.battle_mode:
                    text = self.font.render(f"Game Over: {self.game.second_ai.capitalize()} Wins!", True, self.YELLOW)
                else:
                    text = self.font.render(f"Game Over: {self.game.ai_type.capitalize()} Wins!", True, self.YELLOW)
            
            # Center the text horizontally, position it higher in the top bar
            text_rect = text.get_rect(
                center=(self.WIDTH // 2, self.SQUARE_SIZE // 3)
            )
            screen.blit(text, text_rect)
            
            # Restart instruction - center below the winner message
            restart_text = self.font.render("Press 'R' to Restart", True, self.BLACK)
            restart_rect = restart_text.get_rect(
                center=(self.WIDTH // 2, self.SQUARE_SIZE * 2 // 3)
            )
            screen.blit(restart_text, restart_rect)
        
    def draw_turn_indicator(self, screen):
        """Draw an indicator of whose turn it is."""
        if self.game.winner is None:
            if self.game.battle_mode:
                # AI vs AI mode
                current_ai = self.game.first_ai if self.game.current_player == 1 else self.game.second_ai
                text = self.font.render(f"{current_ai.capitalize()} AI is thinking...", True, 
                                        self.RED if self.game.current_player == 1 else self.YELLOW)
            elif self.game.current_player == self.game.HUMAN_PLAYER:
                text = self.font.render("Your Turn", True, self.RED)
            else:
                ai_type = self.game.ai_type.capitalize()
                if self.game.ai_thinking:
                    text = self.font.render(f"{ai_type} AI is thinking...", True, self.YELLOW)
                else:
                    text = self.font.render(f"{ai_type} AI's Turn", True, self.YELLOW)
            
            screen.blit(text, (10, 10))
    
    def draw(self, screen):
        """Draw the complete game UI."""
        # Fill background
        screen.fill(self.BLACK)
        
        # Draw the board
        self.draw_board(screen)
        
        # Draw piece preview
        self.draw_piece_preview(screen)
        
        # Draw turn indicator
        self.draw_turn_indicator(screen)
        
        # Draw winner message if game is over
        self.draw_winner_message(screen)