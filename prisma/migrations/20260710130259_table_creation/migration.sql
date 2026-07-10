/*
  Warnings:

  - You are about to drop the column `country` on the `Team` table. All the data in the column will be lost.
  - Added the required column `leagueId` to the `Team` table without a default value. This is not possible if the table is not empty.

*/
-- AlterTable
ALTER TABLE "Team" DROP COLUMN "country",
ADD COLUMN     "founded" INTEGER,
ADD COLUMN     "leagueId" INTEGER NOT NULL,
ADD COLUMN     "logo" TEXT,
ADD COLUMN     "stadium" TEXT,
ALTER COLUMN "id" DROP DEFAULT;
DROP SEQUENCE "team_id_seq";

-- CreateTable
CREATE TABLE "League" (
    "id" INTEGER NOT NULL,
    "name" TEXT NOT NULL,
    "country" TEXT NOT NULL,

    CONSTRAINT "League_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "SeasonStats" (
    "id" SERIAL NOT NULL,
    "season" TEXT NOT NULL,
    "matchesPlayed" INTEGER NOT NULL,
    "wins" INTEGER NOT NULL,
    "draws" INTEGER NOT NULL,
    "losses" INTEGER NOT NULL,
    "goalsFor" INTEGER NOT NULL,
    "goalsAgainst" INTEGER NOT NULL,
    "points" INTEGER NOT NULL,
    "teamId" INTEGER NOT NULL,

    CONSTRAINT "SeasonStats_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "Trophy" (
    "id" SERIAL NOT NULL,
    "teamId" INTEGER NOT NULL,
    "trophy" TEXT NOT NULL,
    "year" INTEGER NOT NULL,

    CONSTRAINT "Trophy_pkey" PRIMARY KEY ("id")
);

-- AddForeignKey
ALTER TABLE "Team" ADD CONSTRAINT "Team_leagueId_fkey" FOREIGN KEY ("leagueId") REFERENCES "League"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "SeasonStats" ADD CONSTRAINT "SeasonStats_teamId_fkey" FOREIGN KEY ("teamId") REFERENCES "Team"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Trophy" ADD CONSTRAINT "Trophy_teamId_fkey" FOREIGN KEY ("teamId") REFERENCES "Team"("id") ON DELETE RESTRICT ON UPDATE CASCADE;
