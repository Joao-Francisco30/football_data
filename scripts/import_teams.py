import os
import requests
import psycopg2
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

    imported_count = 0

    for league_id, league_code in leagues:

        print(f"Importing teams from {league_code}...")

        response = requests.get(
            f"https://api.football-data.org/v4/competitions/{league_code}/teams",
            headers=HEADERS,
            timeout=30
        )

        if response.status_code != 200:
            print(
                f"Failed to get teams for {league_code}: "
                f"{response.status_code}"
            )
            continue

        data = response.json()

        for team in data["teams"]:

            cursor.execute(
                '''
                INSERT INTO "Team"
                (
                    id,
                    name,
                    "shortName",
                    founded,
                    stadium,
                    website,
                    logo,
                    "leagueId"
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)

                ON CONFLICT (id)
                DO UPDATE SET
                    name = EXCLUDED.name,
                    "shortName" = EXCLUDED."shortName",
                    founded = EXCLUDED.founded,
                    stadium = EXCLUDED.stadium,
                    website = EXCLUDED.website,
                    logo = EXCLUDED.logo,
                    "leagueId" = EXCLUDED."leagueId"
                ''',
                (
                    team["id"],
                    team["name"],
                    team.get("shortName"),
                    team.get("founded"),
                    team.get("venue"),
                    team.get("website"),
                    team.get("crest"),
                    league_id
                )
            )

            imported_count += 1

    conn.commit()

    print(f"{imported_count} teams processed.")

finally:
    cursor.close()
    conn.close()

print("Team import completed.")