"""
Tetris AI Project

This package includes modules for the Tetris AI implementation,
including game logic, AI strategies, and experiment running.
"""

__version__ = '1.0'
__author__ = 'Khouloud BEN CHEIKH'

# Import key classes and functions for easy access
from .game import Game
from .piece import Piece
from .mcts import MCTS_AI
from .genetic_controller import run_X_epochs
from .run_experiments import run_genetic_experiments
