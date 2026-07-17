import subprocess

subprocess.run(["python", "scripts/import_leagues.py"])
subprocess.run(["python", "scripts/import_teams.py"])
subprocess.run(["python", "scripts/import_season_stats.py"])

print("Pipeline completed.")