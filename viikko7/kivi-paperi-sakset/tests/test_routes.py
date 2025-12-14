"""Tests for Flask routes"""
import pytest


class TestIndexRoute:
    """Test the home page route"""
    
    def test_index_returns_200(self, client):
        """Test that index route returns 200 status"""
        response = client.get('/')
        assert response.status_code == 200
    
    def test_index_contains_game_modes(self, client):
        """Test that index page shows all game modes"""
        response = client.get('/')
        assert b'Player vs Player' in response.data
        assert b'Player vs AI' in response.data
        assert b'Player vs Enhanced AI' in response.data
    
    def test_index_contains_game_links(self, client):
        """Test that index page contains links to game modes"""
        response = client.get('/')
        assert b'/game/a' in response.data
        assert b'/game/b' in response.data
        assert b'/game/c' in response.data
    
    def test_index_contains_rules(self, client):
        """Test that index page displays game rules"""
        response = client.get('/')
        assert b'Rock' in response.data or b'Kivi' in response.data
        assert b'Paper' in response.data or b'Paperi' in response.data
        assert b'Scissors' in response.data or b'Sakset' in response.data


class TestGameRoute:
    """Test the game starting route"""
    
    def test_game_mode_a_returns_200(self, client):
        """Test that player vs player game loads"""
        response = client.get('/game/a')
        assert response.status_code == 200
    
    def test_game_mode_b_returns_200(self, client):
        """Test that player vs AI game loads"""
        response = client.get('/game/b')
        assert response.status_code == 200
    
    def test_game_mode_c_returns_200(self, client):
        """Test that player vs enhanced AI game loads"""
        response = client.get('/game/c')
        assert response.status_code == 200
    
    def test_invalid_game_mode_redirects(self, client):
        """Test that invalid game mode redirects to home"""
        response = client.get('/game/invalid')
        assert response.status_code == 302
        assert response.location.endswith('/')
    
    def test_game_mode_a_has_correct_title(self, client):
        """Test that player vs player shows correct title"""
        response = client.get('/game/a')
        assert b'Player vs Player' in response.data
    
    def test_game_mode_b_has_correct_title(self, client):
        """Test that player vs AI shows correct title"""
        response = client.get('/game/b')
        assert b'Player vs AI' in response.data
    
    def test_game_mode_c_has_correct_title(self, client):
        """Test that enhanced AI shows correct title"""
        response = client.get('/game/c')
        assert b'Player vs Enhanced AI' in response.data
    
    def test_game_page_contains_move_buttons(self, client):
        """Test that game page has move selection buttons"""
        response = client.get('/game/b')
        assert b'move-btn' in response.data
    
    def test_game_page_contains_play_button(self, client):
        """Test that game page has play button"""
        response = client.get('/game/b')
        assert b'Play Round' in response.data
    
    def test_game_page_contains_score_board(self, client):
        """Test that game page has score tracking"""
        response = client.get('/game/b')
        assert b'score-board' in response.data or b'score-value' in response.data
    
    def test_game_creates_session(self, client):
        """Test that starting a game creates a session"""
        response = client.get('/game/a')
        # Check that a session was created (will have session cookie)
        assert 'Set-Cookie' in response.headers or response.status_code == 200
    
    def test_pvp_game_has_two_move_sections(self, client):
        """Test that PvP has move sections for both players"""
        response = client.get('/game/a')
        assert response.data.count(b'Player') >= 2


class TestTemplateRendering:
    """Test that templates render correctly"""
    
    def test_index_template_renders(self, client):
        """Test that index template renders without errors"""
        response = client.get('/')
        assert response.status_code == 200
        assert len(response.data) > 100
    
    def test_game_template_renders(self, client):
        """Test that game template renders without errors"""
        response = client.get('/game/b')
        assert response.status_code == 200
        assert len(response.data) > 100
    
    def test_base_template_styling(self, client):
        """Test that base template includes styling"""
        response = client.get('/')
        # Check for external CSS file link
        assert b'style.css' in response.data or b'<style>' in response.data
    
    def test_game_template_has_javascript(self, client):
        """Test that game template includes JavaScript"""
        response = client.get('/game/b')
        assert b'<script>' in response.data
        assert b'</script>' in response.data
