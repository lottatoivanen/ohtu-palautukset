import requests
from player import Player

def main():
    url = "https://studies.cs.helsinki.fi/nhlstats/2024-25/players"
    response = requests.get(url).json()

    players = [Player(player_dict) for player_dict in response]
    psorted = sorted(players, key=lambda p: p.assists + p.goals, reverse=True)
    nationality = "FIN"
    chosen = [p for p in psorted if p.nationality == nationality]

    print(f"Players from {nationality}:")

    for player in chosen:
        print(player)

if __name__ == "__main__":
    main()
