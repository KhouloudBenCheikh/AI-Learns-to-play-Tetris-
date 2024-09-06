"""
The main function of this code is to manage the state and operations of the Tetris game board.
"""

from copy import deepcopy

class Board:

    """Initialize the board with specified dimensions and properties."""
    def __init__(self):
        self.width, self.height = 10, 20  # Set board dimensions
        self.board = self.init_board()  # Initialize the board with empty cells
        self.colors = self.init_board()  # Initialize the color board
        self.widths = [0] * (self.height + 4)  # Track the width of each row (including extra space)
        self.heights = [0] * self.width  # Track the height of each column

    """Create and return an empty board with dimensions."""
    def init_board(self):
        
        b = []
        for row in range(self.height + 4):
            row = []
            for col in range(self.width):
                row.append(False)  # Initialize cells as empty (False)
            b.append(row)
        return b

    """Revert the board to its previous state."""
    def undo(self):
        
        self.board = self.last_board
        self.colors = self.last_colors
        self.widths = self.last_widths
        self.heights = self.last_heights

    """Place a piece on the board at the specified position."""
    def place(self, x, y, piece):
        
        # Check if the placement is valid
        for pos in piece.body:
            target_y = y + pos[1]
            target_x = x + pos[0]
            if (
                target_y < 0
                or target_y >= self.height + 4
                or target_x < 0
                or target_x >= self.width
                or self.board[y + pos[1]][x + pos[0]]
            ):
                return Exception("Bad placement")  # Invalid placement
        # Place the piece and update board state
        for pos in piece.body:
            self.board[y + pos[1]][x + pos[0]] = True
            self.colors[y + pos[1]][x + pos[0]] = piece.color
            self.widths[y + pos[1]] += 1
            self.heights[x + pos[0]] = max(self.heights[x + pos[0]], y + pos[1] + 1)
        return 0

    """Calculate the drop height of a piece at column x."""
    def drop_height(self, piece, x):
    
        y = -1
        for i in range(len(piece.skirt)):
            y = max(self.heights[x + i] - piece.skirt[i], y)
        return y

    """Check if the top rows of the board are filled."""
    def top_filled(self):
        
        return sum([w for w in self.widths[-4:]]) > 0

    """Clear completed rows and update board state."""
    def clear_rows(self):
        
        num = 0
        to_delete = []
        # Identify full rows to clear
        for i in range(len(self.widths)):
            if self.widths[i] < self.width:
                continue
            num += 1
            to_delete.append(i)

        # Remove full rows and update board
        for row in to_delete:
            del self.board[row]
            self.board.append([False] * self.width)

            del self.widths[row]
            self.widths.append(0)

            del self.colors[row]
            self.colors.append([False] * self.width)

        # Update heights after clearing rows
        if num > 0:
            heights = []
            for col in range(self.width):
                m = 0
                for row in range(self.height):
                    if self.board[row][col]:
                        m = row + 1
                heights.append(m)
            self.heights = heights
        return num
