import os
import requests
import psycopg2
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("FOOTBALL_API_KEY")

HEADERS = {
    "X-Auth-Token": API_KEY
}

COMPETITIONS_URL = "https://api.football-data.org/v4/competitions"

TARGET_LEAGUES = {
    "PL",   # Premier League
    "PD",   # La Liga
    "SA",   # Serie A
    "BL1",  # Bundesliga
    "FL1",  # Ligue 1
    "PPL",  # Primeira Liga
    "DED"   # Eredivisie
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

    response = requests.get(
        COMPETITIONS_URL,
        headers=HEADERS
    )

    if response.status_code != 200:
        print(f"API request failed: {response.status_code}")
        exit()

    data = response.json()

    imported_count = 0

    for league in data["competitions"]:

        if league["code"] not in TARGET_LEAGUES:
            continue

        cursor.execute(
            '''
            INSERT INTO "League"
            (id, code, name, country)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING
            ''',
            (
                league["id"],
                league["code"],
                league["name"],
                league["area"]["name"]
            )
        )

        imported_count += 1

    conn.commit()

    print(f"{imported_count} leagues processed.")

finally:
    cursor.close()
    conn.close()

print("League import completed.")