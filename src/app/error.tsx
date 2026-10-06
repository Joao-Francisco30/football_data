"use client";

export default function ErrorPage({ reset }: { reset: () => void }) {
  return (
    <main className="mx-auto w-full max-w-xl space-y-4 px-6 py-20 text-center">
      <h1 className="text-2xl font-bold">Something went wrong</h1>
      <p className="text-gray-400">
        The data couldn&apos;t be loaded. The database may be unavailable.
      </p>
      <button
        type="button"
        onClick={reset}
        className="rounded-lg border border-gray-700 px-4 py-2 text-sm transition hover:border-gray-400"
      >
        Try again
      </button>
    </main>
  );
}
