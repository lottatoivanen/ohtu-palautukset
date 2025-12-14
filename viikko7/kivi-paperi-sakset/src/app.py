from flask import Flask, render_template, request, session, redirect, url_for
import sys
import os

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(__file__))

from kps_pelaaja_vs_pelaaja import KPSPelaajaVsPelaaja
from kps_tekoaly import KPSTekoaly
from kps_parempi_tekoaly import KPSParempiTekoaly
from tuomari import Tuomari

app = Flask(__name__)
app.secret_key = 'kivi_paperi_sakset_secret'

# Game sessions storage
game_sessions = {}


class WebGame:
    """Wrapper for web-based game sessions"""
    WINNING_SCORE = 3  # First player to reach 3 wins ends the game
    
    def __init__(self, game_type):
        self.game_type = game_type
        if game_type == 'a':
            self.game = KPSPelaajaVsPelaaja()
        elif game_type == 'b':
            self.game = KPSTekoaly()
        elif game_type == 'c':
            self.game = KPSParempiTekoaly()
        self.tuomari = Tuomari()
        self.history = []
        self.game_over = False
        self.winner = None  # 'player1', 'player2', or None
    
    def play_round(self, first_move):
        """Play a single round"""
        if not self._is_valid_move(first_move):
            return {"error": "Invalid move", "valid": False}
        
        if self.game_over:
            return {"error": "Game is over", "valid": False, "game_over": True}
        
        # Get second player's move
        if self.game_type == 'a':
            # For player vs player, we need to get input from web form
            return {"waiting_for_second": True}
        else:
            # For AI games, get computer move
            second_move = self.game._toisen_siirto(first_move)
            self.tuomari.kirjaa_siirto(first_move, second_move)
            
            # Check for game over
            self._check_game_over()
            
            result = {
                "first_move": first_move,
                "second_move": second_move,
                "first_score": self.tuomari.ekan_pisteet,
                "second_score": self.tuomari.tokan_pisteet,
                "draws": self.tuomari.tasapelit,
                "valid": True,
                "game_over": self.game_over,
                "winner": self.winner
            }
            self.history.append(result)
            return result
    
    def play_round_pvp(self, first_move, second_move):
        """Play a round for player vs player"""
        if not self._is_valid_move(first_move) or not self._is_valid_move(second_move):
            return {"error": "Invalid move", "valid": False}
        
        if self.game_over:
            return {"error": "Game is over", "valid": False, "game_over": True}
        
        self.tuomari.kirjaa_siirto(first_move, second_move)
        
        # Check for game over
        self._check_game_over()
        
        result = {
            "first_move": first_move,
            "second_move": second_move,
            "first_score": self.tuomari.ekan_pisteet,
            "second_score": self.tuomari.tokan_pisteet,
            "draws": self.tuomari.tasapelit,
            "valid": True,
            "game_over": self.game_over,
            "winner": self.winner
        }
        self.history.append(result)
        return result
    
    def _check_game_over(self):
        """Check if the game should end"""
        if self.tuomari.ekan_pisteet >= self.WINNING_SCORE:
            self.game_over = True
            self.winner = 'player1'
        elif self.tuomari.tokan_pisteet >= self.WINNING_SCORE:
            self.game_over = True
            self.winner = 'player2'
    
    def _is_valid_move(self, move):
        """Check if move is valid"""
        return move in ['k', 'p', 's']
    
    def get_status(self):
        """Get current game status"""
        return {
            "first_score": self.tuomari.ekan_pisteet,
            "second_score": self.tuomari.tokan_pisteet,
            "draws": self.tuomari.tasapelit,
            "history": self.history,
            "game_over": self.game_over,
            "winner": self.winner
        }


@app.route('/')
def index():
    """Home page - game mode selection"""
    return render_template('index.html')


@app.route('/game/<mode>')
def game(mode):
    """Start a new game with the selected mode"""
    if mode not in ['a', 'b', 'c']:
        return redirect(url_for('index'))
    
    session_id = os.urandom(16).hex()
    session['game_session'] = session_id
    session['game_mode'] = mode
    session['round'] = 0
    
    web_game = WebGame(mode)
    game_sessions[session_id] = web_game
    
    mode_names = {
        'a': 'Player vs Player',
        'b': 'Player vs AI',
        'c': 'Player vs Enhanced AI'
    }
    
    return render_template('game.html', mode=mode, mode_name=mode_names[mode])


@app.route('/api/play', methods=['POST'])
def play_move():
    """Handle a game move"""
    data = request.get_json() or {}
    first_move = (data.get('first_move') or '').strip().lower()
    second_move = (data.get('second_move') or '').strip().lower()
    
    session_id = session.get('game_session')
    if not session_id or session_id not in game_sessions:
        return {"error": "Game session not found"}, 400
    
    game = game_sessions[session_id]
    game_mode = session.get('game_mode')
    
    if game_mode == 'a':
        # Player vs Player
        result = game.play_round_pvp(first_move, second_move)
    else:
        # Player vs AI
        result = game.play_round(first_move)
    
    return result


@app.route('/api/status')
def status():
    """Get current game status"""
    session_id = session.get('game_session')
    if not session_id or session_id not in game_sessions:
        return {"error": "Game session not found"}, 400
    
    game = game_sessions[session_id]
    return game.get_status()


if __name__ == '__main__':
    app.run(debug=False, port=5000, use_reloader=False)
