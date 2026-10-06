# Football Data Dashboard

A football analytics dashboard: a Python pipeline imports data from
[football-data.org](https://www.football-data.org) into PostgreSQL, and a
Next.js app (Prisma + TypeScript + Tailwind) displays it.

Covers: Premier League, La Liga, Serie A, Bundesliga, Ligue 1, Primeira Liga, Eredivisie.

## Setup

```bash
npm install                  # also runs `prisma generate`
cp .env.example .env         # fill in DATABASE_URL and FOOTBALL_API_KEY
npx prisma migrate deploy    # create the tables
pip install -r scripts/requirements.txt
python scripts/run_pipeline.py   # import leagues, teams and standings (~2 min)
npm run dev
```

Open [http://localhost:3000](http://localhost:3000).

## Pages

- `/` – list of leagues
- `/league/[code]` – current standings for a league (e.g. `/league/PL`)

## Data pipeline

`scripts/run_pipeline.py` runs, in order: `import_leagues.py`, `import_teams.py`,
`import_season_stats.py`. It respects the API's free-tier rate limit (10 requests/minute),
so a full run takes about two minutes. Each script can also be run on its own.

`.github/workflows/update-data.yml` re-runs the pipeline daily. It needs the
repository secrets `DATABASE_URL` and `FOOTBALL_API_KEY`.

## Deploying

1. Create a hosted PostgreSQL database and put its connection string in `DATABASE_URL`.
2. Run `npx prisma migrate deploy` and `python scripts/run_pipeline.py` once against it.
3. Deploy to Vercel with `DATABASE_URL` set as an environment variable.
