# Web UI Test Suite

Complete automated test suite for the Rock-Paper-Scissors Web UI application.

## Overview

- **Total Tests**: 75
- **Test Files**: 3
- **Code Coverage**: 97% (app.py), 75% overall
- **Status**: ✅ All tests passing

## Running Tests

### Run all tests
```bash
cd viikko7/kivi-paperi-sakset
poetry run pytest tests/
```

### Run with verbose output
```bash
poetry run pytest tests/ -v
```

### Run specific test file
```bash
poetry run pytest tests/test_api.py -v
poetry run pytest tests/test_routes.py -v
poetry run pytest tests/test_game_logic.py -v
```

### Run specific test class
```bash
poetry run pytest tests/test_api.py::TestPlayAPI -v
```

### Run with coverage report
```bash
poetry run pytest tests/ --cov=src --cov-report=term-missing
```

### Generate HTML coverage report
```bash
poetry run pytest tests/ --cov=src --cov-report=html
# Open htmlcov/index.html in browser
```

## Test Structure

### 1. **tests/conftest.py** (57 lines)
Pytest configuration and shared fixtures:
- Flask test client
- CLI runner
- Session cleanup
- Game instance fixtures (PvP, AI, Enhanced AI)

### 2. **tests/test_routes.py** (126 lines)
24 tests for Flask routes and templates:

**TestIndexRoute** (4 tests)
- Homepage loads correctly
- Displays all game modes
- Contains game mode links
- Shows game rules

**TestGameRoute** (8 tests)
- All game modes load (a, b, c)
- Invalid game mode redirects
- Correct titles displayed
- Contains UI elements (buttons, score board)
- Session creation

**TestTemplateRendering** (4 tests)
- Templates render without errors
- Styling included
- JavaScript loaded

### 3. **tests/test_api.py** (229 lines)
21 tests for API endpoints:

**TestPlayAPI** (10 tests)
- Valid moves return JSON
- AI returns valid moves
- Score tracking
- Invalid move rejection
- PvP move validation
- Session handling
- Game logic verification
- Score accumulation

**TestStatusAPI** (8 tests)
- Status endpoint returns JSON
- Scores and history included
- Initial state verification
- History accumulation
- Session error handling

**TestAPIValidation** (3 tests)
- Empty body handling
- Whitespace trimming
- Case conversion

### 4. **tests/test_game_logic.py** (257 lines)
30 tests for game logic and WebGame class:

**TestWebGameInitialization** (3 tests)
- Create game instances for all modes
- Proper initialization

**TestWebGameValidation** (5 tests)
- Valid moves (k, p, s)
- Invalid move rejection
- Case sensitivity

**TestWebGamePlayRound** (5 tests)
- AI round execution
- Invalid move handling
- PvP round execution

**TestWebGameScoring** (5 tests)
- Win conditions (all combinations)
- Draw detection
- Score accumulation
- Status queries

**TestWebGameHistory** (5 tests)
- History tracking
- Round recording
- Accumulation
- Data preservation

**TestAIGamePlay** (4 tests)
- AI move validity
- Response to different moves
- Enhanced AI functionality
- Pattern adaptation

**TestGameResultDetermination** (4 tests)
- Rock beats Scissors
- Scissors beats Paper
- Paper beats Rock
- Draw logic

**TestResponseFormats** (3 tests)
- Response field validation
- Data structure consistency
- History item format

## Test Coverage

### Coverage by Module

| Module | Lines | Missing | Coverage |
|--------|-------|---------|----------|
| src/app.py | 79 | 2 | 97% |
| src/tuomari.py | 25 | 1 | 96% |
| src/tekoaly_parannettu.py | 31 | 9 | 71% |
| src/kps_parempi_tekoaly.py | 10 | 0 | 100% |
| src/kps_tekoaly.py | 10 | 0 | 100% |
| **Overall** | **219** | **54** | **75%** |

### What's Covered

✅ All Flask routes and endpoints
✅ All API endpoints (play and status)
✅ WebGame class and wrapper logic
✅ Game result determination
✅ Score tracking
✅ History recording
✅ Input validation
✅ Error handling
✅ Template rendering
✅ AI functionality
✅ Session management

### Not Covered

- CLI entry point (index.py) - separate from web UI
- Game factory functions - used transitively
- Some AI decision trees

## Test Fixtures

### client
Flask test client with testing mode enabled.

### runner
Flask CLI runner for command testing.

### clear_sessions
Auto-use fixture that clears game sessions between tests.

### web_game_pvp
WebGame instance for Player vs Player mode.

### web_game_ai
WebGame instance for Player vs AI mode.

### web_game_enhanced_ai
WebGame instance for Player vs Enhanced AI mode.

## Running Tests in CI/CD

### Requirements
```bash
poetry install  # Installs pytest and dependencies
```

### Basic test run
```bash
poetry run pytest tests/
```

### With coverage
```bash
poetry run pytest tests/ --cov=src --cov-report=xml
```

### Exit codes
- 0: All tests passed
- 1: One or more tests failed
- 2: Test execution was interrupted
- 3: Internal pytest error
- 4: pytest command line usage error
- 5: No tests collected

## Key Testing Patterns

### 1. Session-based testing
Each test that uses API endpoints starts with a game session via `GET /game/<mode>`.

### 2. JSON validation
API responses are parsed and fields validated for correct types and values.

### 3. Move validation
All valid moves (k, p, s) tested individually and in combinations.

### 4. Score integrity
Tests verify scores don't reset and accumulate correctly.

### 5. AI consistency
Multiple runs ensure AI returns valid moves in all cases.

## Troubleshooting

### Tests fail with "Module not found"
```bash
# Ensure dependencies are installed
poetry install
```

### Coverage report shows 0%
```bash
# The app module needs to be imported during tests
# This happens automatically - try running again
poetry run pytest tests/ --cov=src --cov-report=term-missing
```

### Session-related test failures
```bash
# conftest.py fixture clears sessions automatically
# If issues persist, check that clear_sessions fixture is marked autouse=True
```

### Import errors from src modules
```bash
# conftest.py adds src to Python path
# If issues persist, verify PYTHONPATH includes the src directory
export PYTHONPATH="${PYTHONPATH}:./src"
poetry run pytest tests/
```

## Performance

- All 75 tests complete in ~0.1-0.4 seconds
- Fast enough for pre-commit hooks
- Suitable for continuous integration

## Maintenance

### Adding new tests
1. Create test method in appropriate test file
2. Follow naming convention: `test_<what_is_being_tested>`
3. Use existing fixtures from conftest.py
4. Add docstring explaining test purpose
5. Run `poetry run pytest tests/` to verify

### Updating fixtures
1. Modify fixture in `tests/conftest.py`
2. Run all tests to ensure backward compatibility
3. Update documentation

### Code coverage goals
- Aim for >90% coverage on app.py
- Document any intentional uncovered code
- Regular coverage reviews
