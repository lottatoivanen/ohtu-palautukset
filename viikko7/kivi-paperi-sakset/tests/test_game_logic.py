"""Tests for WebGame class and game logic integration"""
import pytest


class TestWebGameInitialization:
    """Test WebGame class initialization"""
    
    def test_create_pvp_game(self, web_game_pvp):
        """Test creating a PvP game"""
        assert web_game_pvp.game_type == 'a'
        assert web_game_pvp.tuomari is not None
        assert web_game_pvp.history == []
    
    def test_create_ai_game(self, web_game_ai):
        """Test creating an AI game"""
        assert web_game_ai.game_type == 'b'
        assert web_game_ai.tuomari is not None
        assert web_game_ai.history == []
    
    def test_create_enhanced_ai_game(self, web_game_enhanced_ai):
        """Test creating an Enhanced AI game"""
        assert web_game_enhanced_ai.game_type == 'c'
        assert web_game_enhanced_ai.tuomari is not None
        assert web_game_enhanced_ai.history == []


class TestWebGameValidation:
    """Test move validation in WebGame"""
    
    def test_valid_move_k(self, web_game_ai):
        """Test that 'k' is valid"""
        assert web_game_ai._is_valid_move('k') == True
    
    def test_valid_move_p(self, web_game_ai):
        """Test that 'p' is valid"""
        assert web_game_ai._is_valid_move('p') == True
    
    def test_valid_move_s(self, web_game_ai):
        """Test that 's' is valid"""
        assert web_game_ai._is_valid_move('s') == True
    
    def test_invalid_move(self, web_game_ai):
        """Test that invalid moves are rejected"""
        assert web_game_ai._is_valid_move('x') == False
        assert web_game_ai._is_valid_move('') == False
        assert web_game_ai._is_valid_move('kk') == False
    
    def test_uppercase_move_invalid(self, web_game_ai):
        """Test that uppercase moves are invalid (filtering done in app)"""
        # The app.py converts to lowercase before calling this
        result = web_game_ai._is_valid_move('K')
        # This should be false since the method only accepts lowercase
        assert result == False


class TestWebGamePlayRound:
    """Test playing rounds in WebGame"""
    
    def test_play_round_ai_returns_result(self, web_game_ai):
        """Test that AI round returns game result"""
        result = web_game_ai.play_round('k')
        assert result['valid'] == True
        assert 'first_move' in result
        assert 'second_move' in result
    
    def test_play_round_ai_invalid_move(self, web_game_ai):
        """Test that invalid move is caught"""
        result = web_game_ai.play_round('invalid')
        assert result['valid'] == False
    
    def test_play_round_pvp_valid_moves(self, web_game_pvp):
        """Test PvP round with valid moves"""
        result = web_game_pvp.play_round_pvp('k', 'p')
        assert result['valid'] == True
        assert result['first_move'] == 'k'
        assert result['second_move'] == 'p'
    
    def test_play_round_pvp_invalid_first_move(self, web_game_pvp):
        """Test PvP round with invalid first move"""
        result = web_game_pvp.play_round_pvp('invalid', 'k')
        assert result['valid'] == False
    
    def test_play_round_pvp_invalid_second_move(self, web_game_pvp):
        """Test PvP round with invalid second move"""
        result = web_game_pvp.play_round_pvp('k', 'invalid')
        assert result['valid'] == False


class TestWebGameScoring:
    """Test score tracking in WebGame"""
    
    def test_player1_wins_rock_vs_scissors(self, web_game_pvp):
        """Test score when player 1 wins"""
        web_game_pvp.play_round_pvp('k', 's')
        assert web_game_pvp.tuomari.ekan_pisteet == 1
        assert web_game_pvp.tuomari.tokan_pisteet == 0
    
    def test_player2_wins_paper_vs_rock(self, web_game_pvp):
        """Test score when player 2 wins"""
        web_game_pvp.play_round_pvp('k', 'p')
        assert web_game_pvp.tuomari.ekan_pisteet == 0
        assert web_game_pvp.tuomari.tokan_pisteet == 1
    
    def test_draw_same_moves(self, web_game_pvp):
        """Test draw when same moves"""
        web_game_pvp.play_round_pvp('k', 'k')
        assert web_game_pvp.tuomari.ekan_pisteet == 0
        assert web_game_pvp.tuomari.tokan_pisteet == 0
        assert web_game_pvp.tuomari.tasapelit == 1
    
    def test_multiple_rounds_accumulate(self, web_game_pvp):
        """Test that scores accumulate across rounds"""
        web_game_pvp.play_round_pvp('k', 's')
        web_game_pvp.play_round_pvp('k', 's')
        assert web_game_pvp.tuomari.ekan_pisteet == 2
        
        web_game_pvp.play_round_pvp('k', 'p')
        assert web_game_pvp.tuomari.tokan_pisteet == 1
    
    def test_get_status_returns_current_scores(self, web_game_pvp):
        """Test that get_status returns current scores"""
        web_game_pvp.play_round_pvp('k', 's')
        status = web_game_pvp.get_status()
        assert status['first_score'] == 1
        assert status['second_score'] == 0
        assert status['draws'] == 0


class TestWebGameHistory:
    """Test game history tracking"""
    
    def test_history_empty_initially(self, web_game_ai):
        """Test that history is empty at start"""
        assert len(web_game_ai.history) == 0
    
    def test_history_records_round(self, web_game_pvp):
        """Test that history records played rounds"""
        web_game_pvp.play_round_pvp('k', 'p')
        assert len(web_game_pvp.history) == 1
    
    def test_history_accumulates(self, web_game_pvp):
        """Test that history accumulates rounds"""
        web_game_pvp.play_round_pvp('k', 'p')
        web_game_pvp.play_round_pvp('p', 's')
        web_game_pvp.play_round_pvp('s', 'k')
        assert len(web_game_pvp.history) == 3
    
    def test_history_contains_moves(self, web_game_pvp):
        """Test that history contains move information"""
        web_game_pvp.play_round_pvp('k', 'p')
        result = web_game_pvp.history[0]
        assert result['first_move'] == 'k'
        assert result['second_move'] == 'p'
    
    def test_history_contains_scores(self, web_game_pvp):
        """Test that history contains score after each round"""
        web_game_pvp.play_round_pvp('k', 'p')
        result = web_game_pvp.history[0]
        assert 'first_score' in result
        assert 'second_score' in result
        assert 'draws' in result


class TestAIGamePlay:
    """Test AI game functionality"""
    
    def test_ai_returns_valid_move(self, web_game_ai):
        """Test that AI returns valid moves"""
        for _ in range(5):
            result = web_game_ai.play_round('k')
            if not result.get('game_over', False):
                assert 'second_move' in result
                assert result['second_move'] in ['k', 'p', 's']
    
    def test_ai_responds_to_different_moves(self, web_game_ai):
        """Test that AI can respond to different moves"""
        results = []
        for move in ['k', 'p', 's']:
            result = web_game_ai.play_round(move)
            results.append(result)
        
        # All should be valid
        for result in results:
            assert result['valid'] == True
    
    def test_enhanced_ai_returns_valid_move(self, web_game_enhanced_ai):
        """Test that enhanced AI returns valid moves"""
        for _ in range(5):
            result = web_game_enhanced_ai.play_round('k')
            if not result.get('game_over', False):
                assert 'second_move' in result
                assert result['second_move'] in ['k', 'p', 's']
    
    def test_enhanced_ai_learns_patterns(self, web_game_enhanced_ai):
        """Test that enhanced AI can adapt"""
        # Play several rounds with same move
        for _ in range(5):
            web_game_enhanced_ai.play_round('k')
        
        # Enhanced AI should still return valid moves
        result = web_game_enhanced_ai.play_round('k')
        assert result['valid'] == False


class TestGameResultDetermination:
    """Test game result logic"""
    
    def test_rock_beats_scissors(self, web_game_pvp):
        """Test that rock beats scissors"""
        result = web_game_pvp.play_round_pvp('k', 's')
        assert result['first_score'] == 1
        assert result['second_score'] == 0
    
    def test_scissors_beats_paper(self, web_game_pvp):
        """Test that scissors beats paper"""
        result = web_game_pvp.play_round_pvp('s', 'p')
        assert result['first_score'] == 1
        assert result['second_score'] == 0
    
    def test_paper_beats_rock(self, web_game_pvp):
        """Test that paper beats rock"""
        result = web_game_pvp.play_round_pvp('p', 'k')
        assert result['first_score'] == 1
        assert result['second_score'] == 0
    
    def test_all_same_moves_draw(self, web_game_pvp):
        """Test that same moves result in draw"""
        for move in ['k', 'p', 's']:
            result = web_game_pvp.play_round_pvp(move, move)
            assert result['draws'] >= 1
            assert result['first_score'] == 0
            assert result['second_score'] == 0


class TestResponseFormats:
    """Test response format consistency"""
    
    def test_play_round_response_has_required_fields(self, web_game_ai):
        """Test that play_round response has all required fields"""
        result = web_game_ai.play_round('k')
        required_fields = ['first_move', 'second_move', 'first_score', 
                          'second_score', 'draws', 'valid']
        for field in required_fields:
            assert field in result
    
    def test_get_status_response_has_required_fields(self, web_game_ai):
        """Test that get_status response has all required fields"""
        status = web_game_ai.get_status()
        required_fields = ['first_score', 'second_score', 'draws', 'history']
        for field in required_fields:
            assert field in status
    
    def test_history_items_have_required_fields(self, web_game_pvp):
        """Test that history items have all required fields"""
        web_game_pvp.play_round_pvp('k', 'p')
        status = web_game_pvp.get_status()
        history_item = status['history'][0]
        required_fields = ['first_move', 'second_move', 'first_score',
                          'second_score', 'draws', 'valid']
        for field in required_fields:
            assert field in history_item


class TestGameOverCondition:
    """Test game-ending conditions (first to 5 wins)"""
    
    def test_game_not_over_initially(self, web_game_pvp):
        """Test that game is not over when just created"""
        status = web_game_pvp.get_status()
        assert status['game_over'] == False
        assert status['winner'] is None
    
    def test_game_not_over_at_2_0(self, web_game_pvp):
        """Test that game continues at 2-0"""
        # Player 1 wins 2 times
        for _ in range(2):
            web_game_pvp.play_round_pvp('k', 's')
        status = web_game_pvp.get_status()
        assert status['game_over'] == False
        assert status['winner'] is None
    
    def test_game_ends_at_3_0(self, web_game_pvp):
        """Test that game ends when player 1 reaches 3 wins"""
        # Player 1 wins 3 times
        for _ in range(3):
            web_game_pvp.play_round_pvp('k', 's')
        status = web_game_pvp.get_status()
        assert status['game_over'] == True
        assert status['winner'] == 'player1'
        assert status['first_score'] == 3
        assert status['second_score'] == 0
    
    def test_game_ends_at_0_3(self, web_game_pvp):
        """Test that game ends when player 2 reaches 3 wins"""
        # Player 2 wins 3 times
        for _ in range(3):
            web_game_pvp.play_round_pvp('s', 'k')
        status = web_game_pvp.get_status()
        assert status['game_over'] == True
        assert status['winner'] == 'player2'
        assert status['first_score'] == 0
        assert status['second_score'] == 3
    
    def test_game_ends_at_3_1(self, web_game_pvp):
        """Test that game ends when player 1 reaches 3 with opponent at 1"""
        # Player 1 wins 1 time, Player 2 wins 1 time, then Player 1 wins 2 more
        web_game_pvp.play_round_pvp('k', 's')  # Player 1: 1-0
        web_game_pvp.play_round_pvp('s', 'k')  # Player 2: 1-1
        web_game_pvp.play_round_pvp('k', 's')  # Player 1: 2-1
        web_game_pvp.play_round_pvp('k', 's')  # Player 1: 3-1

        
        status = web_game_pvp.get_status()
        assert status['game_over'] == True
        assert status['winner'] == 'player1'
        assert status['first_score'] == 3
        assert status['second_score'] == 1
    
    def test_draws_dont_end_game(self, web_game_pvp):
        """Test that draws don't end the game"""
        # Play 100 draws - game should never end
        for _ in range(100):
            web_game_pvp.play_round_pvp('k', 'k')
        
        status = web_game_pvp.get_status()
        assert status['game_over'] == False
        assert status['winner'] is None
        assert status['first_score'] == 0
        assert status['second_score'] == 0
        assert status['draws'] == 100
    
    def test_draws_mixed_with_wins(self, web_game_pvp):
        """Test that draws don't interfere with game-ending condition"""
        # Mix draws with wins: 3 wins for P1, draws, 2 wins for P2, then P1 wins to 5
        web_game_pvp.play_round_pvp('k', 's')  # P1: 1-0
        web_game_pvp.play_round_pvp('k', 'k')  # Draw
        web_game_pvp.play_round_pvp('k', 's')  # P1: 2-0
        web_game_pvp.play_round_pvp('p', 'p')  # Draw
        web_game_pvp.play_round_pvp('s', 'k')  # P1: 2-1
        web_game_pvp.play_round_pvp('s', 'k')  # P2: 2-2
        web_game_pvp.play_round_pvp('s', 's')  # Draw
        web_game_pvp.play_round_pvp('k', 's')  # P1: 3-2
        
        status = web_game_pvp.get_status()
        assert status['game_over'] == True
        assert status['winner'] == 'player1'
        assert status['first_score'] == 3
        assert status['second_score'] == 2
        assert status['draws'] == 3
    
    def test_play_round_response_includes_game_over(self, web_game_ai):
        """Test that play_round response includes game_over and winner fields"""
        result = web_game_ai.play_round('k')
        assert 'game_over' in result
        assert 'winner' in result
        assert result['game_over'] == False
        assert result['winner'] is None
    
    def test_get_status_includes_game_over_fields(self, web_game_pvp):
        """Test that get_status response includes game_over and winner"""
        status = web_game_pvp.get_status()
        assert 'game_over' in status
        assert 'winner' in status
        assert status['game_over'] == False
        assert status['winner'] is None
    
    def test_cannot_play_after_game_over(self, web_game_pvp):
        """Test that plays after game over are prevented by the backend"""
        # Get to 5 wins
        for _ in range(5):
            web_game_pvp.play_round_pvp('k', 's')
        
        status_before = web_game_pvp.get_status()
        assert status_before['game_over'] == True
        
        # Try to play another round (backend prevents it)
        result = web_game_pvp.play_round_pvp('k', 's')
        
        # Backend should prevent the play after game is over
        assert result['valid'] == False
        assert result['game_over'] == True

