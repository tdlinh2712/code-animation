# Code Animation: Stack & Valid Parentheses Visualizer

This project provides animated visualizations of stack operations and the valid parentheses problem using [Manim Community Edition](https://docs.manim.community/).

## Features
- **Stack Visualization**: See push and pop operations animated step-by-step.
- **Valid Parentheses Visualizer**: Watch how a stack is used to check if a string of parentheses is valid, with color-coded feedback for matches (green) and errors (red).
- **Custom Input**: Pass your own parentheses string for visualization.

## Environment
- **Python version**: 3.9+ recommended
- **Manim Community Edition**: v0.19.0
- All dependencies should be installed in a virtual environment (e.g., `venv`, `conda`, or `micromamba`).

## Setup
1. Clone the repository:
   ```sh
   git clone <your-repo-url>
   cd code-animation
   ```
2. Install dependencies:
   ```sh
   pip install manim
   # or use your environment manager (conda/micromamba)
   ```

## Usage
### 1. Stack Visualization
To run the basic stack animation:
```sh
manim -pql src/stack_visualization.py StackScene
```

### 2. Valid Parentheses Visualization
To run the valid parentheses visualizer with the default string:
```sh
manim -pql src/valid_parentheses_visualization.py ValidParenthesesScene
```

To use your own input string (e.g., `'([)]'`), pass it as an environment variable:
```sh
INPUT_STR='([)]' manim -pql src/valid_parentheses_visualization.py ValidParenthesesScene
```
- **Note:** If your string contains special shell characters (like `[`, `]`, `{`, `}`), always wrap it in single quotes `'...'`.

## File Structure
- `src/stack_visualization.py` — Stack animation scene
- `src/valid_parentheses_visualization.py` — Valid parentheses animation scene
- `src/dsa/stack.py` — Stack class logic and animation helpers

## Troubleshooting
- If you get `ModuleNotFoundError`, make sure you are running Manim from the project root and your `PYTHONPATH` includes `src` if needed.
- For Manim Community v0.19.0, **do not use `--config`** for custom arguments; use environment variables as shown above.

## License
MIT
