from statistics import Statistics
from player_reader import PlayerReader
from matchers import And, HasAtLeast, Not, PlaysIn, All, HasFewerThan, Or, QueryBuilder

def main():
    url = "https://studies.cs.helsinki.fi/nhlstats/2024-25/players.txt"
    reader = PlayerReader(url)
    stats = Statistics(reader)


    query = QueryBuilder()
    matcher = (
    query
        .one_of(
        query.plays_in("PHI")
            .has_at_least(10, "assists")
            .has_fewer_than(10, "goals"),
        query.plays_in("EDM")
            .has_at_least(50, "points")
        )
        .build()
    )

    for player in stats.matches(matcher):
        print(player)
    
    filtered_with_all = stats.matches(All())
    print(len(filtered_with_all))


if __name__ == "__main__":
    main()