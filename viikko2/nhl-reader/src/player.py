class Player:
    def __init__(self, pdict):
        self.name = pdict['name']
        self.nationality = pdict['nationality']
        self.assists = pdict['assists']
        self.goals = pdict['goals']
        self.team = pdict['team']
        self.games = pdict['games']

    def get_score(self):
        return self.goals + self.assists

    def __str__(self):
        summa = self.assists + self.goals
        return f"{self.name:20} {self.team:15} {self.goals:2} + {self.assists:2} = {summa:2}"
