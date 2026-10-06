import os
import time

import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://api.football-data.org/v4"

# Free tier allows 10 requests per minute -> keep calls at least 6.5s apart.
MIN_SECONDS_BETWEEN_CALLS = 6.5

_last_call = 0.0


def _headers():
    api_key = os.getenv("FOOTBALL_API_KEY")

    if not api_key:
        raise RuntimeError(
            "FOOTBALL_API_KEY is not set. Copy .env.example to .env and fill it in."
        )

    return {"X-Auth-Token": api_key}


def get(path, max_retries=3):
    """
    GET {BASE_URL}{path} with rate limiting, a timeout, and retries on HTTP 429.
    Returns the requests.Response (callers check status_code).
    """
    global _last_call

    url = f"{BASE_URL}{path}"

    for attempt in range(max_retries + 1):
        wait = MIN_SECONDS_BETWEEN_CALLS - (time.monotonic() - _last_call)
        if wait > 0:
            time.sleep(wait)

        response = requests.get(url, headers=_headers(), timeout=30)
        _last_call = time.monotonic()

        if response.status_code == 429 and attempt < max_retries:
            try:
                retry_after = int(response.headers.get("Retry-After", 60))
            except ValueError:
                retry_after = 60

            print(f"Rate limited. Waiting {retry_after}s before retrying...")
            time.sleep(retry_after)
            continue

        return response

    return response
