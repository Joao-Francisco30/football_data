import { prisma } from "@/lib/prisma";

export default async function TestPage() {
  const teams = await prisma.team.findMany();

  return (
    <div>
      <h1>Football Data Test</h1>

      <p>Total teams: {teams.length}</p>
    </div>
  );
}