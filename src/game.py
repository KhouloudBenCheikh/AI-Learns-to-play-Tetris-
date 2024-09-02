import numpy as np
from piece import Piece

class Board:
    """
    Represents the Tetris board. Handles the game board's state,
    including piece placement, row clearing, and more.
    """

    def __init__(self, width=10, height=20):
        self.width = width
        self.height = height
        self.board = np.zeros((height, width), dtype=int)
        self.widths = np.zeros(width, dtype=int)
        self.heights = np.zeros(width, dtype=int)

    def drop_height(self, piece, x):
        """
        Calculate the height where the piece will land when dropped at column x.
        """
        piece_width = len(piece.skirt)
        for offset in range(piece_width):
            column = x + offset
            if column >= self.width or column < 0:
                raise ValueError("Column out of bounds")
            height = self.heights[column] - piece.skirt[offset]
            if height < 0:
                raise ValueError("Piece goes out of bounds")
        return min(self.heights[x + i] - piece.skirt[i] for i in range(piece_width))

    def place(self, x, y, piece):
        """
        Place a piece on the board at position (x, y).
        """
        for (px, py) in piece.body:
            if y + py >= self.height or x + px < 0 or x + px >= self.width:
                raise ValueError("Piece placement out of bounds")
            self.board[y + py, x + px] = 1
        self.update_heights()

    def clear_rows(self):
        """
        Clear completed rows and return the number of rows cleared.
        """
        full_rows = np.all(self.board, axis=1)
        num_cleared = np.sum(full_rows)
        self.board = np.vstack([self.board[~full_rows], np.zeros((num_cleared, self.width), dtype=int)])
        self.update_heights()
        return num_cleared

    def update_heights(self):
        """
        Update the heights of each column based on the current board state.
        """
        for x in range(self.width):
            self.heights[x] = self.height - np.max(np.where(self.board[:, x] == 1)[0], initial=-1)

class Game:
    """
    Manages the Tetris game loop, including piece management and game state.
    """

    def __init__(self, mode='normal'):
        self.board = Board()
        self.current_piece = Piece()
        self.next_piece = Piece()
        self.mode = mode
        self.score = 0

    def run_no_visual(self):
        """
        Run the game without visual representation. Returns the number of dropped pieces and rows cleared.
        """
        dropped, rows = 0, 0
        while not self.is_game_over():
            x = np.random.randint(self.board.width)
            y = self.board.drop_height(self.current_piece, x)
            self.board.place(x, y, self.current_piece)
            rows += self.board.clear_rows()
            self.score += rows
            self.current_piece = self.next_piece
            self.next_piece = Piece()
            dropped += 1
        return dropped, rows

    def run(self):
        """
        Run the game with visual representation. Includes user input handling and game updates.
        """
        # Implement game loop with visual updates
        pass

    def is_game_over(self):
        """
        Check if the game is over. The game is over if there is no space to place a new piece.
        """
        for x in range(self.board.width):
            if self.board.drop_height(self.current_piece, x) >= 0:
                return False
        return True
