# 2048 Game

Welcome to the 2048 game! This is a clone of the popular 2048 puzzle game, built using Pygame. The objective of the game is to slide numbered tiles on a grid to combine them and create a tile with the number 2048.

## Features

- **Smooth Animations**: Enjoy a seamless gameplay experience with smooth tile animations.
- **Sound Effects**: The game includes various sound effects for actions like moves, game start, and game over.
- **Intuitive Controls**: Use the arrow keys to move the tiles.
- **Score Tracking**: Keep track of your score as you play.

## Getting Started

### Prerequisites

Ensure you have Python and Pygame installed on your system.

You can install Pygame using pip:

```bash
pip install pygame
```

### Running the Game

1. Clone the repository:

   ```bash
   git clone https://github.com/sayhan1610/2048.git
   cd 2048
   ```

2. Run the game:
   ```bash
   python main.py
   ```

### Game Instructions

- **Move Tiles**: Use the arrow keys (↑, ↓, ←, →) to move the tiles.
- **Objective**: Merge the tiles to reach the 2048 tile.
- **Toggle Animations**: Press `D` to enable or disable tile animations.
- **Home Screen**: Press `Enter` to start the game from the home screen.
- **Instructions Screen**: Press `I` on the home screen to view the instructions.
- **Game Over**: When the game is over, press `Enter` to restart the game.

## Code Overview

### Main Components

- **Game State Management**: The game uses different states such as home, game, instructions, and game over to manage the game flow.
- **Tile Animations**: Animations for moving tiles are implemented for a smooth user experience.
- **Sound Effects**: Various sound effects are included to enhance the gameplay.

### Key Functions

- `initialize_board()`: Initializes the game board with two random tiles.
- `add_random_tile(board)`: Adds a random tile (2 or 4) to an empty spot on the board.
- `move_left(board)`, `move_right(board)`, `move_up(board)`, `move_down(board)`: Functions to handle the movement and merging of tiles in different directions.
- `draw_board(board, score, moving_tiles, elapsed_time, animations_enabled)`: Renders the game board and tiles.
- `draw_home_page()`, `draw_instructions_page()`, `draw_game_over_page(score)`: Functions to render different game screens.

### Sound Files

- **game_start.mp3**: Played when the game starts.
- **bg_music.mp3**: Background music played during the game.
- **move.mp3**: Played when tiles are moved.
- **game_over.mp3**: Played when the game is over.

### Dependencies

- `pygame`: The game is built using the Pygame library for Python.

## Contributing

Feel free to fork the repository and submit pull requests. Contributions, whether it's improving the code, adding features, or fixing bugs, are welcome!

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- Inspired by the original 2048 game by Gabriele Cirulli.

Enjoy the game and have fun reaching 2048!
