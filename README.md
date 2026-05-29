# VideoGame2D

Small 2D RPG prototype built with Pygame.

## Features
- Internal render resolution scaled to a window with letterboxing
- Large map background with camera follow
- Player movement with animations and collisions
- Decorative atlas auto-extraction (no manual slicing)

## Requirements
- Python 3.10+
- Pygame

## Install
```bash
pip install pygame
```

## Run
```bash
python main.py
```

## Controls
- Move: WASD
- Quit: Close the window

## Project Structure
- main.py: entry point
- game.py: main loop and scaling
- level.py: map, camera, decorations
- player.py: player movement and animations
- support.py: asset helpers
- assets/graphics: sprites and atlases

## Notes
If you add new assets, keep the same naming convention for player frames:
- persontop1.png ... persontop3.png
- personback1.png ... personback3.png
- personleft1.png ... personleft3.png
- personright1.png ... personright3.png
