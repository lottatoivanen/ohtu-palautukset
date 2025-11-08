class PlayerStats:
    def __init__(self, reader):
        self.reader = reader

    def top_scorers_by_nationality(self, nationality):
        players = self.reader.get_players()
        psorted = sorted(players, key=lambda p: p.assists + p.goals, reverse=True)
        chosen = [p for p in psorted if p.nationality == nationality]
        return chosen

    def least_scores_by_nationality(self, nationality):
        players = self.reader.get_players()
        psorted = sorted(players, key=lambda p: p.assists + p.goals, reverse=False)
        chosen = [p for p in psorted if p.nationality == nationality]
        return chosen
