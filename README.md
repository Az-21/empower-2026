# Empower 2026

Developer setup and workflow for the weekly Python exercises in this repo.

## Project Layout

```text
question/                 # source exercise files
solution/<your_name>/     # your working copies and solutions
```

Do not edit files in `question/`. Copy the exercise you are working on into your own folder under `solution/`.

## 1. Install `uv`

### Windows (PowerShell)

```powershell
winget install astral-sh.uv
```

### Linux

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## 2. Sync the Project

From the repo root, run:

```bash
uv sync
```

## 3. Set up Formatting in VS Code

Install the `Ruff` extension from the VS Code Marketplace.

This repo already includes `ruff.toml`, so you do not need to add formatter settings to the project. Just enable format on save and set Ruff as the default formatter for Python.

Recommended `settings.json` snippet:

```json
{
  "[python]": {
    "editor.defaultFormatter": "charliermarsh.ruff",
    "editor.formatOnSave": true
  }
}
```

## 4. Copy the Exercise into Your Solution Folder

If your name is `alex`, keep the same week folder and filename under `solution/alex/`.

Example target path:

```text
solution/alex/week_03/01_rational_numbers.py
```

## 5. Run a Program

```bash
uv run <path-to-file>.py

# Example
uv run solution/alex/week_03/01_rational_numbers.py
```

## 6. Dependency Model

- Every exercise file is designed to be self-contained.
- Exercise files use only the Python standard library.
- No external Python packages are required to work on the exercises.
