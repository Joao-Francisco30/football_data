from utils import api
from utils.db import db_connection


def main():
    imported_count = 0
    failed = []

    with db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute('SELECT id, code FROM "League"')
            leagues = cursor.fetchall()

            if not leagues:
                raise RuntimeError("No leagues found. Run import_leagues.py first.")

            for league_id, league_code in leagues:
                print(f"Importing teams from {league_code}...")

                response = api.get(f"/competitions/{league_code}/teams")

                if response.status_code != 200:
                    print(
                        f"Failed to get teams for {league_code}: "
                        f"{response.status_code}"
                    )
                    failed.append(league_code)
                    continue

                for team in response.json()["teams"]:
                    cursor.execute(
                        '''
                        INSERT INTO "Team"
                            (id, name, "shortName", founded, stadium, website, logo, "leagueId")
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                        ON CONFLICT (id) DO UPDATE SET
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
                            league_id,
                        ),
                    )
                    imported_count += 1

    print(f"{imported_count} teams processed.")

    if failed:
        raise RuntimeError(f"Teams could not be fetched for: {', '.join(failed)}")


if __name__ == "__main__":
    main()
