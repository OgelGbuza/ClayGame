# Development instructions for ClayGame

- This project is a Python 3.10+ Pygame prototype.
- Keep code compatible with Python 3.10 and follow PEP 8 with 4-space indentation.
- Document new functions or modules with concise docstrings.
- After modifying any `.py` files, ensure they compile with:
  ```bash
  python -m py_compile $(git ls-files '*.py')
  ```
- When adding new features or scripts, update `README.md` if usage or dependencies change.
- Mention the relevant user request in each commit message.
