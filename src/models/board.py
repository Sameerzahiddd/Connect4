import numpy as np

class Board:
    """Connect Four game board representation."""
    
    def __init__(self, rows=6, cols=7):
        """Initialize an empty board."""
        self.rows = rows
        self.cols = cols
        self.board = np.zeros((rows, cols), dtype=int)
        self.last_move = None
    
    def get_cell(self, row, col):
        """Get the value at a specific cell."""
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return self.board[row][col]
        return None
    
    def drop_piece(self, col, player):
        """
        Drop a piece into the specified column.
        
        Args:
            col: Column index
            player: Player number (1 or 2)
            
        Returns:
            success: True if the piece was dropped, False if the column is full
        """
        if not self.is_valid_move(col):
            return False
        
        # Find the lowest empty row
        for row in range(self.rows - 1, -1, -1):
            if self.board[row][col] == 0:
                self.board[row][col] = player
                self.last_move = (row, col)
                return True
        
        return False
    
    def is_valid_move(self, col):
        """Check if a column is valid for placing a piece."""
        if col < 0 or col >= self.cols:
            return False
        
        # Check if top row of this column is empty
        return self.board[0][col] == 0
    
    def get_valid_moves(self):
        """Get all valid moves (columns where pieces can be placed)."""
        return [col for col in range(self.cols) if self.is_valid_move(col)]
    
    def check_win(self, row, col, player):
        """
        Check if the last move at (row, col) resulted in a win for the player.
        
        Args:
            row, col: Position of the last move
            player: Player to check for
            
        Returns:
            win: True if the player has won, False otherwise
        """
        # Store winning coordinates
        self.winning_pieces = []
        
        # Check horizontal
        count = 0
        start_col = max(0, col - 3)
        end_col = min(self.cols - 1, col + 3)
        
        for c in range(start_col, end_col + 1):
            if self.board[row][c] == player:
                count += 1
                self.winning_pieces.append((row, c))
                if count >= 4:
                    return True
            else:
                count = 0
                self.winning_pieces = []
        
        # Check vertical
        count = 0
        self.winning_pieces = []
        start_row = max(0, row - 3)
        end_row = min(self.rows - 1, row + 3)
        
        for r in range(start_row, end_row + 1):
            if self.board[r][col] == player:
                count += 1
                self.winning_pieces.append((r, col))
                if count >= 4:
                    return True
            else:
                count = 0
                self.winning_pieces = []
        
        # Check diagonal /
        count = 0
        self.winning_pieces = []
        # Find the top-left starting point of the diagonal
        r, c = row, col
        while r < self.rows - 1 and c > 0 and count < 3:
            r += 1
            c -= 1
        
        # Check the diagonal
        while r >= 0 and c < self.cols:
            if self.board[r][c] == player:
                count += 1
                self.winning_pieces.append((r, c))
                if count >= 4:
                    return True
            else:
                count = 0
                self.winning_pieces = []
            r -= 1
            c += 1
        
        # Check diagonal \
        count = 0
        self.winning_pieces = []
        # Find the top-right starting point of the diagonal
        r, c = row, col
        while r < self.rows - 1 and c < self.cols - 1 and count < 3:
            r += 1
            c += 1
        
        # Check the diagonal
        while r >= 0 and c >= 0:
            if self.board[r][c] == player:
                count += 1
                self.winning_pieces.append((r, c))
                if count >= 4:
                    return True
            else:
                count = 0
                self.winning_pieces = []
            r -= 1
            c -= 1
        
        self.winning_pieces = []
        return False
    def is_winner(self, player):
        """
        Check if the player has won the game.
        
        Args:
            player: Player to check
            
        Returns:
            win: True if the player has won, False otherwise
        """
        if self.last_move is None:
            return False
        
        row, col = self.last_move
        return self.check_win(row, col, player)
    
    def is_full(self):
        """Check if the board is full (draw)."""
        return len(self.get_valid_moves()) == 0