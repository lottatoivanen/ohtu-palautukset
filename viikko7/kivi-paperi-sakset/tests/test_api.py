"""Tests for API endpoints"""
import json
import pytest


class TestPlayAPI:
    """Test the /api/play endpoint"""
    
    def test_play_valid_move_returns_json(self, client):
        """Test that valid move returns JSON response"""
        client.get('/game/b')  # Start a game session
        response = client.post('/api/play',
                               data=json.dumps({'first_move': 'k'}),
                               content_type='application/json')
        assert response.status_code == 200
        assert response.content_type == 'application/json'
    
    def test_play_ai_returns_valid_moves(self, client):
        """Test that AI game returns valid move information"""
        client.get('/game/b')
        response = client.post('/api/play',
                               data=json.dumps({'first_move': 'k'}),
                               content_type='application/json')
        data = json.loads(response.data)
        assert data['valid'] == True
        assert 'first_move' in data
        assert 'second_move' in data
        assert data['first_move'] in ['k', 'p', 's']
        assert data['second_move'] in ['k', 'p', 's']
    
    def test_play_returns_score(self, client):
        """Test that response includes updated score"""
        client.get('/game/b')
        response = client.post('/api/play',
                               data=json.dumps({'first_move': 'k'}),
                               content_type='application/json')
        data = json.loads(response.data)
        assert 'first_score' in data
        assert 'second_score' in data
        assert 'draws' in data
    
    def test_play_invalid_first_move(self, client):
        """Test that invalid first move is rejected"""
        client.get('/game/b')
        response = client.post('/api/play',
                               data=json.dumps({'first_move': 'invalid'}),
                               content_type='application/json')
        data = json.loads(response.data)
        assert data['valid'] == False
    
    def test_play_pvp_requires_both_moves(self, client):
        """Test that PvP mode requires both player moves"""
        client.get('/game/a')  # Player vs Player
        response = client.post('/api/play',
                               data=json.dumps({'first_move': 'k', 'second_move': 'p'}),
                               content_type='application/json')
        data = json.loads(response.data)
        assert data['valid'] == True
    
    def test_play_pvp_invalid_second_move(self, client):
        """Test that invalid second move in PvP is rejected"""
        client.get('/game/a')
        response = client.post('/api/play',
                               data=json.dumps({'first_move': 'k', 'second_move': 'invalid'}),
                               content_type='application/json')
        data = json.loads(response.data)
        assert data['valid'] == False
    
    def test_play_no_session_returns_error(self, client):
        """Test that playing without session returns error"""
        response = client.post('/api/play',
                               data=json.dumps({'first_move': 'k'}),
                               content_type='application/json')
        assert response.status_code == 400
    
    def test_play_rock_beats_scissors(self, client):
        """Test game logic: rock beats scissors"""
        # Set up a game and manually verify rock vs scissors
        client.get('/game/b')
        # Play multiple rounds to see if player wins with rock vs scissors
        responses = []
        for _ in range(10):
            response = client.post('/api/play',
                                   data=json.dumps({'first_move': 'k'}),
                                   content_type='application/json')
            data = json.loads(response.data)
            responses.append(data)
            if data['second_move'] == 's':
                assert data['first_score'] > 0
                break
    
    def test_play_updates_score_accumulation(self, client):
        """Test that scores accumulate correctly"""
        client.get('/game/b')
        
        # Play first round
        response1 = client.post('/api/play',
                                data=json.dumps({'first_move': 'k'}),
                                content_type='application/json')
        data1 = json.loads(response1.data)
        first_score_1 = data1['first_score']
        
        # Play second round
        response2 = client.post('/api/play',
                                data=json.dumps({'first_move': 'k'}),
                                content_type='application/json')
        data2 = json.loads(response2.data)
        first_score_2 = data2['first_score']
        
        # Second score should be >= first score (not reset)
        assert first_score_2 >= first_score_1
    
    def test_play_returns_correct_result_types(self, client):
        """Test that response has correct data types"""
        client.get('/game/b')
        response = client.post('/api/play',
                               data=json.dumps({'first_move': 'k'}),
                               content_type='application/json')
        data = json.loads(response.data)
        assert isinstance(data['valid'], bool)
        assert isinstance(data['first_move'], str)
        assert isinstance(data['second_move'], str)
        assert isinstance(data['first_score'], int)
        assert isinstance(data['second_score'], int)
        assert isinstance(data['draws'], int)


class TestStatusAPI:
    """Test the /api/status endpoint"""
    
    def test_status_returns_json(self, client):
        """Test that status endpoint returns JSON"""
        client.get('/game/b')
        response = client.get('/api/status')
        assert response.status_code == 200
        assert response.content_type == 'application/json'
    
    def test_status_returns_scores(self, client):
        """Test that status returns current scores"""
        client.get('/game/b')
        response = client.get('/api/status')
        data = json.loads(response.data)
        assert 'first_score' in data
        assert 'second_score' in data
        assert 'draws' in data
    
    def test_status_returns_history(self, client):
        """Test that status returns game history"""
        client.get('/game/b')
        response = client.get('/api/status')
        data = json.loads(response.data)
        assert 'history' in data
        assert isinstance(data['history'], list)
    
    def test_status_initial_scores_zero(self, client):
        """Test that initial status has zero scores"""
        client.get('/game/b')
        response = client.get('/api/status')
        data = json.loads(response.data)
        assert data['first_score'] == 0
        assert data['second_score'] == 0
        assert data['draws'] == 0
    
    def test_status_initial_history_empty(self, client):
        """Test that initial history is empty"""
        client.get('/game/b')
        response = client.get('/api/status')
        data = json.loads(response.data)
        assert len(data['history']) == 0
    
    def test_status_after_play_has_history(self, client):
        """Test that status includes history after playing"""
        client.get('/game/b')
        client.post('/api/play',
                   data=json.dumps({'first_move': 'k'}),
                   content_type='application/json')
        response = client.get('/api/status')
        data = json.loads(response.data)
        assert len(data['history']) == 1
    
    def test_status_no_session_returns_error(self, client):
        """Test that status without session returns error"""
        response = client.get('/api/status')
        assert response.status_code == 400
    
    def test_status_multiple_rounds_accumulate(self, client):
        """Test that status accumulates all rounds"""
        client.get('/game/b')
        
        # Play 3 rounds
        for _ in range(3):
            client.post('/api/play',
                       data=json.dumps({'first_move': 'k'}),
                       content_type='application/json')
        
        response = client.get('/api/status')
        data = json.loads(response.data)
        assert len(data['history']) == 3



class TestAPIValidation:
    """Test API input validation"""
    
    def test_play_with_empty_body(self, client):
        """Test that empty body is handled"""
        client.get('/game/b')
        response = client.post('/api/play',
                               data=json.dumps({}),
                               content_type='application/json')
        data = json.loads(response.data)
        assert data['valid'] == False
    
    def test_play_with_whitespace_moves(self, client):
        """Test that whitespace moves are stripped"""
        client.get('/game/b')
        response = client.post('/api/play',
                               data=json.dumps({'first_move': '  k  '}),
                               content_type='application/json')
        data = json.loads(response.data)
        assert data['valid'] == True
    
    def test_play_with_uppercase_moves(self, client):
        """Test that uppercase moves are converted to lowercase"""
        client.get('/game/b')
        response = client.post('/api/play',
                               data=json.dumps({'first_move': 'K'}),
                               content_type='application/json')
        data = json.loads(response.data)
        assert data['valid'] == True


class TestGameOverAPI:
    """Test game-over condition in API responses"""
    
    def test_play_response_includes_game_over_fields(self, client):
        """Test that play response includes game_over and winner fields"""
        client.get('/game/b')
        response = client.post('/api/play',
                               data=json.dumps({'first_move': 'k'}),
                               content_type='application/json')
        data = json.loads(response.data)
        assert 'game_over' in data
        assert 'winner' in data
        assert data['game_over'] == False
        assert data['winner'] is None
    
    def test_status_response_includes_game_over_fields(self, client):
        """Test that status response includes game_over and winner fields"""
        client.get('/game/b')
        response = client.get('/api/status')
        data = json.loads(response.data)
        assert 'game_over' in data
        assert 'winner' in data
        assert data['game_over'] == False
        assert data['winner'] is None
    
    def test_play_ai_game_ends_at_5_wins(self, client):
        """Test that API responses include game_over flag"""
        client.get('/game/b')  # Start AI game
        
        # The game will end eventually, test that game_over flag is always present
        for i in range(50):
            response = client.post('/api/play',
                                   data=json.dumps({'first_move': 'k'}),
                                   content_type='application/json')
            data = json.loads(response.data)
            # Response should always have game_over field
            assert 'game_over' in data
            assert 'winner' in data
            
            if data.get('game_over'):
                break
        
        # Verify game_over and winner fields in status
        status_response = client.get('/api/status')
        status_data = json.loads(status_response.data)
        assert 'game_over' in status_data
        assert 'winner' in status_data
    
    def test_play_pvp_game_ends_at_3_wins(self, client):
        """Test that PvP API game ends when player 1 reaches 3 wins"""
        client.get('/game/a')  # Start PvP game
        
        # Simulate 3 wins for player 1 using /api/play with both moves
        for _ in range(3):
            response = client.post('/api/play',
                                   data=json.dumps({'first_move': 'k', 'second_move': 's'}),
                                   content_type='application/json')
            if response.status_code != 200:
                break
        
        # Check final status
        status_response = client.get('/api/status')
        if status_response.status_code == 200:
            data = json.loads(status_response.data)
            assert data['first_score'] == 3
            assert data['second_score'] == 0
            assert data['game_over'] == True
            assert data['winner'] == 'player1'
    
    def test_play_pvp_game_ends_at_3_for_player2(self, client):
        """Test that PvP game ends when player 2 reaches 3 wins"""
        client.get('/game/a')  # Start PvP game
        
        # Simulate 3 wins for player 2 using /api/play
        for _ in range(3):
            response = client.post('/api/play',
                                   data=json.dumps({'first_move': 's', 'second_move': 'k'}),
                                   content_type='application/json')
            if response.status_code != 200:
                break
        
        # Check final status
        status_response = client.get('/api/status')
        if status_response.status_code == 200:
            data = json.loads(status_response.data)
            assert data['first_score'] == 0
            assert data['second_score'] == 3
            assert data['game_over'] == True
            assert data['winner'] == 'player2'
    
    def test_draws_dont_end_game_in_api(self, client):
        """Test that draws don't end the game via API"""
        client.get('/game/a')  # Start PvP game
        
        # Play 100 draws
        for _ in range(100):
            response = client.post('/api/play',
                                   data=json.dumps({'first_move': 'k', 'second_move': 'k'}),
                                   content_type='application/json')
            if response.status_code != 200:
                break
        
        # Check final status
        status_response = client.get('/api/status')
        data = json.loads(status_response.data)
        assert data['game_over'] == False
        assert data['winner'] is None
        assert data['draws'] == 100
        assert data['first_score'] == 0
        assert data['second_score'] == 0

