import sys
import os
import pytest

# Add src directory to path so we can import game modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from app import app, game_sessions, WebGame


@pytest.fixture
def client():
    """Create a Flask test client"""
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test-secret-key'
    
    with app.test_client() as client:
        yield client


@pytest.fixture
def runner():
    """Create a Flask CLI runner"""
    return app.test_cli_runner()


@pytest.fixture(autouse=True)
def clear_sessions():
    """Clear game sessions before each test"""
    game_sessions.clear()
    yield
    game_sessions.clear()


@pytest.fixture
def app_context():
    """Provide app context for testing"""
    with app.app_context():
        yield app


@pytest.fixture
def web_game_pvp():
    """Create a Player vs Player game instance"""
    return WebGame('a')


@pytest.fixture
def web_game_ai():
    """Create a Player vs AI game instance"""
    return WebGame('b')


@pytest.fixture
def web_game_enhanced_ai():
    """Create a Player vs Enhanced AI game instance"""
    return WebGame('c')
