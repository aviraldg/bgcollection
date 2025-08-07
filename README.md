# Board Game Collection

This project helps you manage your board game collection. It provides scripts to:

- Fetch board game data from BoardGameGeek (BGG).
- Keep your collection updated.
- Visualize your collection with an interactive HTML page.

## Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/aviraldg/bgcollection.git
    cd bgcollection
    ```

2.  **Create a virtual environment (optional but recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

### Updating Board Game Data

The `update_boardgames.py` script fetches the latest data for your board games from BGG. It reads the `boardgames.json` file, finds any games with missing information, and fetches the data from BGG.

To run the script:
```bash
python update_boardgames.py boardgames.json
```

### Updating Your BGG Collection

The `update_collection.py` script helps you add your board games to your collection on the BGG website. It uses Selenium to automate the process.

To run the script:
```bash
python update_collection.py
```
The script will open a browser window and ask you to log in to your BGG account. After you log in, it will iterate through your `boardgames.json` file and add each game to your collection.

### Viewing Your Collection

Open the `index.html` file in your browser to see an interactive view of your collection. You can filter your games by various criteria and see where they are located on your shelves.

## Development

### Pre-commit Hooks

This project uses `ruff` for linting and formatting. To automatically run `ruff` before each commit, you need to install the pre-commit hooks:

1.  **Install pre-commit:**
    ```bash
    pip install pre-commit
    ```

2.  **Install the hooks:**
    ```bash
    pre-commit install
    ```

Now, `ruff` will run automatically on any changed files before you make a commit.

### Running Tests

To run the unit tests, use the following command:
```bash
python -m unittest discover tests
```
