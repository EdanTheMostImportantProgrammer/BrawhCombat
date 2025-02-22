# BrawhCombat

## Description
BrawhCombat is a 2D multiplayer fighting game built using Pygame. Two players control characters that can move, jump, and collide with each other to deal damage. The goal is to deplete the opponent's health and be the last one standing!

## Features
- **Two-player local gameplay**
- **Physics-based movement and gravity**
- **Health bar system**
- **Dynamic animations and smooth controls**
- **Beautiful pixel-art environment with clouds and grass**
- **Main menu and game over screen**

## Controls
### Player 1:
- `A` - Move left
- `D` - Move right
- `Space` - Jump

### Player 2:
- `Left Arrow` - Move left
- `Right Arrow` - Move right
- `Up Arrow` - Jump

## How to Play
1. Launch the game.
2. On the main menu, press any key to start.
3. Move and jump to avoid attacks while trying to push your opponent.
4. If your opponent's health reaches zero, you win!
5. Press any key to exit after the game over screen.

## Installation
### Prerequisites
- Python 3.x
- Pygame (`pip install pygame`)

### Running the Game
1. Clone this repository or download the files.
2. Make sure the following image assets are in the correct directories:
   - `ground.png`
   - `grass1.png`
   - `grass2.png`
   - `cloud.png`
   - `Player1/left.png`, `Player1/right.png` (and variations)
   - `Player2/left.png`, `Player2/right.png` (and variations)
3. Open a terminal in the project directory.
4. Run the game:
   ```sh
   python game.py
   ```

## Future Improvements
- Add sound effects and background music
- Implement AI for single-player mode
- Introduce power-ups and special abilities
- Improve collision detection and movement physics

## License
This project is open-source. Feel free to modify and improve it!

## Author
Created by Leonabcd123 And edog007.
