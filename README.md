# AI Learns to play Tetris 

This project manages and runs a Tetris game with various AI algorithms. It includes implementations for **Greedy AI**, **Monte Carlo Tree Search (MCTS) AI**, and **Genetic Algorithm**. The game can be played with different *AI strategies* or *manually*, and it tracks and displays Statistics such as pieces dropped and rows cleared.

- **Genetic Algorithm AI**: Utilizes genetic algorithms to evolve and optimize its performance.
- **Greedy AI**: Implements a heuristic approach to make decisions based on immediate benefits.
- **Monte Carlo Tree Search (MCTS) AI**: Uses MCTS for decision-making by simulating and evaluating potential future moves.

## Project Structure

- **`genetic.py`**: Contains the implementation of the Genetic Algorithm AI. This AI uses a genotype to evaluate board states and determine the best move.
- **`greedy.py`**: Implements the Greedy AI that chooses the move with the minimal cost based on heuristic evaluation.
- **`mcts.py`**: Includes the Monte Carlo Tree Search AI for decision-making using simulations to find the best move.
- **`main.py`**: The entry point of the application. It runs the game with the AI agents.
- **`game.py`**: Contains the core game logic, including the game loop and interaction with the AI agents.
- **`board.py`**: Defines the board representation and manipulation functions.
- **`piece.py`**: Manages the Tetris pieces and their rotations.
- **`genetic_helpers.py`**: Helper functions used by the Genetic Algorithm AI.
  
## Requirements

To install the necessary dependencies, run:

```sh
pip install -r requirements.txt 
```

## Configuration

Clone the repository:

   ```bash
   git clone https://github.com/KhouloudBenCheikh/AI-Learns-to-play-Tetris-.git
   cd AI-Learns-to-play-Tetris-
   ```

## Running 🎮

To play the game manually, and the Control buttons are (Left, Right, Down, Up):

```sh
python src/main.py player
```

## AI Algorithms 🤖
#### Greedy AI
To run the game with the Greedy AI:

```sh
python src/main.py greedy 
```

#### Monte Carlo Tree Search AI
To run the game with the Monte Carlo Tree Search (MCTS) AI:

```sh
python src/main.py mcts 
```

#### Genetic Algorithm
To run the game with the Genetic Algorithm:

```sh
python src/main.py genetic
```

## Author
This project is maintained by [Khouloud BEN CHEIKH](https://www.linkedin.com/in/khouloudbencheikh/) 🦋