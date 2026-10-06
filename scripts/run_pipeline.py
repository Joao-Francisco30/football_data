import sys

import import_leagues
import import_season_stats
import import_teams

STEPS = [
    ("leagues", import_leagues.main),
    ("teams", import_teams.main),
    ("season stats", import_season_stats.main),
]


def main():
    for name, step in STEPS:
        print(f"\n=== Importing {name} ===")
        step()

    print("\nPipeline completed.")


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(f"\nPipeline failed: {error}", file=sys.stderr)
        sys.exit(1)
