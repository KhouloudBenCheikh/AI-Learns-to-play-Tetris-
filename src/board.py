# src/board.py

import numpy as np
from piece import Piece

class Board:
    def __init__(self, width=10, height=20):
        """Initialize a game board with the specified width and height."""
        self.width = width
        self.height = height
        self.board = np.zeros((height, width), dtype=int)  # Empty board
        self.widths = np.zeros(width, dtype=int)           # Widths of each column
        self.heights = np.zeros(width, dtype=int)          # Heights of each column

    def place(self, x, y, piece):
        """Place a piece on the board at position (x, y)."""
        for (px, py) in piece.body:
            if 0 <= x + px < self.width and 0 <= y + py < self.height:
                self.board[y + py, x + px] = 1
                self.heights[x + px] = max(self.heights[x + px], y + py + 1)
                self.widths[x + px] = max(self.widths[x + px], y + py + 1)

    def clear_rows(self):
        """Clear completed rows and return the number of rows cleared."""
        cleared_rows = 0
        rows_to_clear = np.all(self.board, axis=1)  # Identify complete rows
        for row in np.where(rows_to_clear)[0]:
            self.board[1:row+1, :] = self.board[:row, :]  # Move rows down
            self.board[0, :] = 0  # Clear the top row
            cleared_rows += 1
        return cleared_rows

    def drop_height(self, piece, x):
        """Calculate the drop height of a piece at position x."""
        for y in range(self.height - 1, -1, -1):
            if self._can_place(piece, x, y):
                return y
        raise ValueError("Piece cannot be placed at this column.")

    def _can_place(self, piece, x, y):
        """Check if a piece can be placed at position (x, y)."""
        for (px, py) in piece.body:
            if not (0 <= x + px < self.width and 0 <= y + py < self.height):
                return False
            if self.board[y + py, x + px] != 0:
                return False
        return True

    def __str__(self):
        """Return a string representation of the board."""
        return '\n'.join([' '.join(['#' if cell else '.' for cell in row]) for row in self.board])
