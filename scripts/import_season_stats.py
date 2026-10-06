from utils import api
from utils.db import db_connection


def main():
    stats_count = 0
    failed = []

    with db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute('SELECT id, code FROM "League"')
            leagues = cursor.fetchall()

            if not leagues:
                raise RuntimeError("No leagues found. Run import_leagues.py first.")

            for league_id, league_code in leagues:
                print(f"Processing {league_code}...")

                response = api.get(f"/competitions/{league_code}/standings")

                if response.status_code != 200:
                    print(
                        f"Failed to fetch standings for "
                        f"{league_code}: {response.status_code}"
                    )
                    failed.append(league_code)
                    continue

                data = response.json()
                season = data["season"]["startDate"][:4]

                # The API also returns HOME and AWAY tables - we want the overall one.
                total = next(
                    (s for s in data["standings"] if s.get("type") == "TOTAL"),
                    None,
                )

                if total is None:
                    print(f"No TOTAL standings found for {league_code}")
                    failed.append(league_code)
                    continue

                for row in total["table"]:
                    team_id = row["team"]["id"]

                    # Make sure the team exists (import_teams normally creates it)
                    cursor.execute(
                        '''
                        INSERT INTO "Team" (id, name, "leagueId")
                        VALUES (%s, %s, %s)
                        ON CONFLICT (id) DO NOTHING
                        ''',
                        (team_id, row["team"]["name"], league_id),
                    )

                    cursor.execute(
                        '''
                        INSERT INTO "SeasonStats"
                            (season, "matchesPlayed", wins, draws, losses,
                             "goalsFor", "goalsAgainst", points, "teamId")
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                        ON CONFLICT ("teamId", season) DO UPDATE SET
                            "matchesPlayed" = EXCLUDED."matchesPlayed",
                            wins = EXCLUDED.wins,
                            draws = EXCLUDED.draws,
                            losses = EXCLUDED.losses,
                            "goalsFor" = EXCLUDED."goalsFor",
                            "goalsAgainst" = EXCLUDED."goalsAgainst",
                            points = EXCLUDED.points
                        ''',
                        (
                            season,
                            row["playedGames"],
                            row["won"],
                            row["draw"],
                            row["lost"],
                            row["goalsFor"],
                            row["goalsAgainst"],
                            row["points"],
                            team_id,
                        ),
                    )
                    stats_count += 1

                print(f"Imported standings for {league_code}")

    print(f"{stats_count} season stat rows processed.")

    if failed:
        raise RuntimeError(f"Standings could not be imported for: {', '.join(failed)}")


if __name__ == "__main__":
    main()
