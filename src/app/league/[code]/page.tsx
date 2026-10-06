import Link from "next/link";
import { notFound } from "next/navigation";
import { getPrisma } from "@/lib/prisma";

export const dynamic = "force-dynamic";

type Props = {
  params: Promise<{ code: string }>;
};

// "2025" -> "2025/26"
function formatSeason(season: string): string {
  const start = Number(season);
  if (Number.isNaN(start)) return season;
  return `${start}/${String(start + 1).slice(-2)}`;
}

export default async function LeaguePage({ params }: Props) {
  const { code } = await params;
  const prisma = getPrisma();

  const league = await prisma.league.findUnique({
    where: { code: code.toUpperCase() },
  });

  if (!league) {
    notFound();
  }

  // Most recent season that has stats for this league
  const latest = await prisma.seasonStats.findFirst({
    where: { team: { leagueId: league.id } },
    orderBy: { season: "desc" },
    select: { season: true },
  });

  const stats = latest
    ? await prisma.seasonStats.findMany({
        where: { season: latest.season, team: { leagueId: league.id } },
        include: { team: true },
      })
    : [];

  const table = stats
    .map((row) => ({
      ...row,
      goalDifference: row.goalsFor - row.goalsAgainst,
    }))
    .sort(
      (a, b) =>
        b.points - a.points ||
        b.goalDifference - a.goalDifference ||
        b.goalsFor - a.goalsFor
    );

  return (
    <main className="mx-auto w-full max-w-5xl space-y-6 px-6 py-10">
      <Link href="/" className="text-sm text-gray-400 hover:text-white">
        ← All leagues
      </Link>

      <header className="space-y-1">
        <h1 className="text-3xl font-bold">{league.name}</h1>
        <p className="text-gray-400">
          {league.country}
          {latest && ` · Season ${formatSeason(latest.season)}`}
        </p>
      </header>

      {table.length === 0 ? (
        <p className="rounded-lg border border-dashed border-gray-700 p-8 text-center text-gray-400">
          No standings imported for this league yet.
        </p>
      ) : (
        <div className="overflow-x-auto rounded-lg border border-gray-800">
          <table className="w-full min-w-[640px] text-sm">
            <thead className="border-b border-gray-800 text-left text-gray-400">
              <tr>
                <th className="px-3 py-3 font-medium">#</th>
                <th className="px-3 py-3 font-medium">Team</th>
                <th className="px-3 py-3 text-right font-medium">P</th>
                <th className="px-3 py-3 text-right font-medium">W</th>
                <th className="px-3 py-3 text-right font-medium">D</th>
                <th className="px-3 py-3 text-right font-medium">L</th>
                <th className="px-3 py-3 text-right font-medium">GF</th>
                <th className="px-3 py-3 text-right font-medium">GA</th>
                <th className="px-3 py-3 text-right font-medium">GD</th>
                <th className="px-3 py-3 text-right font-medium">Pts</th>
              </tr>
            </thead>
            <tbody>
              {table.map((row, index) => (
                <tr
                  key={row.id}
                  className="border-b border-gray-900 last:border-0 hover:bg-white/5"
                >
                  <td className="px-3 py-2 text-gray-500">{index + 1}</td>
                  <td className="px-3 py-2">
                    <div className="flex items-center gap-3">
                      {row.team.logo && (
                        // eslint-disable-next-line @next/next/no-img-element
                        <img
                          src={row.team.logo}
                          alt=""
                          width={20}
                          height={20}
                          loading="lazy"
                          className="h-5 w-5 object-contain"
                        />
                      )}
                      <span>{row.team.name}</span>
                    </div>
                  </td>
                  <td className="px-3 py-2 text-right">{row.matchesPlayed}</td>
                  <td className="px-3 py-2 text-right">{row.wins}</td>
                  <td className="px-3 py-2 text-right">{row.draws}</td>
                  <td className="px-3 py-2 text-right">{row.losses}</td>
                  <td className="px-3 py-2 text-right">{row.goalsFor}</td>
                  <td className="px-3 py-2 text-right">{row.goalsAgainst}</td>
                  <td className="px-3 py-2 text-right">
                    {row.goalDifference > 0
                      ? `+${row.goalDifference}`
                      : row.goalDifference}
                  </td>
                  <td className="px-3 py-2 text-right font-semibold">
                    {row.points}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </main>
  );
}
