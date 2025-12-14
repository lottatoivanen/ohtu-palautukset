# Rock Paper Scissors - Web User Interface

A Flask-based web interface for the Rock Paper Scissors game that reuses all the existing game logic from the command-line application.

## Features

- **Player vs Player**: Two players compete against each other via the web interface
- **Player vs AI**: Play against a basic AI opponent
- **Player vs Enhanced AI**: Play against an improved AI opponent
- **Beautiful UI**: Modern, responsive design with emoji-based move selection
- **Game History**: Track all moves and results in real-time
- **Score Board**: Keep track of points, draws, and overall statistics

## Installation & Setup

### Requirements
- Python 3.12+
- Poetry

### Install Dependencies

```bash
cd viikko7/kivi-paperi-sakset
poetry install
```

## Running the Application

### Start the Flask Server

```bash
cd viikko7/kivi-paperi-sakset
poetry run python src/app.py
```

The application will start on `http://localhost:5000`

### Usage

1. Open your browser and navigate to `http://localhost:5000`
2. Select a game mode:
   - **Player vs Player** (a) - for two human players
   - **Player vs AI** (b) - for playing against the basic AI
   - **Player vs Enhanced AI** (c) - for playing against the improved AI
3. Select your move using the buttons:
   - 🪨 **k** = Rock (Kivi)
   - 📄 **p** = Paper (Paperi)  
   - ✂️ **s** = Scissors (Sakset)
4. For Player vs Player, both players select their moves before clicking "Play Round"
5. For AI modes, select your move and the computer will automatically respond
6. Track your score and game history in real-time

## Architecture

The web interface is built with:
- **Backend**: Flask web framework
- **Frontend**: HTML5, CSS3, JavaScript (vanilla)
- **Game Logic**: Reuses 100% of the existing game classes:
  - `KiviPaperiSakset` - Base game class
  - `KPSPelaajaVsPelaaja` - Player vs Player
  - `KPSTekoaly` - AI opponent
  - `KPSParempiTekoaly` - Enhanced AI opponent
  - `Tuomari` - Score tracking
  - `Tekoaly` / `Tekoaly_parannettu` - AI logic

## API Endpoints

### GET `/`
Returns the home page with game mode selection.

### GET `/game/<mode>`
Starts a new game session with the specified mode (`a`, `b`, or `c`).

### POST `/api/play`
Plays a round of the game.

**Request body**:
```json
{
  "first_move": "k|p|s",
  "second_move": "k|p|s"  // Only required for player vs player mode
}
```

**Response**:
```json
{
  "first_move": "k",
  "second_move": "p",
  "first_score": 1,
  "second_score": 0,
  "draws": 0,
  "valid": true
}
```

### GET `/api/status`
Returns the current game status and history.

**Response**:
```json
{
  "first_score": 1,
  "second_score": 0,
  "draws": 0,
  "history": [...]
}
```

## Code Organization

```
src/
├── app.py                          # Flask application and game wrapper
├── index.py                        # Original CLI entry point
├── kivi_paperi_sakset.py          # Base game class (unchanged)
├── kps_pelaaja_vs_pelaaja.py      # PvP game class (unchanged)
├── kps_tekoaly.py                 # AI game class (unchanged)
├── kps_parempi_tekoaly.py         # Enhanced AI class (unchanged)
├── tuomari.py                     # Score tracking (unchanged)
├── tekoaly.py                     # AI logic (unchanged)
├── tekoaly_parannettu.py          # Enhanced AI logic (unchanged)
├── luo_peli.py                    # Game factory (unchanged)
├── player_reader.py               # Possibly from a different exercise (unchanged)
├── player.py                      # Possibly from a different exercise (unchanged)
└── templates/
    ├── base.html                  # Base template with styling
    ├── index.html                 # Home page template
    └── game.html                  # Game page template
```

## Design Notes

- **Zero Changes to Game Logic**: All existing game classes are used as-is
- **Session Management**: Each game session maintains its own `Tuomari` instance for score tracking
- **AJAX API**: The frontend uses fetch API for responsive gameplay without page reloads
- **Responsive Design**: Works on desktop and mobile devices
- **Accessibility**: Clear move labels with both emoji and text descriptions

## Future Enhancements

- User authentication for tracking stats across sessions
- Multiplayer support with WebSockets
- Difficulty levels for AI
- Match statistics and leaderboards
- Dark mode toggle
