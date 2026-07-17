import os
import requests
import psycopg2
import time
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("FOOTBALL_API_KEY")

HEADERS = {
    "X-Auth-Token": API_KEY
}

conn = psycopg2.connect(
    dbname="football_data",
    user="postgres",
    password=os.getenv("POSTGRES_PASSWORD"),
    host="localhost",
    port="5432"
)

try:
    cursor = conn.cursor()

    cursor.execute('SELECT id, code FROM "League"')
    leagues = cursor.fetchall()

    stats_count = 0

    for league_id, league_code in leagues:

        print(f"Processing {league_code}...")

        response = requests.get(
            f"https://api.football-data.org/v4/competitions/{league_code}/standings",
            headers=HEADERS,
            timeout=30
        )
        time.sleep(6)

        if response.status_code != 200:
            print(
                f"Failed to fetch standings for "
                f"{league_code}: {response.status_code}"
            )
            continue

        data = response.json()

        season = data["season"]["startDate"][:4]

        standings = data["standings"][0]["table"]

        for team_data in standings:

            team_id = team_data["team"]["id"]
            team_name = team_data["team"]["name"]

            # Ensure team exists
            cursor.execute(
                'SELECT 1 FROM "Team" WHERE id = %s',
                (team_id,)
            )

            if cursor.fetchone() is None:

                print(
                    f"Adding missing team: "
                    f"{team_name} ({team_id})"
                )

                cursor.execute(
                    '''
                    INSERT INTO "Team"
                    (id, name, "leagueId")
                    VALUES (%s, %s, %s)
                    ON CONFLICT (id) DO NOTHING
                    ''',
                    (
                        team_id,
                        team_name,
                        league_id
                    )
                )

            cursor.execute(
                """
                INSERT INTO "SeasonStats"
                (
                    season,
                    "matchesPlayed",
                    wins,
                    draws,
                    losses,
                    "goalsFor",
                    "goalsAgainst",
                    points,
                    "teamId"
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)

                ON CONFLICT ("teamId", season)
                DO UPDATE SET
                    "matchesPlayed" = EXCLUDED."matchesPlayed",
                    wins = EXCLUDED.wins,
                    draws = EXCLUDED.draws,
                    losses = EXCLUDED.losses,
                    "goalsFor" = EXCLUDED."goalsFor",
                    "goalsAgainst" = EXCLUDED."goalsAgainst",
                    points = EXCLUDED.points
                """,
                (
                    season,
                    team_data["playedGames"],
                    team_data["won"],
                    team_data["draw"],
                    team_data["lost"],
                    team_data["goalsFor"],
                    team_data["goalsAgainst"],
                    team_data["points"],
                    team_id
                )
            )

            stats_count += 1

        print(f"Imported standings for {league_code}")

    conn.commit()

    print(f"{stats_count} season stat rows processed.")

finally:
    cursor.close()
    conn.close()

print("Season statistics import completed.")