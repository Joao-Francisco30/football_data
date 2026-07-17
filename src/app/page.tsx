import { prisma } from "@/lib/prisma";

export default async function HomePage() {
  const leagues = await prisma.league.findMany({
    orderBy: {
      name: "asc",
    },
  });

  return (
    <main>
      <h1>Football Data</h1>

      {leagues.map((league) => (
        <div key={league.id}>
          {league.name} ({league.country})
        </div>
      ))}
    </main>
  );
}