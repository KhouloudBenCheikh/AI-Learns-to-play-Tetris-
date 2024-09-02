from random import choice
import numpy as np

# Define colors as RGB tuples
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
INDIGO = (255, 0, 255)
TURQ = (64, 224, 208)

# Define piece shapes and colors
BODIES = [
    (((0, 0), (0, 1), (0, 2), (0, 3)), RED),  # Stick
    (((0, 0), (0, 1), (0, 2), (1, 0)), ORANGE),  # L1
    (((0, 0), (1, 0), (1, 1), (1, 2)), ORANGE),  # L2
    (((0, 0), (1, 0), (1, 1), (2, 1)), GREEN),  # S1
    (((0, 1), (1, 0), (1, 1), (2, 0)), GREEN),  # S2
    (((0, 0), (0, 1), (1, 0), (1, 1)), TURQ),  # Square
    (((0, 0), (1, 0), (1, 1), (2, 0)), CYAN),  # Pyramid
]

class Piece:
    """
    Represents a Tetris piece, including its body shape and color.
    The piece is defined by its body coordinates and color.
    """

    def __init__(self, body=None, color=None):
        """
        Initializes a Tetris piece. If no body is provided, a random piece is chosen from predefined shapes.
        """
        if body is None:
            self.body, self.color = choice(BODIES)
        else:
            self.body = body
            self.color = color
        self.skirt = self.calc_skirt()

    def calc_skirt(self):
        """
        Calculates the skirt of the piece, which is the minimum y-coordinate for each x-coordinate in the piece's body.
        """
        skirt = [float('inf')] * 4  # Assuming maximum 4 columns
        for x, y in self.body:
            if 0 <= x < len(skirt):
                skirt[x] = min(skirt[x], y)
        return skirt

    def get_next_rotation(self):
        """
        Returns a new Piece that is a rotated version of the current piece.
        The rotation is counterclockwise 90 degrees.
        """
        width = len(self.skirt)
        new_body = [(width - y - 1, x) for x, y in self.body]
        leftmost = min(x for x, _ in new_body)
        new_body = [(x - leftmost, y) for x, y in new_body]
        return Piece(new_body, self.color)

def main():
    """
    Test the Piece class by printing the skirt of each predefined piece shape.
    """
    for body in BODIES:
        piece = Piece(body)
        print(f"Piece Skirt: {piece.skirt}")

if __name__ == "__main__":
    main()
