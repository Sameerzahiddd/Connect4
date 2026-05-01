# Connect 4 — Documentation

> A Python implementation of Connect Four featuring two distinct AI opponents, adjustable difficulty levels, and an AI vs AI battle mode.

---

## Getting Started

### Requirements
- Python 3.7+
- Pygame
- NumPy

### Installation

```bash
git clone https://github.com/Sameerzahiddd/Connect4
cd Connect4
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Running the Game

```bash
python main.py
```

---

## Game Modes

### 1. Human vs Minimax AI
Play against an AI powered by the Minimax algorithm with Alpha-Beta pruning. The AI thinks ahead by exploring possible future moves and choosing the one most likely to lead to a win. At higher difficulties, it searches deeper into the game tree, making it significantly harder to beat.

### 2. Human vs MCTS AI
Play against an AI powered by Monte Carlo Tree Search. Rather than exhaustively evaluating every possible move, MCTS runs thousands of random game simulations and learns which moves tend to produce wins over time. It plays differently to Minimax — less predictable, more probabilistic.

### 3. AI vs AI Battle
Watch Minimax and MCTS compete against each other. You choose which AI goes first and set the difficulty for each independently. Useful for observing how the two algorithms behave differently under the same conditions.

---

## Difficulty Levels

| Difficulty | Minimax Search Depth | MCTS Iterations | MCTS Time Limit |
|---|---|---|---|
| Easy | 2 | 1,000 | 0.5s |
| Medium | 3 | 5,000 | 2.0s |
| Hard | 5 | 10,000 | 5.0s |

Higher difficulty means the AI thinks longer and further ahead. On Hard, Minimax evaluates up to 5 moves deep, and MCTS runs up to 10,000 simulations before deciding.

---

## Controls

| Key | Action |
|---|---|
| Mouse click | Drop a piece into a column (Human vs AI modes) |
| `R` | Reset the current game |
| `Escape` | Return to main menu |

---

## AI Architecture

### Minimax with Alpha-Beta Pruning + History Heuristic

The Minimax algorithm works by building a game tree of all possible future moves up to a set depth, assuming both players play optimally. Alpha-Beta pruning eliminates branches that cannot possibly affect the final decision, significantly reducing computation time.

On top of this, the implementation uses a **history heuristic** — a table that tracks which moves have historically caused the most pruning. Moves that performed well in previous searches are tried first, improving pruning efficiency over time. These scores are persisted to `data/history_scores.json` between sessions and decay by 5% each game to prevent inflation.

The search uses **iterative deepening** — it runs Minimax at depth 1, then depth 2, up to the target depth. This ensures the best available answer is always ready even if time runs out.

### Monte Carlo Tree Search (MCTS)

MCTS builds a search tree using four repeated phases:

1. **Selection** — navigate the existing tree using the UCT formula, balancing exploitation (known good moves) and exploration (less visited moves)
2. **Expansion** — add a new child node for an untried move
3. **Simulation** — play out a random game from that position to a terminal state
4. **Backpropagation** — update visit counts and win statistics up the tree

The UCT formula used is:

```
UCT = win_ratio + exploration_weight × √(ln(parent_visits) / child_visits)
```

Draws count as half-wins (0.5) in the win statistics. The best move is selected by visit count, not win rate — the most explored move is considered the most reliable.

---

## Project Structure

```
Connect4/
├── main.py               # Entry point, menus, game mode selection
├── requirements.txt
├── data/
│   └── history_scores.json   # Persisted Minimax history heuristic
└── src/
    ├── game.py           # Game controller, game loop, move handling
    ├── gui.py            # Pygame rendering
    ├── models/
    │   └── board.py      # Board state, move validation, win detection
    └── ai/
        ├── minimax.py    # Minimax + Alpha-Beta + history heuristic
        ├── mcts.py       # Monte Carlo Tree Search
        └── evaluation.py # Board evaluation function for Minimax
```

---

## What's New

*Update this section when new features ship to production.*

---

## Breaking Changes

*Update this section when breaking changes ship to production.*
