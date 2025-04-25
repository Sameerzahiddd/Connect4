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

def get_first_player(screen, mode):
    """Get who should play first."""
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
    if mode == 3:  # AI vs AI
        title = title_font.render('Who should play first?', True, BLUE)
        option1 = option_font.render('1. Minimax AI (Red)', True, RED)
        option2 = option_font.render('2. MCTS AI (Yellow)', True, YELLOW)
    else:  # Human vs AI
        title = title_font.render('Who should play first?', True, BLUE)
        option1 = option_font.render('1. You (Red)', True, RED)
        option2 = option_font.render('2. AI (Yellow)', True, YELLOW)
    
    title_rect = title.get_rect(center=(screen.get_width() // 2, 150))
    option1_rect = option1.get_rect(center=(screen.get_width() // 2, 250))
    option2_rect = option2.get_rect(center=(screen.get_width() // 2, 350))
    
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
                    return 1  # Human/Minimax goes first
                elif event.key == pygame.K_2:
                    return 2  # AI/MCTS goes first
                elif event.key == pygame.K_ESCAPE:
                    return None  # Back to main menu

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
        
        # Get who should play first
        first_player = get_first_player(screen, mode)
        
        if first_player is None:
            continue  # Back to main menu
        
        # Start the game with the selected mode
        if mode == 1:
            game = Game(ai_type="minimax", first_player=first_player)
        elif mode == 2:
            game = Game(ai_type="mcts", first_player=first_player)
        else:  # mode == 3
            # For AI vs AI, first_player=1 means minimax goes first, first_player=2 means MCTS goes first
            game = Game(ai_type="battle", first_ai="minimax", second_ai="mcts", first_player=first_player)
        
        # Run the game
        # If it returns True, we go back to the menu (handled by the outer loop)
        # If it returns False, we exit the application
        if not game.run():
            running = False
    
    # Clean up
    pygame.quit()

if __name__ == "__main__":
    main()