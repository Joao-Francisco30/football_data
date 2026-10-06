import Link from "next/link";
import { getPrisma } from "@/lib/prisma";

// Read from the database on every request instead of at build time.
export const dynamic = "force-dynamic";

export default async function HomePage() {
  const prisma = getPrisma();

  const leagues = await prisma.league.findMany({
    orderBy: { name: "asc" },
    include: { _count: { select: { teams: true } } },
  });

  return (
    <main className="mx-auto w-full max-w-5xl space-y-8 px-6 py-10">
      <header className="space-y-2">
        <h1 className="text-3xl font-bold">Football Data</h1>
        <p className="text-gray-400">
          Pick a league to see its current standings.
        </p>
      </header>

      {leagues.length === 0 ? (
        <p className="rounded-lg border border-dashed border-gray-700 p-8 text-center text-gray-400">
          No leagues yet. Run the data pipeline (
          <code className="font-mono">python scripts/run_pipeline.py</code>) to
          import them.
        </p>
      ) : (
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {leagues.map((league) => (
            <Link
              key={league.id}
              href={`/league/${league.code}`}
              className="rounded-lg border border-gray-800 p-4 transition hover:border-gray-500"
            >
              <h2 className="text-lg font-semibold">{league.name}</h2>
              <p className="mt-1 text-sm text-gray-400">{league.country}</p>
              <p className="mt-3 text-sm text-gray-500">
                {league._count.teams} teams
              </p>
            </Link>
          ))}
        </div>
      )}
    </main>
  );
}
