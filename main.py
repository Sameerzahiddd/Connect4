import pygame
import sys
from src.game import Game
from src.ai.minimax import iterative_deepening_minimax
from src.ai.mcts import mcts_search

def display_menu(screen):
    """Display the game mode selection menu."""
    # Colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    YELLOW = (255, 255, 0)
    BLUE = (0, 0, 255)
    
    # Set up fonts
    pygame.font.init()
    title_font = pygame.font.SysFont('Arial', 48)
    option_font = pygame.font.SysFont('Arial', 36)
    
    # Title text
    title = title_font.render('Connect Four AI', True, BLUE)
    title_rect = title.get_rect(center=(screen.get_width() // 2, 80))
    
    # Option texts
    option1 = option_font.render('1. Play against Alpha-Beta Minimax AI', True, BLACK)
    option1_rect = option1.get_rect(center=(screen.get_width() // 2, 200))
    
    option2 = option_font.render('2. Play against Monte Carlo Tree Search AI', True, BLACK)
    option2_rect = option2.get_rect(center=(screen.get_width() // 2, 250))
    
    option3 = option_font.render('3. Watch AI vs AI Battle', True, BLACK)
    option3_rect = option3.get_rect(center=(screen.get_width() // 2, 300))
    
    # Draw everything
    screen.fill(WHITE)
    screen.blit(title, title_rect)
    screen.blit(option1, option1_rect)
    screen.blit(option2, option2_rect)
    screen.blit(option3, option3_rect)
    
    pygame.display.flip()
    
    # Wait for user selection
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return 1  # Minimax AI
                elif event.key == pygame.K_2:
                    return 2  # MCTS AI
                elif event.key == pygame.K_3:
                    return 3  # AI vs AI
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

def choose_first_player(screen):
    """Display menu to choose who goes first."""
    # Colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    BLUE = (0, 0, 255)
    
    # Set up fonts
    pygame.font.init()
    title_font = pygame.font.SysFont('Arial', 48)
    option_font = pygame.font.SysFont('Arial', 36)
    
    # Title text
    title = title_font.render('Who goes first?', True, BLUE)
    title_rect = title.get_rect(center=(screen.get_width() // 2, 80))
    
    # Option texts
    option1 = option_font.render('1. You go first', True, BLACK)
    option1_rect = option1.get_rect(center=(screen.get_width() // 2, 200))
    
    option2 = option_font.render('2. AI goes first', True, BLACK)
    option2_rect = option2.get_rect(center=(screen.get_width() // 2, 250))
    
    # Draw everything
    screen.fill(WHITE)
    screen.blit(title, title_rect)
    screen.blit(option1, option1_rect)
    screen.blit(option2, option2_rect)
    
    pygame.display.flip()
    
    # Wait for user selection
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return 1  # Human goes first
                elif event.key == pygame.K_2:
                    return 2  # AI goes first
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

def choose_first_ai(screen):
    """Display menu to choose which AI goes first in battle mode."""
    # Colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    BLUE = (0, 0, 255)
    
    # Set up fonts
    pygame.font.init()
    title_font = pygame.font.SysFont('Arial', 48)
    option_font = pygame.font.SysFont('Arial', 36)
    
    # Title text
    title = title_font.render('Which AI goes first?', True, BLUE)
    title_rect = title.get_rect(center=(screen.get_width() // 2, 80))
    
    # Option texts
    option1 = option_font.render('1. Minimax (Red)', True, BLACK)
    option1_rect = option1.get_rect(center=(screen.get_width() // 2, 200))
    
    option2 = option_font.render('2. MCTS (Yellow)', True, BLACK)
    option2_rect = option2.get_rect(center=(screen.get_width() // 2, 250))
    
    # Draw everything
    screen.fill(WHITE)
    screen.blit(title, title_rect)
    screen.blit(option1, option1_rect)
    screen.blit(option2, option2_rect)
    
    pygame.display.flip()
    
    # Wait for user selection
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return "minimax"  # Minimax goes first
                elif event.key == pygame.K_2:
                    return "mcts"  # MCTS goes first
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

def main():
    """Main entry point for the Connect Four game."""
    # Initialize pygame
    pygame.init()
    
    # Set up the display
    screen_width = 700
    screen_height = 700
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('Connect Four AI')
    
    running = True
    while running:  # Main application loop
        # Display menu and get user selection
        mode = display_menu(screen)
        
        # If it's a human vs AI game, ask who goes first
        first_player = 1  # Default: Human goes first
        if mode == 1 or mode == 2:  # Human vs AI modes
            first_player = choose_first_player(screen)
        
        # Start the game with the selected mode
        if mode == 1:
            game = Game(ai_type="minimax", first_player=first_player)
        elif mode == 2:
            game = Game(ai_type="mcts", first_player=first_player)
        else:  # mode == 3 (AI vs AI battle)
            # Ask which AI should go first
            first_ai = choose_first_ai(screen)
            
            # The second AI is whichever one isn't the first
            second_ai = "mcts" if first_ai == "minimax" else "minimax"
            
            game = Game(ai_type="battle", first_ai=first_ai, second_ai=second_ai)
        
        # Run the game
        # If it returns True, we go back to the menu (handled by the outer loop)
        # If it returns False, we exit the application
        if not game.run():
            running = False
    
    # Clean up
    pygame.quit()

if __name__ == "__main__":
    main()