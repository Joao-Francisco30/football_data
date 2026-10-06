import Link from "next/link";

export default function NotFound() {
  return (
    <main className="mx-auto w-full max-w-xl space-y-4 px-6 py-20 text-center">
      <h1 className="text-2xl font-bold">Not found</h1>
      <p className="text-gray-400">That page or league doesn&apos;t exist.</p>
      <Link href="/" className="text-sm underline">
        Back to all leagues
      </Link>
    </main>
  );
}
