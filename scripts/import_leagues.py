import os
import requests
import psycopg2
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("FOOTBALL_API_KEY")

headers = {
    "X-Auth-Token": API_KEY
}

conn = psycopg2.connect(
    dbname="football_data",
    user="postgres",
    password=os.getenv("POSTGRES_PASSWORD"),
    host="localhost",
    port="5432"
)

cursor = conn.cursor()

response = requests.get(
    "https://api.football-data.org/v4/competitions",
    headers=headers
)

data = response.json()

TARGET_LEAGUES = {
    "PL",
    "PD",
    "SA",
    "BL1",
    "FL1",
    "PPL",
    "DED"
}

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

conn.commit()

cursor.close()
conn.close()

print("Leagues imported.")