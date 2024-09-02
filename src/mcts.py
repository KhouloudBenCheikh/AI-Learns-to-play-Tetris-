import numpy as np
from collections import defaultdict
from board import Board
from copy import deepcopy
from piece import Piece
from greedy import Greedy_AI

"""
Monte Carlo Tree Search (MCTS) AI for determining the best move in a Tetris game.
"""

# Initialize Greedy AI for evaluation
greed = Greedy_AI()

class MCTS_AI:
    """
    MCTS AI to determine the best move for a given Tetris board and piece.
    """

    def get_best_move(self, board, piece):
        """
        Determines the best move for the given board and piece using MCTS.
        """
        initial_state = State(board, piece, 0)
        root = MonteCarloTreeSearchNode(initial_state)
        selected_node = root.best_action()
        action = selected_node.parent_action
        return action[1], action[0]  # Return x, piece

class State:
    """
    Represents a state in the Tetris game, including the board, piece, depth, and cleared rows.
    """

    def __init__(self, board, piece, depth, cleared=0):
        """
        Initializes a state with the given board, piece, depth, and cleared rows.
        """
        self.board = board
        self.piece = piece
        self.depth = depth
        self.cleared = cleared

    def get_legal_actions(self):
        """
        Generates a list of all legal actions for the current state.
        """
        actions = []
        piece = self.piece
        for _ in range(4):  # Try all rotations
            piece = piece.get_next_rotation()
            for x in range(self.board.width):
                try:
                    y = self.board.drop_height(piece, x)
                except IndexError:
                    continue  # Skip if the piece cannot be placed
                actions.append((piece, x, y))
        return actions

    def move(self, action):
        """
        Applies the given action to the current state and returns the resulting new state.
        """
        board_copy = deepcopy(self.board)
        piece, x, y = action
        board_copy.place(x, y, piece)
        cleared = board_copy.clear_rows()
        return State(board_copy, Piece(), self.depth + 1, self.cleared + cleared)

    def is_game_over(self):
        """
        Checks if the game is over. (Placeholder, should be implemented)
        """
        return False

    def game_result(self):
        """
        Evaluates the result of the game from the current state.
        """
        return -greed.cost0(self.board)

class MonteCarloTreeSearchNode:
    """
    Represents a node in the MCTS tree, including the state, children, and statistics.
    """

    def __init__(self, state, parent=None, parent_action=None):
        """
        Initializes a node with the given state, parent, and parent action.
        """
        self.state = state
        self.parent = parent
        self.parent_action = parent_action
        self.children = []
        self._number_of_visits = 0
        self._results = defaultdict(int)
        self._results[1] = 0
        self._results[-1] = 0
        self._score = 0
        self._untried_actions = self.untried_actions()

    def untried_actions(self):
        """
        Returns a list of actions that have not yet been tried from this node.
        """
        self._untried_actions = self.state.get_legal_actions()
        return self._untried_actions

    def q(self):
        """
        Returns the current score of the node.
        """
        return self._score

    def n(self):
        """
        Returns the number of times this node has been visited.
        """
        return self._number_of_visits

    def expand(self):
        """
        Expands the node by adding a new child node.
        """
        action = self._untried_actions.pop()
        next_state = self.state.move(action)
        child_node = MonteCarloTreeSearchNode(next_state, parent=self, parent_action=action)
        self.children.append(child_node)
        return child_node

    def is_terminal_node(self):
        """
        Checks if the current node represents a terminal state.
        """
        return self.state.is_game_over()

    def rollout(self):
        """
        Performs a rollout to simulate the outcome of a game from the current state.
        """
        current_rollout_state = self.state
        while not current_rollout_state.is_game_over():
            possible_moves = current_rollout_state.get_legal_actions()
            action = self.rollout_policy(possible_moves)
            current_rollout_state = current_rollout_state.move(action)
        return current_rollout_state.game_result()

    def backpropagate(self, result):
        """
        Backpropagates the result of a rollout up the tree to update node statistics.
        """
        self._number_of_visits += 1
        self._score += result
        if self.parent:
            self.parent.backpropagate(result)

    def is_fully_expanded(self):
        """
        Checks if the node has been fully expanded.
        """
        return len(self._untried_actions) == 0

    def best_child(self, c_param=0.1):
        """
        Selects the best child node based on the UCB1 formula.
        """
        choices_weights = [
            (child.q() / child.n()) + c_param * np.sqrt((2 * np.log(self.n()) / child.n()))
            for child in self.children
        ]
        return self.children[np.argmax(choices_weights)]

    def rollout_policy(self, possible_moves):
        """
        Selects a move during the rollout phase.
        """
        return np.random.choice(possible_moves)

    def _tree_policy(self):
        """
        Determines the node to expand using the tree policy.
        """
        current_node = self
        while not current_node.is_terminal_node():
            if not current_node.is_fully_expanded():
                return current_node.expand()
            else:
                current_node = current_node.best_child()
        return current_node

    def best_action(self):
        """
        Determines the best action by performing simulations and selecting the best child.
        """
        for _ in range(self.simulations):
            v = self._tree_policy()
            reward = v.rollout()
            v.backpropagate(reward)
        return self.best_child(c_param=0.0)

