# Neon Pac-Man Arcade Edition

A feature-complete 2D Pac-Man arcade game built in Python and Pygame featuring advanced ghost AI pathfinding, a finite state machine engine, particle effects, dynamic level map loading, and persistent high scores.

## Key Features

- **Finite State Machine Engine:** Modular states for Main Menu, Gameplay, Pause Menu, and Game Over overlay.
- **Distinct Ghost AI Personalities:**
  - **Blinky (Red):** Directly chases Pac-Man's location.
  - **Pinky (Pink):** Ambush predator targeting tiles ahead of Pac-Man's trajectory.
  - **Inky (Skyblue):** Strategic flanker targeting vector offsets.
  - **Clyde (Orange):** Shy wanderer that chases when far and scatters when near.
- **Power Pellets & Frightened States:** Eat Power Pellets to send ghosts into scared mode (blue rendering), granting combo point multipliers.
- **Particle System:** Dynamic visual particle bursts for collecting dots, power pellets, and capturing ghosts.
- **Dynamic Level Loader:** Map layouts read dynamically from text files in the `maps/` directory.
- **Persistent High Scores:** Automatic high score saving stored locally in `high_scores.json`.
- **Flexible Controls:** Full support for both Arrow Keys and WASD controls.

## Prerequisites

- Python 3.8+
- Pygame (`pip install -r requirements.txt`)

## How to Run

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Start the game:
   ```bash
   python main.py
   # or
   py main.py
   ```

## Game Controls

- **Arrow Keys / W, A, S, D:** Move Pac-Man
- **ENTER / SPACE:** Start game from Main Menu
- **P / ESC:** Pause / Resume game
- **R:** Restart level from Game Over screen
- **M:** Return to Main Menu

## Project Architecture

- `main.py` - Application entry point.
- `state_manager.py` - Handles Finite State Machine (Menu, Play, Pause, GameOver).
- `ghost.py` - Smart AI pathfinding and frightened ghost behaviors.
- `pac.py` - Player controller with WASD/Arrow support and combo multipliers.
- `world.py` - Game world manager, collision matrix, and sprite updates.
- `particle.py` - Dynamic particle physics for visual effects.
- `map_loader.py` - Dynamic level map parser loading files from `maps/`.
- `high_score_manager.py` - Persistent high score tracking system (`high_scores.json`).
- `asset_manager.py` - Image, surface, and font cache manager.
- `settings.py` - Game constants, grid tile dimensions, and defaults.