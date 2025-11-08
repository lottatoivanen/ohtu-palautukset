from rich import print
from rich.table import Table
from rich import box
from playerreader import PlayerReader
from playerstats import PlayerStats


seasons = ["2018-19", "2019-20", "2020-21", "2021-22", "2022-23", "2023-24", "2024-25", "2025-26"]

def choose_season():
    seasonstr = "/".join(seasons)
    while True:
        print(f"Season [[bright_magenta]{seasonstr}[/bright_magenta]]:")
        season = input().strip()
        if season not in seasons:
            print("Not a valid season. Please try again.")
        else:
            return season

def choose_nationality(reader):
    players = reader.get_players()
    nationalities = sorted({p.nationality for p in players})
    nationalitystr = "/".join(nationalities)
    while True:
        print(f"Nationality [[bright_magenta]{nationalitystr}[bright_magenta]]")
        nationality = input().strip().upper()
        if nationality not in nationalities:
            print("Not a valid nationality. Please try again.")
        else:
            return nationality

def table(players, season, nationality):
    t = Table(title = f"Season {season} players from {nationality}", box=box.SQUARE, header_style="bold white")
    t.add_column("Released")
    t.add_column("teams")
    t.add_column("goals")
    t.add_column("assists")
    t.add_column("points")

    for p in players:
        summa = p.goals + p.assists
        t.add_row(f"[bright_cyan]{p.name}[/bright_cyan]", f"[hot_pink]{p.team}[/hot_pink]", f"[violet]{p.goals}[/violet]", f"[violet]{p.assists}[/violet]", f"[violet]{summa}[/violet]")

    print(t)


def main():
    url = "https://studies.cs.helsinki.fi/nhlstats/"
    season = choose_season()


    chosenplayers = f"{url}{season}/players"
    reader = PlayerReader(chosenplayers)
    stats = PlayerStats(reader)

    nationality = choose_nationality(reader)

    players = stats.top_scorers_by_nationality(nationality)

    table(players, season, nationality)



if __name__ == "__main__":
    main()
