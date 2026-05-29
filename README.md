# VideoGame2D

2D RPG prototype inspired by classic handheld style, built with Pygame.

## Features
- Internal render resolution scaled to a window with letterboxing
- Large map background with camera follow
- Player movement with directional animations
- Collisions against decorative props
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

## How It Works
### Rendering and Camera
The game renders to an internal surface (render size) and scales it to the window
with letterboxing. The camera follows the player by offsetting sprite draw positions
relative to the player's center.

### Decorative Atlas Extraction
All trees/trunks are stored in a single image. The game automatically extracts
each distinct opaque region and treats it as a separate sprite. This avoids manual
slicing and lets you add more objects to the atlas without touching the code.

## Asset Conventions
### Player Frames
If you add new assets, keep the same naming convention for player frames:
- persontop1.png ... persontop3.png
- personback1.png ... personback3.png
- personleft1.png ... personleft3.png
- personright1.png ... personright3.png

### Map and Decorations
- Map: assets/graphics/grassland3.png
- Decorations atlas: assets/graphics/grasslands decorative.png

## Configuration
Main settings live in settings.py:
- WINDOW_WIDTH / WINDOW_HEIGHT: final window size
- RENDER_WIDTH / RENDER_HEIGHT: internal render resolution
- FPS: target frame rate

## Project Structure
- main.py: entry point
- game.py: main loop and scaling
- level.py: map, camera, decorations, and placement
- player.py: player movement and animations
- support.py: asset helpers and atlas extraction
- assets/graphics: sprites and atlases

## Troubleshooting
- If decorations do not appear, confirm the atlas file exists and has distinct
	objects separated by background color or transparency.
- If performance drops, lower the map scale factor or reduce decorations.

## Roadmap Ideas
- NPCs and dialog system
- Basic combat prototype
- Inventory UI
- Save/load
