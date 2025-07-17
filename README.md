# ClayGame

ClayGame is a small experimental project that mixes turn‑based strategy with a
comedic claymation art style.  Players control heroic animal soldiers defending
the fictional land of Clayonia from bumbling invaders.  Most art assets are
generated or processed to look like stop‑motion clay figures.

## Installation
1. Ensure Python 3.10+ is installed.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Game
Execute the main entry point:
```bash
python main.py
```

The game opens with a short cutscene and then drops you into a basic battle
scenario.  Use the arrow keys to move and space to advance dialogue.

## Debugging
Press **F3** during gameplay to toggle an overlay showing the current FPS and
player position. This can help when tuning sprite behavior or level layouts.

## Asset Generation
The repository includes a script, `generate_assets.py`, which creates placeholder
sprites and other resources.  Run it if you wish to regenerate the sample images
located in the `assets/` folder:

```bash
python generate_assets.py
```

Generated files will appear under `assets/`.

For custom clay-style artwork you can also use the GUI in `tools/clay_generator_gui.py`:

```bash
python tools/clay_generator_gui.py
```

This tool can call a local Stable Diffusion model or the DALL·E API (requires an
OpenAI API key) to generate new sprites.

## Scene Templates
Example battle setups are stored in `assets/scenes/`. The simple designer state
(`scene_designer_state.py`) lets you drag sprites around and save a new template
JSON file for later use.

The optional `voice_input.py` module demonstrates how to transcribe audio using
the Whisper API, allowing future tools to create scenes from spoken commands.

