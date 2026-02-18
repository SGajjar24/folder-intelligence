# Contributing to Folder Intelligence (Project Phoenix)

We welcome contributions! This project has evolved into a concise, powerful Universal CLI tool (`universal_cli.py`).

## 🛠️ Development Setup

1.  **Fork & Clone**
    ```bash
    git clone https://github.com/SGajjar24/folder-intelligence.git
    cd folder-intelligence
    ```

2.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    # Ensure Tesseract OCR is installed on your system
    ```

3.  **Create a Branch**
    ```bash
    git checkout -b feature/AmazingFeature
    ```

## 🛣️ Roadmap & Help Wanted

We are actively looking for contributors to help with:

*   **[ ] GUI Dashboard**: A simple Electron or Tkinter interface for non-technical users to select folders and configs.
*   **[ ] Config Profiles**: Create more `json` config files for different use cases (e.g., `music_config.json`, `code_project_cleanup.json`).
*   **[ ] Undo System**: Create a transaction log (`undo.json`) to rollback changes if needed.
*   **[ ] Docker Support**: Create a `Dockerfile` for server-side deployment (headless mode).
*   **[ ] Unit Tests**: Add `pytest` coverage for the `UniversalOrganizer` class.

## 📐 Code Style & Conventions

*   **Core Logic:** All new logic should go into `universal_cli.py` or helper modules.
*   **Configuration:** Do **not** hardcode rules. Always use `self.config` so users can override via JSON.
*   **Safety First:**
    *   Any file operation (move/delete) **MUST** be wrapped in `if not self.dry_run:`.
    *   Always print what you are doing in Dry Run mode.
*   **Formatting:** Use `black` for Python formatting.

## 🚀 Submitting a Pull Request (PR)

1.  Ensure your code runs with `python universal_cli.py --dry-run`.
2.  Update `README.md` if you changed arguments or usage.
3.  Push to your fork and open a PR against `main`.

Thank you for making folder organization smarter! 🧠
