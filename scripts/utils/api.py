import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("FOOTBALL_API_KEY")

HEADERS = {
    "X-Auth-Token": API_KEY
}