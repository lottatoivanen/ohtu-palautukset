class TennisGame:
    SCORE_NAMES = {0: "Love", 1: "Fifteen", 2: "Thirty", 3: "Forty"}

    MIN_POINTS_FOR_WIN = 4
    MIN_LEAD_FOR_WIN = 2

    def __init__(self, player1_name, player2_name):
        self.player1_name = player1_name
        self.player2_name = player2_name
        self.player1_score = 0
        self.player2_score = 0

    def won_point(self, player_name):
        if player_name == "player1":
            self.player1_score = self.player1_score + 1
        else:
            self.player2_score = self.player2_score + 1

    def get_score(self):
        if self.game_tie():
            return self.tie_result()
        
        if self.game_win():
            return self.win_result()
        
        return self.game_score()
    
    def game_tie(self):
        return self.player1_score == self.player2_score
    
    def tie_result(self):
        if self.player1_score >= 3:
            return "Deuce"
        return f"{self.score_name(self.player1_score)}-All"
    
    def game_win(self):
        return (self.player1_score >= self.MIN_POINTS_FOR_WIN or self.player2_score >= self.MIN_POINTS_FOR_WIN)
    
    def win_result(self):
        difference = self.player1_score - self.player2_score

        if abs(difference) >= self.MIN_LEAD_FOR_WIN:
            winner = "player1" if difference > 0 else "player2"
            return f"Win for {winner}"

        advantage_player = "player1" if difference > 0 else "player2"
        return f"Advantage {advantage_player}"
    
    def score_name(self, points):
        return self.SCORE_NAMES.get(points, "Forty")
    
    def game_score(self):
        return f"{self.score_name(self.player1_score)}-{self.score_name(self.player2_score)}"


