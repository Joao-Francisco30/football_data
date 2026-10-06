from utils import api
from utils.db import db_connection

TARGET_LEAGUES = {
    "PL",   # Premier League
    "PD",   # La Liga
    "SA",   # Serie A
    "BL1",  # Bundesliga
    "FL1",  # Ligue 1
    "PPL",  # Primeira Liga
    "DED",  # Eredivisie
}


def main():
    response = api.get("/competitions")

    if response.status_code != 200:
        raise RuntimeError(f"Leagues request failed: {response.status_code}")

    leagues = [
        competition
        for competition in response.json()["competitions"]
        if competition["code"] in TARGET_LEAGUES
    ]

    with db_connection() as conn:
        with conn.cursor() as cursor:
            for league in leagues:
                cursor.execute(
                    '''
                    INSERT INTO "League" (id, code, name, country)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (id) DO UPDATE SET
                        code = EXCLUDED.code,
                        name = EXCLUDED.name,
                        country = EXCLUDED.country
                    ''',
                    (
                        league["id"],
                        league["code"],
                        league["name"],
                        league["area"]["name"],
                    ),
                )

    print(f"{len(leagues)} leagues processed.")


if __name__ == "__main__":
    main()
