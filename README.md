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

2.  **Backend Setup (Python):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    pip install -r requirements.txt
    ```

3.  **Frontend Setup (React):**
    ```bash
    cd frontend
    npm install
    ```

## Usage

### Updating Board Game Data

The `update_boardgames.py` script fetches the latest data for your board games from BGG. It reads and writes to the `boardgames.json` file. Since the frontend is now in `frontend/public`, target that file:

```bash
# From root directory
python update_boardgames.py frontend/public/boardgames.json
```

### Updating Your BGG Collection

The `update_collection.py` script helps you add your board games to your collection on the BGG website.

```bash
python update_collection.py
```

### Viewing Your Collection

The collection is now a React application.

**Development:**
```bash
cd frontend
npm run dev
```
Open `http://localhost:5173` in your browser.

**Production / GitHub Pages:**
The app is configured to deploy to GitHub Pages via GitHub Actions.

## Development

### Pre-commit Hooks

This project uses `ruff` for linting and formatting Python code.

1.  **Install pre-commit:**
    ```bash
    pip install pre-commit
    ```

2.  **Install the hooks:**
    ```bash
    pre-commit install
    ```

### Running Tests

**Python:**
```bash
python -m unittest discover tests
```

**Frontend:**
```bash
cd frontend
npm test          # Unit tests
npx playwright test # E2E tests
```
