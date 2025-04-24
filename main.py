import pygame
from src.game import Game

def main():
    """Main entry point for the Connect Four game."""
    # Initialize pygame
    pygame.init()
    
    # Start the game
    game = Game()
    game.run()
    
    # Clean up
    pygame.quit()

if __name__ == "__main__":
    main()