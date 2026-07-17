/*
  Warnings:

  - A unique constraint covering the columns `[teamId,season]` on the table `SeasonStats` will be added. If there are existing duplicate values, this will fail.

*/
-- CreateIndex
CREATE UNIQUE INDEX "SeasonStats_teamId_season_key" ON "SeasonStats"("teamId", "season");
